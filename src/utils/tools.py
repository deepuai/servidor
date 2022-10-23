import os
import zipfile
import aiofiles
from os.path import join, basename, split
from PIL import Image

CHUNK_SIZE = 1024 * 1024

async def save_uploaded_zip(zip_file, path):
    try:
        print('Saving uploaded file...')
        os.makedirs(path, exist_ok=True)
        full_path = join(path, basename(zip_file.filename))
        async with aiofiles.open(full_path, 'wb') as file:
            while chunk := await zip_file.read(CHUNK_SIZE):
                await file.write(chunk)
    except Exception as e:
        raise e
    finally:
        await zip_file.close()
        print('Upload file was saved successfully!')
        return full_path

def extract_zip(zip_path):
    print('Extracting zip file...')
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            zip_file.extractall(split(zip_path)[0])
        print('Zip file extracted successfully!')
        os.remove(zip_path)
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
