import os
from PIL import Image
from constants import IMG_DIR

def resize_img_if_needs(img_name, size):
    img_path = os.path.join(IMG_DIR, img_name)
    image = Image.open(img_path)
    if (image.size[0] * image.size[1] > size[0] * size[1]):
        image.thumbnail(size)
        image.save(img_path)
