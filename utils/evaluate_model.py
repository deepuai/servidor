import numpy as np
from applications.ResNet import ResNet
from utils.preprocessing import resize_img_if_needs
def convert_floats(predictions):
    for i in range(len(predictions)):
        predictions[i] = (
            predictions[i][0],predictions[i][1],
            float(predictions[i][2])
        )

def evaluate_model(model_name, image):
    model = ResNet()
    predictions = model.predict_from_bytes(uploaded_file=image, n_predictions=3)
    # img_name = 'capivara.jpg'
    # resize_img_if_needs(img_name=img_name, size=(224,224))
    #predictions = model.predict_from_path(img_name=img_name, n_predictions=3)
    convert_floats(predictions)
    return {
        "message": "Hello World",
        "model_name":model_name,
        "predictions":predictions}