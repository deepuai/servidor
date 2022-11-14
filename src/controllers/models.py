import json
from src.rabbitmq.producer import send_message_to_queue
from src.utils.tools import get_model_db_name

TABLE = 'models'

async def fit_from_dataset(deepuai_app, version, model_id, dataset_id):
    message = {
        'deepuai_app':deepuai_app,
        'version': version,
        'dataset_id': dataset_id,
        'model_id': model_id,
        'model': get_model_db_name(model_db_id=model_id)
    }
    send_message_to_queue(queue='fit', message=json.dumps(message))
    return {
        "message": "Esse treinamento foi colocado na fila, quando terminar você será avisado!"
    }