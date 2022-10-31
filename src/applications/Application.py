import os
import numpy as np
import tensorflow as tf
from PIL import Image
from constants import ROOT_DIR
from keras.api._v2.keras.preprocessing import image
from src.utils.helpers import decode_predictions
from keras.models import load_model

BASE_WEIGHTS = ['imagenet']
class Application:
    def __init__(self, model_name, weights_name):
        self.model = load_model(os.path.join(ROOT_DIR,'assets','models',model_name,weights_name))

    def predict_from_uploaded_file(self, uploaded_file, n_predictions, model_name, weights_name, input_size):
        img = Image.open(uploaded_file.file)
        img = img.resize(input_size)
        x = np.asarray(img)
        img.close()
        x = np.expand_dims(x, axis=0)
        preds = self.model.predict(x)
        return decode_predictions(preds, model_name, weights_name, n_predictions)