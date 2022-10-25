import numpy as np

import bentoml
from bentoml.io import JSON

model_ref = bentoml.xgboost.get("credit_risk_model:latest")  # reference to model
dv = model_ref.custom_objects['dictVectorizer']     # name 'dictVectorizer' should exactly correcpond to saved name 

model_runner = model_ref.to_runner()  # get access to model

svc = bentoml.Service("credit_risk_classifier", runners=[model_runner])  # create service
# "credit_risk_classifier" is a neme of our service, that we create


@svc.api(input=JSON(), output=JSON())
async def classify(application_data):
    vector = dv.transform(application_data)
    prediction = await model_runner.predict.async_run(vector)
    print(prediction)
    result = prediction[0]

    if result > 0.5:
        return {
            "status": "DECLINED"
        }
    elif result > 0.25:
        return {
            "status": "MAYBE"
        }
    else:
        return {
            "status": "APPROVED"
        }
