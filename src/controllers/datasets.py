import json
from os.path import join, split, getsize
from os import listdir, walk
from constants import ROOT_DIR, BASE_URL, DATASETS_URL
from src.db.postgres import DatabaseClient
from src.utils.tools import save_uploaded_zip, extract_zip

TABLE = 'datasets'
def get_image_url(image_path):
    path = image_path
    image_endpoint = ''
    while(split(path)[1] != 'dataset'):
        path_tuple = split(path)
        path = path_tuple[0]
        image_endpoint = f'/{path_tuple[1]}' + image_endpoint
    return BASE_URL + DATASETS_URL + image_endpoint

async def save(zip_file):
    path = join(ROOT_DIR, 'assets', 'dataset')
    dataset_path = await save_uploaded_zip(zip_file, path)
    dataset_path = extract_zip(dataset_path)

    dataset_name = split(dataset_path)[1]
    dataset_classes = listdir(join(dataset_path,'train'))
    classes_length = len(dataset_classes)

    dataset_size = 0
    images_length = 0
    images_urls = []
    for path, _, files in walk(dataset_path):
        images_length += len(files)
        for f in files:
            fp = join(path, f)
            dataset_size += getsize(fp)
            images_urls.append(get_image_url(fp))
    images_urls = json.dumps(images_urls)
    dataset_classes = json.dumps(dataset_classes)

    # Salvar Dataset no Banco
    DatabaseClient.initialize('deepuai')
    fields = 'name, size, n_images, n_classes, classes, images'
    values = f"'{dataset_name}', '{dataset_size}', {images_length}, {classes_length}, '{dataset_classes}', '{images_urls}'"
    sql_command = f'INSERT INTO {TABLE} ({fields}) VALUES ({values})'
    DatabaseClient.execute(sql_command)
    DatabaseClient.close(DatabaseClient)
    return {"message": "Dataset criado com sucesso!"}