import numpy as np
import os
from tensorflow.keras.preprocessing import image
from constants import IMG_DIR

class Application:
    def predict(self, img_name, n_predictions):
        img_path = os.path.join(IMG_DIR, img_name)
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = self.preprocess_input(x)

        preds = self.model.predict(x)
        return self.decode_predictions(preds, top=n_predictions)[0]