def application_helper(application) -> dict:
    return {
        'id': str(application['_id']),
        'name': application['name'],
        'version': application['version'],
        'applicationAccuracy': application['applicationAccuracy'],
        'applicationNumberOfAccesses': application['applicationNumberOfAccesses'],
        'datasetName': application['datasetName'],
        'datasetSize': application['datasetSize'], 
        'datasetNumberOfImgs': application['datasetNumberOfImgs'],
        'datasetNumberOfClasses': application['datasetNumberOfClasses'],
        'modelName': application['modelName'],
        'modelNumberOfParams': application['modelNumberOfParams'],
        'modelNumberOfLayers': application['modelNumberOfLayers'],
        'modelSize': application['modelSize']
    }

def convert_predictions_to_float(predictions):
    for i in range(len(predictions)):
        predictions[i] = (
            predictions[i][0],
            predictions[i][1],
            round(float(predictions[i][2]), 4)
        )