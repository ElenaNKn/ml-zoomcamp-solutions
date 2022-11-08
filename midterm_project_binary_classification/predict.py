import pickle

from flask import Flask
from flask import request
from flask import jsonify


model_file = 'model.bin'

with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

app = Flask('popularity')

@app.route('/predict', methods=['POST'])
def predict():
    course = request.get_json()

    X = dv.transform([course])
    y_pred = model.predict_proba(X)[0, 1]
    popular = y_pred >= 0.5

    result = {
        'probability_of_being_popular': float(y_pred),
        'is_popular': bool(popular)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)



