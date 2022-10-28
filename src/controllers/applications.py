import json
from os.path import join
from constants import ROOT_DIR
from src.db.postgres import DatabaseClient
from src.utils.tools import save_uploaded_zip
from src.rabbitmq.producer import send_message_to_queue

TABLE = 'applications'

async def fit(model_name, weights_name, deepuai_app, version, zip_file):
    path = join(ROOT_DIR, 'assets', 'dataset', f'{model_name}-{weights_name}')
    full_path = await save_uploaded_zip(zip_file, path)
    
    message = {
        'model': model_name,
        'weights': weights_name,
        'dir': full_path
    }
    send_message_to_queue(queue='fit', message=json.dumps(message))

    return {
        "message": "Esse treinamento foi colocado na fila, quando terminar você será avisado!"
    }