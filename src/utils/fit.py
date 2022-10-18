from os.path import join
from constants import ROOT_DIR
from src.applications.ResNet import ResNet50UAI
from src.utils.preprocessing import extract_zip, load_unziped_dataset

def fit_resnet50(weights_name, zip_file):
    path = join(ROOT_DIR, 'assets', 'dataset', 'resnet50')
    extract_zip(zip_file, output_dir=path)
    x, y = load_unziped_dataset(path)
    print(x, y)

    # treinamento

    return {
        "message": "Success!"
    }