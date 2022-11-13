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

def fit(message):
    try:
        print("******** START FIT PROCESS ******** \n")
        print(f'Message: \n{message}')
        if message.get('dataset_id', False):
            dataset_path = get_dataset_db_path(message['dataset_id'])
        else:
            dataset_path = extract_zip(message['dir'])
        dataset = preprocess_dataset_from_directory(
            dir=dataset_path,
            img_size=get_input_size_or_shape(model=message['model'], shape=False))
        print(f'Dataset: {dataset}')
        print("\n******** Instantiating selected keras model ********")
        application = Application(message['model'], message.get('weights','random'))
        pretrained_model = Model(application.model.input, application.model.layers[-2].output)
        if message.get('weights', False):
            for layer in pretrained_model.layers:
                layer.trainable=False

        print("\n******** Creating sequencial model for transfer learning ********")
        model = create_sequencial_model(pretrained_model, dataset['number_of_classes'])
        model.compile(optimizer=Adam(lr=0.001),loss='sparse_categorical_crossentropy',metrics=['accuracy'])
        
        print("\n******** Initializing fit ********")
        epochs=5
        applicationHistory = model.fit(
            dataset['training'],
            validation_data=dataset['validation'],
            epochs=epochs
        )
        print("******** Fit finished ********")

        name = message['deepuai_app']
        version = message['version']
        accuracy = applicationHistory.history['val_accuracy'][-1]
        classes = json.dumps(dataset['classes'])
        parent_id = message['parent_id']
        model_id = message['model_id']
        dataset_id = message.get('dataset_id', False)

        DatabaseClient.initialize('deepuai')

        if not dataset_id:
            print("\n******** Saving new dataset into database ********")
            dataset_name = os.path.split(dataset_path)[1]
            dataset_size = 0
            n_images = 0
            n_classes = dataset['number_of_classes']
            images_urls = []
            for path, _, files in walk(dataset_path):
                n_images += len(files)
                for f in files:
                    fp = join(path, f)
                    dataset_size += getsize(fp)
                    images_urls.append(get_image_url(fp))
            images_urls = json.dumps(images_urls)
            DatabaseClient.insert_into(
                table='datasets',
                fields='name, size, n_images, n_classes, classes, images',
                values=f"'{dataset_name}', '{dataset_size}', {n_images}, {n_classes}, '{classes}', '{images_urls}'")
            dataset_id = DatabaseClient.select_from(
                table='datasets',
                fields='id',
                where=f"name='{dataset_name}' AND size='{dataset_size}' AND n_images='{n_images}' AND n_classes='{n_classes}'"
            )[0][0]

        print("\n******** Saving new application into database ********")
        DatabaseClient.insert_into(
                table='applications',
                fields='name, version, accuracy, n_accesses, classes, parent_id, model_id, dataset_id',
                values=f"'{name}', '{version}', {accuracy}, 0, '{classes}', {parent_id}, {model_id}, {dataset_id}")
        DatabaseClient.close(DatabaseClient)
        
        print("\n******** Saving new application as keras model ********")
        model.save(os.path.join(ROOT_DIR, 'assets','models',message['model'],version))
        print("******** Application was saved ********")
    except Exception as e:
        print(f'Error: {e}')