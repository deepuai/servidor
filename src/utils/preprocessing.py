import os
from os.path import join
import tensorflow as tf
from PIL import Image
from constants import IMG_DIR

def resize_img_if_needs(img_name, size):
    img_path = os.path.join(IMG_DIR, img_name)
    image = Image.open(img_path)
    if (image.size[0] * image.size[1] > size[0] * size[1]):
        image.thumbnail(size)
        image.save(img_path)

def preprocess_dataset_from_directory(dir, validation_split=0.2, seed=42, img_size=(256, 256), batch_size=32):
    print('\n******** Preprocessing the training subset... ********')
    training_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        directory=dir,
        validation_split=validation_split,
        subset="training",
        seed=seed,
        image_size=img_size,
        batch_size=batch_size)
    print('\n******** Preprocessing the validation subset... ********')
    validation_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        directory=dir,
        validation_split=validation_split,
        subset="validation",
        seed=seed,
        image_size=img_size,
        batch_size=batch_size)
    dataset = {
        'training': training_dataset,
        'validation': validation_dataset,
        'classes': training_dataset.class_names,
        'number_of_classes': len(training_dataset.class_names)
    }
    return dataset