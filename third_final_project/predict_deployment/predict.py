import pickle
import pandas as pd

from flask import Flask
from flask import request
from flask import jsonify


model_file = 'model.bin'

with open(model_file, 'rb') as f_in:
    model = pickle.load(f_in)

app = Flask('prediction')

@app.route('/prediction', methods=['POST'])
def prediction():
    material_components = request.get_json()
    
    df = pd.json_normalize(material_components)
    y_pred = model.predict(df)
    
    result = {
        'proof_stress_mpa': round(float(y_pred[0][0]), 3),
        'tensile_strength_mpa': round(float(y_pred[0][1]), 3),
        'elongation_perc': round(float(y_pred[0][2]), 3),
        'reduction_in_area_perc': round(float(y_pred[0][3]), 3)
    } 

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)



