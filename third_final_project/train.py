import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error



def mape_calc(y_val, y_pred):
    mape = {}

    for i in range(4):
        mape[list_targets[i]] = mean_absolute_percentage_error(y_val[:, i], y_pred[:, i])
    return mape


df = pd.read_csv('mechanical_properties_low-alloy_steels.csv', header=0, sep=',')

# Data preparation

df.columns = df.columns.str.lower().str.lstrip()
df.columns = df.columns.str.replace('+', 'and', regex=True).str.replace('°c', 'celcius', regex=True)
df.columns = df.columns.str.replace('0.2% ', '', regex=True).str.replace('%', 'perc', regex=True)
df.columns = df.columns.str.replace(' ', '_').str.replace('+', 'and', regex=True)
df.columns = df.columns.str.replace('(', '', regex=True).str.replace(')', '', regex=True)
df.columns = df.columns.str.lower().str.replace('ta', 'ti')
del df['ceq']
del df['alloy_code']

# Outliers deleting

tensile_strength_outlier = df[df['tensile_strength_mpa']>1000]
ind_dropped = tensile_strength_outlier.index
df.drop(ind_dropped, inplace=True)


# Setting up the validation framework

list_features = [
    'c', 'si', 'mn', 'p', 's', 'ni', 'cr',
    'mo', 'cu', 'v', 'al', 'n',
    'nb_and_ti', 'temperature_celcius'
    ]

list_targets = [
    'proof_stress_mpa', 'tensile_strength_mpa',
    'elongation_perc', 'reduction_in_area_perc'
    ]


df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=42)

df_train = df_train.reset_index(drop=True)
df_val = df_val.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)

dy_train = df_train[list_targets]
dy_val = df_val[list_targets]
dy_test = df_test[list_targets]

df_train.drop(list_targets, axis=1, inplace=True)
df_val.drop(list_targets, axis=1, inplace=True)
df_test.drop(list_targets, axis=1, inplace=True)

y_val = dy_val.to_numpy()
y_test = dy_test.to_numpy()

# Model creation

rf = RandomForestRegressor(n_estimators=33,
                                max_depth=13,
                                min_samples_leaf=1,
                                random_state=1)
rf.fit(df_train, dy_train)

y_pred = rf.predict(df_val)

mape = mape_calc(y_val, y_pred)
mean_mape = sum(list(mape.values())) / 4
print('Mean MAPE for random forest model = %.4f' % (mean_mape))

# Model training on train+val dataset

df_full_train = df_full_train.reset_index(drop=True)
dy_full_train = df_full_train[list_targets]
df_full_train.drop(list_targets, axis=1, inplace=True)

rf = RandomForestRegressor(n_estimators=33,
                                max_depth=13,
                                min_samples_leaf=1,
                                random_state=1)
rf.fit(df_full_train, dy_full_train)

y_pred = rf.predict(df_test)
y_test = dy_test.to_numpy()

mape = mape_calc(y_test, y_pred)
mean_mape = sum(list(mape.values())) / 4
print('Mean MAPE for random forest model on test dataset = %.4f' % (mean_mape))

# Saving the final model

import pickle

output_file = 'model.bin'

with open(output_file, 'wb') as f_out: 
    pickle.dump(rf, f_out)