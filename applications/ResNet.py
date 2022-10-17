from applications.Application import Application
from keras.models import load_model, Model
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

BASE_WEIGHTS = ['imagenet']
class ResNet50UAI(Application):
    def __init__(self, weights_name):
        if weights_name in BASE_WEIGHTS:
            self.model = ResNet50(weights=weights_name)
        else:
            self.model = load_model(f'models/resnet50/{weights_name}')
        self.preprocess_input = preprocess_input
        self.decode_predictions = decode_predictions