from src.db.mongodb import DatabaseClient
from src.utils.helpers import application_helper

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