import tensorflow as tf
from os.path import join
from src.utils.helpers import get_input_size_or_shape

def initialize_models():
    try:
        resnet50 = tf.keras.applications.resnet50.ResNet50(
            weights='imagenet',
            input_shape=get_input_size_or_shape(model='resnet50', shape=True)
            )
        resnet50.save(join('assets','models','resnet50','imagenet'))

        xception = tf.keras.applications.xception.Xception(
            weights='imagenet',
            input_shape=get_input_size_or_shape(model='xception', shape=True))
        xception.save(join('assets','models','xception','imagenet'))
        
        return("Sucesso!")
    except Exception as e:
        return(e)