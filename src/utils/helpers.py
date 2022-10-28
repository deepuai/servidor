def convert_predictions_to_float(predictions):
    for i in range(len(predictions)):
        predictions[i] = (
            predictions[i][0],
            predictions[i][1],
            round(float(predictions[i][2]), 4)
        )