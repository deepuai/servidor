from os.path import join

from src.applications.ResNet import ResNet50
from src.controllers import applications as applications_controller

def initialize_bd():
    try:
        weights_name = 'imagenet'
        model = ResNet50(weights_name)
        model.save(join('assets','models','resnet50',weights_name))
        resnet_application = {
            'name': 'ResNet50',
            'version': 'ImageNet',
            'applicationAccuracy': 92.1,
            'applicationNumberOfAccesses': 5,
            'datasetName': 'ImageNet',
            'datasetSize': 21000,
            'datasetNumberOfImgs': 1024,
            'datasetNumberOfClasses': 28,
            'modelName': 'ResNet50',
            'modelNumberOfParams': 25.6,
            'modelNumberOfLayers': 107,
            'modelSize': 88
        }
        applications_controller.insert(resnet_application)
        return("Sucesso!")
    except Exception as e:
        return(e)