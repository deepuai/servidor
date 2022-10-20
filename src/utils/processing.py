from src.utils.helpers import convert_predictions_to_float
from src.applications.ResNet import ResNet50UAI

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

def fit(rabbitMQ_message):
    # treinamento
    print(rabbitMQ_message)

    return {
        "message": "Sucesso!"
    }