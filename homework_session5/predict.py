import pickle

model_file = 'model1.bin'
vect_file = 'dv.bin'

with open(model_file, 'rb') as fm_in:
    model = pickle.load(fm_in)

with open(vect_file, 'rb') as fdv_in:
    dv = pickle.load(fdv_in)

client_features = {"reports": 0, "share": 0.001694, "expenditure": 0.12, "owner": "yes"}

X = dv.transform([client_features])
y_pred = model.predict_proba(X)[0, 1]

print(y_pred)