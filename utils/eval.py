from statistics import mode
import numpy as np
from applications.ResNet import ResNet50UAI
from keras.models import load_model
from utils.preprocessing import resize_img_if_needs
def convert_floats(predictions):
    for i in range(len(predictions)):
        predictions[i] = (
            predictions[i][0],predictions[i][1],
        )

def eval_resnet50(weights_name, image):
    # aqui entra o código que carrega 0 arquivo .h5 de uma rede com base em seu nome
    model = ResNet50UAI(weights_name)
    predictions = model.predict_from_uploaded_file(uploaded_file=image, n_predictions=3)
    convert_floats(predictions)
    return {
        "message": "Eis a avaliação da rede:",
        "model_name":weights_name,
        "predictions":predictions,
        "metrics":model.metrics}