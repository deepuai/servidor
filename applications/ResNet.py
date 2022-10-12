from applications.Application import Application
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

class ResNet(Application):
    def __init__(self):
        self.model = ResNet50(weights='imagenet')
        self.preprocess_input = preprocess_input
        self.decode_predictions = decode_predictions
