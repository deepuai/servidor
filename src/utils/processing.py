import tensorflow as tf
from src.utils.helpers import convert_predictions_to_float
from src.utils.preprocessing import preprocess_dataset_from_directory
from src.utils.tools import extract_zip
from src.applications.ResNet import ResNet50UAI
from tensorflow.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam

def eval(model_name, weights_name, image):
    # aqui entra o código que carrega 0 arquivo .h5 de uma rede com base em seu nome
    model = ResNet50UAI(weights_name)
    predictions = model.predict_from_uploaded_file(uploaded_file=image, n_predictions=3)
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
    dataset_path = extract_zip(message['dir'])
    dataset = preprocess_dataset_from_directory(dir=dataset_path, img_size=(256,256))

    pretrained_model= tf.keras.applications.ResNet50(
        include_top=False,
        input_shape=(256,256,3),
        pooling='avg',
        classes=dataset['number_of_classes'],
        weights='imagenet')
    for layer in pretrained_model.layers:
        layer.trainable=False

    model = create_sequencial_model(pretrained_model, dataset['number_of_classes'])
    model.compile(optimizer=Adam(lr=0.001),loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    
    epochs=1
    application = model.fit(
        dataset['training'],
        validation_data=dataset['validation'],
        epochs=epochs
    )
    print(application.history['accuracy'])
    print(application.history['val_accuracy'])
    
    return {
        "message": "Sucesso!"
    }