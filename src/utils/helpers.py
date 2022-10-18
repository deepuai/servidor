def application_helper(application) -> dict:
    return {
        'id': str(application['_id']),
        'name': application['name'],
        'version': application['version'],
        'applicationAccuracy': application['applicationAccuracy'],
        'applicationNumberOfAccesses': application['applicationNumberOfAccesses'],
        'datasetSize': application['datasetSize'], 
        'datasetNumberOfImgs': application['datasetNumberOfImgs'],
        'datasetNumberOfClasses': application['datasetNumberOfClasses'],
        'modelName': application['modelName'],
        'modelNumberOfParams': application['modelNumberOfParams'],
        'modelNumberOfLayers': application['modelNumberOfLayers'],
        'modelSize': application['modelSize']
    }