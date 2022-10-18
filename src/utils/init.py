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
            'datasetImagens': [
                'https://cdn.pixabay.com/photo/2016/03/27/22/22/fox-1284512_960_720.jpg',
                'https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_960_720.jpg',
                'https://cdn.pixabay.com/photo/2017/02/07/16/47/kingfisher-2046453_960_720.jpg',
                'https://cdn.pixabay.com/photo/2018/07/31/22/08/lion-3576045_960_720.jpg',
                'https://cdn.pixabay.com/photo/2017/09/25/13/12/cocker-spaniel-2785074_960_720.jpg',
                'https://cdn.pixabay.com/photo/2016/12/31/21/22/discus-fish-1943755_960_720.jpg',
                'https://cdn.pixabay.com/photo/2018/03/31/06/31/dog-3277416_960_720.jpg',
                'https://cdn.pixabay.com/photo/2019/08/19/07/45/corgi-4415649_960_720.jpg',
                'https://cdn.pixabay.com/photo/2016/12/04/21/58/rabbit-1882699_960_720.jpg',
                'https://cdn.pixabay.com/photo/2016/10/31/14/55/rottweiler-1785760_960_720.jpg',
                'https://cdn.pixabay.com/photo/2017/02/18/13/55/swan-2077219_960_720.jpg',
                'https://cdn.pixabay.com/photo/2016/07/15/15/55/dachshund-1519374_960_720.jpg'
            ],
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