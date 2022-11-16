import json
from os.path import join
from constants import ROOT_DIR
from src.db.postgres import DatabaseClient
from src.utils.tools import save_uploaded_zip
from src.rabbitmq.producer import send_message_to_queue

TABLE = 'applications'

async def fit_from_file(model_name, weights_name, parent_id, deepuai_app, version, model_id, zip_file):
    path = join(ROOT_DIR, 'assets', 'dataset')
    dataset_path = await save_uploaded_zip(zip_file, path)
    
    message = {
        'parent_id': parent_id,
        'model': model_name,
        'model_id': model_id,
        'weights': weights_name,
        'deepuai_app': deepuai_app,
        'version': version,
        'dir': dataset_path
    }
    send_message_to_queue(queue='fit', message=json.dumps(message))
    DatabaseClient.initialize('deepuai')
    DatabaseClient.insert_into(
            table=TABLE,
            fields='name, version, status, parent_id, model_id',
            values=f"'{deepuai_app}', '{version}', 'WAITING', {parent_id}, {model_id}")
    DatabaseClient.close(DatabaseClient)

    return {
        "message": "Esse treinamento foi colocado na fila. É possível acompanhar o andamento do processo na tela Aplicações > Na fila!"
    }

async def fit_from_dataset(model_name, weights_name, parent_id, deepuai_app, version, model_id, dataset_id):
    message = {
        'parent_id': parent_id,
        'model': model_name,
        'model_id': model_id,
        'weights': weights_name,
        'deepuai_app': deepuai_app,
        'version': version,
        'dataset_id': dataset_id
    }
    send_message_to_queue(queue='fit', message=json.dumps(message))
    DatabaseClient.initialize('deepuai')
    fields = 'name, version, status, model_id, dataset_id' + (', parent_id' if parent_id>0 else '')
    values = f"'{deepuai_app}', '{version}', 'WAITING', {model_id}, {dataset_id}" + (f", {parent_id}" if parent_id>0 else '')
    DatabaseClient.insert_into(
            table=TABLE,
            fields=fields,
            values=values)
    DatabaseClient.close(DatabaseClient)

    return {
        "message": "Esse treinamento foi colocado na fila. É possível acompanhar o andamento do processo na tela Aplicações > Na fila!"
    }