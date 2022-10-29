from src.db.postgres import DatabaseClient

def convert_predictions_to_float(predictions):
    for i in range(len(predictions)):
        predictions[i] = (
            predictions[i][0],
            predictions[i][1],
            round(float(predictions[i][2]), 4)
        )

def decode_predictions(predictions, version, n_predictions):
    DatabaseClient.initialize('deepuai')
    table = 'applications'
    field = 'classes'
    where = f"version = '{version}'"
    sql_command = f'SELECT {field} FROM {table} WHERE {where}'
    print(sql_command)
    classes = DatabaseClient.fetch(sql_command)
    DatabaseClient.close(DatabaseClient)

    classes = classes[0][0]
    predictions = predictions[0]
    response = [[id, classes[id], predictions[id]] for id in range(0, len(classes))]
    response.sort(key=lambda elem: elem[2], reverse=True)
    return response[0:n_predictions]