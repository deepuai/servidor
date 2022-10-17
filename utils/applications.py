import os
import json
def applications(model_name):
    application_dir = os.path
    models_dir = os.path.join(application_dir, 'models')
    available_weights = []
    for weights_name in os.scandir(application_dir):
        if weights_name.is_dir():
            assets_path = os.path(models_dir, 'assets')
            with open(os.path(assets_path, 'config.json')) as json_file:
                data = json.load(json_file)
                available_weights.append(data)
    return available_weights