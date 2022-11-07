import os
import zipfile
import aiofiles
from os.path import join, basename, split, exists
from PIL import Image
from constants import BASE_URL, DATASETS_URL, ROOT_DIR
from src.db.postgres import DatabaseClient
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
    print('\n******** Extracting zip file... ********')
    try:
        head_path = split(zip_path)[0]
        if (exists(zip_path)):
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                zip_file.extractall(head_path)
            os.remove(zip_path)
            print('******** Zip file extracted successfully! ********')
        return zip_path.split('.zip')[0]
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

def get_image_url(image_path):
    path = image_path
    image_endpoint = ''
    while(split(path)[1] != 'dataset'):
        path_tuple = split(path)
        path = path_tuple[0]
        image_endpoint = f'/{path_tuple[1]}' + image_endpoint
    return BASE_URL + DATASETS_URL + image_endpoint

def get_dataset_db_path(dataset_db_id):
    print("\n******** Fetching dataset infos from db ********")
    DatabaseClient.initialize('deepuai')
    table = 'datasets'
    fields = 'name, n_classes'
    sql_command = f'SELECT {fields} FROM {table} WHERE id={dataset_db_id}'
    sql_response = DatabaseClient.fetch(sql_command)
    DatabaseClient.close(DatabaseClient)
    dataset = sql_response[0]
    dataset_dir = join(ROOT_DIR, 'assets', 'dataset', dataset[0])
    return dataset_dir

def get_model_db_name(model_db_id):
    print("\n******** Fetching model infos from db ********")
    DatabaseClient.initialize('deepuai')
    table = 'models'
    fields = 'name'
    sql_command = f'SELECT {fields} FROM {table} WHERE id={model_db_id}'
    sql_response = DatabaseClient.fetch(sql_command)
    DatabaseClient.close(DatabaseClient)
    model_name = sql_response[0][0].lower()
    return model_name