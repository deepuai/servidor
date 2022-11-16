import os
import json
from os import walk
from os.path import join, getsize
from constants import ROOT_DIR
from src.utils.helpers import convert_predictions_to_float, get_input_size_or_shape
from src.utils.preprocessing import preprocess_dataset_from_directory
from src.utils.tools import extract_zip, get_dataset_db_path, get_image_url
from src.db.postgres import DatabaseClient
from src.applications.Application import Application
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam

def eval(model_name, weights_name, image):
    application = Application(model_name, weights_name)
    predictions = application.predict_from_uploaded_file(
        uploaded_file=image,
        n_predictions=3,
        model_name=model_name,
        weights_name=weights_name,
        input_size=get_input_size_or_shape(model=model_name, shape=False))
    convert_predictions_to_float(predictions)
    return {
        "message": "Eis a avaliação da rede:",
        "model_name": model_name,
        'weights_name': weights_name,
        "predictions":predictions
    }

def create_sequencial_model(pretrained_model, number_of_classes):
    model = Sequential()
    model.add(pretrained_model)
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dense(number_of_classes, activation='softmax'))
    return model

def persist_dataset_from_zip(dataset_path, n_classes):
    print("\n******** Saving new dataset into database ********")
    dataset_name = os.path.split(dataset_path)[1]
    dataset_size = 0
    n_images = 0
    images_urls = []
    for path, _, files in walk(dataset_path):
        n_images += len(files)
        for f in files:
            fp = join(path, f)
            dataset_size += getsize(fp)
            images_urls.append(get_image_url(fp))
    images_urls = json.dumps(images_urls)
    DatabaseClient.initialize('deepuai')
    DatabaseClient.insert_into(
        table='datasets',
        fields='name, size, n_images, n_classes, classes, images',
        values=f"'{dataset_name}', '{dataset_size}', {n_images}, {n_classes}, '{n_classes}', '{images_urls}'")
    dataset_id = DatabaseClient.select_from(
        table='datasets',
        fields='id',
        where=f"name='{dataset_name}' AND size='{dataset_size}' AND n_images='{n_images}' AND n_classes='{n_classes}'"
    )[0][0]
    DatabaseClient.close(DatabaseClient)
    return dataset_id

def fit(message):
    try:
        print("******** START FIT PROCESS ******** \n")
        print(f'Message: \n{message}')
        name = message['deepuai_app']
        model_name = message['model']
        weights = message['weights']
        version = message['version']
        dataset_id = message.get('dataset_id', False)
        
        print("\n******** Updating application for FITTING status ********")
        DatabaseClient.initialize('deepuai')
        application_id = DatabaseClient.select_from(
                table='applications',
                fields='id',
                where=f"name='{name}' AND version='{version}'")[0][0]
        DatabaseClient.update(
            table='applications',
            values=f"status = 'FITTING'",
            condition=f"id = {application_id}")
        DatabaseClient.close(DatabaseClient)

        if dataset_id:
            print("\n******** Getting dataset from database ********")
            dataset_path = get_dataset_db_path(dataset_id)
        else:
            print("\n******** Extracting uploaded dataset ********")
            dataset_path = extract_zip(message['dir'])

        dataset = preprocess_dataset_from_directory(
            dir=dataset_path,
            img_size=get_input_size_or_shape(model=model_name, shape=False))

        if not dataset_id: dataset_id = persist_dataset_from_zip(dataset_path, dataset['number_of_classes'])

        print("\n******** Instantiating selected keras model ********")
        application = Application(model_name, weights)
        pretrained_model = Model(application.model.input, application.model.layers[-2].output)
        if weights != 'random':
            print("\n******** Creating sequencial model for transfer learning ********")
            for layer in pretrained_model.layers:
                layer.trainable=False
        else:
            print("\n******** Creating sequencial model for complete training ********")

        model = create_sequencial_model(pretrained_model, dataset['number_of_classes'])
        model.compile(optimizer=Adam(lr=0.001),loss='sparse_categorical_crossentropy',metrics=['accuracy'])
        
        print("\n******** Initializing fit [5 epochs] ********")
        epochs=5
        applicationHistory = model.fit(
            dataset['training'],
            validation_data=dataset['validation'],
            epochs=epochs)

        print("******** Fit finished ********")
        accuracy = applicationHistory.history['val_accuracy'][-1]
        classes = json.dumps(dataset['classes'])
        
        print("\n******** Saving new application as keras model ********")
        model.save(os.path.join(ROOT_DIR, 'assets', 'models', model_name, version))
        print("******** Application was saved ********")

        print("\n******** Updating application into database to FITTED status ********")
        DatabaseClient.initialize('deepuai')
        DatabaseClient.update(
            table='applications',
            values=f"status = 'FITTED', accuracy = '{accuracy}', classes = '{classes}', dataset_id = '{dataset_id}'",
            condition=f"id = {application_id}")
        DatabaseClient.close(DatabaseClient)
    except Exception as e:
        print(f'Error: {e}')