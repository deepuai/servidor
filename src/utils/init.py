from os.path import join
from tensorflow.keras.applications.resnet50 import ResNet50

def initialize_models():
    try:
        resnet50 = ResNet50(weights='imagenet', input_shape=(224,224,3))
        resnet50.save(join('assets','models','resnet50','imagenet'))
        return("Sucesso!")
    except Exception as e:
        return(e)