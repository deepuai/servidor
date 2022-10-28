from os.path import join

from src.applications.ResNet import ResNet50UAI

def initialize_models():
    try:
        weights_name = 'imagenet'
        application = ResNet50UAI(weights_name)
        application.model.save(join('assets','models','resnet50',weights_name))
        return("Sucesso!")
    except Exception as e:
        return(e)