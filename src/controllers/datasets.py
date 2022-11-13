import json
from os.path import join, split, getsize
from os import listdir, walk
from constants import ROOT_DIR, BASE_URL, DATASETS_URL
from src.db.postgres import DatabaseClient
from src.utils.tools import save_uploaded_zip, extract_zip, get_image_url

TABLE = 'datasets'
async def save(zip_file):
    path = join(ROOT_DIR, 'assets', 'dataset')
    dataset_path = await save_uploaded_zip(zip_file, path)
    dataset_path = extract_zip(dataset_path)

    dataset_name = split(dataset_path)[1]
    dataset_classes = listdir(dataset_path)
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
    DatabaseClient.insert_into(
                table=TABLE,
                fields='name, size, n_images, n_classes, classes, images',
                values=f"'{dataset_name}', '{dataset_size}', {images_length}, {classes_length}, '{dataset_classes}', '{images_urls}'")
    DatabaseClient.close(DatabaseClient)
    return {"message": "Dataset criado com sucesso!"}