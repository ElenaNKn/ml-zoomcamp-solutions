import numpy as np

import bentoml
from bentoml.io import NumpyNdarray

model_ref = bentoml.sklearn.get("mlzoomcamp_homework:jsi67fslz6txydu5")  

model_runner = model_ref.to_runner()  # get access to model

svc = bentoml.Service("credit_risk_classifier_cool", runners=[model_runner]) 

@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
async def classify(application_data):
    prediction = await model_runner.predict.async_run(application_data)
    return prediction