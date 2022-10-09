import pickle

from flask import Flask
from flask import request
from flask import jsonify


model_file = 'model2.bin'
vect_file = 'dv.bin'

with open(model_file, 'rb') as fm_in:
    model = pickle.load(fm_in)

with open(vect_file, 'rb') as fdv_in:
    dv = pickle.load(fdv_in)

app = Flask('card')

@app.route('/predict_web', methods=['POST'])
def predict():
    client_features = request.get_json()

    X = dv.transform([client_features])
    y_pred = model.predict_proba(X)[0, 1]
    card = y_pred >= 0.5

    result = {
        'card_probability': float(y_pred)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)