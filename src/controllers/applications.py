import json
from os.path import join
from constants import ROOT_DIR
from src.db.mongodb import DatabaseClient
from src.utils.helpers import application_helper
from src.utils.tools import extract_zip
from src.rabbitmq.producer import send_message_to_queue

COLLECTION = 'applications'

def list_all():
    applications = []
    for application in DatabaseClient.find(COLLECTION, query={}):
        applications.append(application_helper(application))
    return applications

def insert(application):
    return DatabaseClient.insert_one(COLLECTION, application)

def remove(query):
    return DatabaseClient.delete(COLLECTION, query)

def list_dataset_imagens(application, datasetName):
    query = {
        'name': application,
        'datasetName': datasetName
    }
    filter = { 
        '_id': 0,
        'datasetImagens': 1
    }
    return DatabaseClient.find_one(COLLECTION, query, filter)

def fit(model_name, weights_name, zip_file):
    path = join(ROOT_DIR, 'assets', 'dataset', model_name)
    extract_zip(zip_file, output_dir=path)
    
    message = {
        'model': model_name,
        'weights': weights_name,
        'dataset_dir': path
    }
    send_message_to_queue(queue='fit', message=json.dumps(message))

    return {
        "message": "Esse treinamento foi colocado na fila, quando terminar você será avisado!"
    }