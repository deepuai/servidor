from applications.ResNet import ResNet50
def init_base():
    try:
        model = ResNet50('imagenet')
        model.save('models/resnet50/imagenet')
        return("Sucesso!")
    except Exception as e:
        return(e)