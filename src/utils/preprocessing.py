import os
import tempfile
import zipfile
from PIL import Image
from constants import IMG_DIR

def resize_img_if_needs(img_name, size):
    img_path = os.path.join(IMG_DIR, img_name)
    image = Image.open(img_path)
    if (image.size[0] * image.size[1] > size[0] * size[1]):
        image.thumbnail(size)
        image.save(img_path)

def extract_zip(zip_file, output_dir):
    try:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
            os.chdir(temp_dir)
            os.mkdir('input')

            with open("input/zip_file.zip", 'wb') as new_file:
                new_file.write(zip_file.file._file.getvalue())

                with zipfile.ZipFile("input/zip_file.zip") as zip_file:
                    for zip_info in zip_file.infolist():
                        zip_info.filename = zip_info.filename.split('/')[1]
                        zip_file.extract(zip_info, output_dir)
    except Exception as e:
        print(e)

def load_unziped_dataset(dir):
    try:
        files = []
        labels = []
        file_list = os.listdir(dir)
        for file in file_list:
            img = Image.open(os.path.join(dir, file))
            files.append(img)
            labels.append(file.split('.')[0])
        return ( files, labels )
    except Exception as e:
        print(e)
