import tensorflow as tf
from src.db.postgres import DatabaseClient

BASE_WEIGHTS = ['imagenet']
BASE_PREDICTIONS_DECODE = {
    'resnet50': tf.keras.applications.resnet50.decode_predictions,
    'xception': tf.keras.applications.xception.decode_predictions
}

def convert_predictions_to_float(predictions):
    for i in range(len(predictions)):
        predictions[i] = (
            predictions[i][0],
            predictions[i][1],
            round(float(predictions[i][2]), 4)
        )

def decode_predictions(predictions, model, version, n_predictions):
    if (version in BASE_WEIGHTS):
        return BASE_PREDICTIONS_DECODE[model](predictions, top=n_predictions)[0]
    else:
        DatabaseClient.initialize('deepuai')
        table = 'applications'
        field = 'classes'
        where = f"version = '{version}'"
        sql_command = f'SELECT {field} FROM {table} WHERE {where}'
        print(sql_command)
        classes = DatabaseClient.fetch(sql_command)
        DatabaseClient.close(DatabaseClient)

        classes = classes[0][0]
        predictions = predictions[0]
        response = [[id, classes[id], predictions[id]] for id in range(0, len(classes))]
        response.sort(key=lambda elem: elem[2], reverse=True)
        return response[0:n_predictions]

def get_input_size_or_shape(model, shape=True):
    if model == 'resnet50':
        input_size = (224,224)
    elif model == 'xception':
        input_size = (299,299)
    
    if (shape == True):
        input_shape = input_size + (3,)
        return input_shape
    return input_size
