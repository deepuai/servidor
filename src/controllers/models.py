import json
from src.rabbitmq.producer import send_message_to_queue
from src.utils.tools import get_model_db_name

TABLE = 'models'

async def fit_from_dataset(new_app_version_code, model_id, dataset_id):
    message = {
        'new_app_version_code': new_app_version_code,
        'dataset_id': dataset_id,
        'model_id': model_id,
        'model': get_model_db_name(model_db_id=model_id)
    }
    send_message_to_queue(queue='fit', message=json.dumps(message))
    return {
        "message": "Esse treinamento foi colocado na fila, quando terminar você será avisado!"
    }