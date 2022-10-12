from applications.ResNet import ResNet
from utils.preprocessing import resize_img_if_needs

if __name__ == "__main__":
    img_name = 'capivara.jpg'
    resize_img_if_needs(img_name=img_name, size=(224,224))

    resNet = ResNet()
    predictions = resNet.predict(img_name=img_name, n_predictions=3)
    print('Predicted:', predictions)
    
    
