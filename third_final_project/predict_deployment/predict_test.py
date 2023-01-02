import requests
import json

url = 'http://localhost:9696/prediction'

material = {
    "c": "0.12",
    "si": "0.36",
    "mn": "0.52",
    "p": "0.009",
    "s": "0.003",
    "ni": "0.089",
    "cr": "0.97",
    "mo": "0.610",
    "cu": "0.04",
    "v": "0",
    "al": "0.003",
    "n": "0.0066",
    "nb_and_ti": "0",
    "temperature_celcius": "27"
    }

# true values:
# proof_stress_mpa	342
# tensile_strength_mpa	490
# elongation_perc	  30
# reduction_in_area_perc   71

response = requests.post(url, json=material).json()

print(json.dumps(response, indent=1))
