import numpy as np
from PIL import Image
from keras.api._v2.keras.preprocessing import image
from src.utils.helpers import decode_predictions

BASE_WEIGHTS = ['imagenet']
class Application:
    def predict_from_path(self, img_path, n_predictions):
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = self.preprocess_input(x)
        preds = self.model.predict(x)
        return self.decode_predictions(preds, top=n_predictions)[0]

    def predict_from_uploaded_file(self, uploaded_file, n_predictions, weights_name):
        img = Image.open(uploaded_file.file)
        img = img.resize((224,224))
        x = np.asarray(img)
        img.close()
        x = np.expand_dims(x, axis=0)
        preds = self.model.predict(x)
        if weights_name in BASE_WEIGHTS:
            return self.decode_predictions(preds, top=n_predictions)[0]
        else:
            preds = self.model.predict(x)
            return decode_predictions(preds, weights_name, n_predictions)