from applications.ResNet import ResNet50
def init_base():
    try:
        weights_name = 'imagenet'
        model = ResNet50(weights_name)
        model.save(f'models/resnet50/{weights_name}')
        config = {
            'name': 'ResNet50-imagenet',
            'version': 'ImageNet',
            'applicationAccuracy': 92.1,
            'applicationNumberOfAccesses': 5,
            'datasetSize': 21000, # MB 
            'datasetNumberOfImgs': 1024,
            'datasetNumberOfClasses': 28,
            'modelName': 'ResNet50',
            'modelNumberOfParams': 25.6, # M
            'modelNumberOfLayers': 107,
            'modelSize': 88
        }
        with open("models/resnet50/imagenet/config.json", "w") as outfile:
            outfile.write(config)
        return("Sucesso!")
    except Exception as e:
        return(e)