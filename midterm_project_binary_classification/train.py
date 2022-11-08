import pandas as pd
import numpy as np
import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import mutual_info_score
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import pickle


df = pd.read_csv('udemy_courses.csv', header=0, sep=',')

# # Data cleaning and data preparation

# convert "is_paid" from boolean to categorical variable
df['is_paid'] = df['is_paid'].map({True: 'yes', False: 'no'}) 

# create a column of an age of a course (in days)

df.published_timestamp = pd.to_datetime(df.published_timestamp).dt.date
scrap_date = datetime.datetime(2020, 5, 10).date()
df['age'] = [(scrap_date - y) for y in df['published_timestamp']]
df.age = df.age.astype(str).str.strip('days').astype(int)

# create a column "popularity", which is equal to "num_subscribers/age"

df['popularity'] = df.num_subscribers / df.age

# Drop a long tail after popularity=40

df_extrem_popular = df[df['popularity']>=40]
ind_dropped = df_extrem_popular.index
df.drop(ind_dropped, inplace=True)

# create a list of column names, except "published_timestamp" (as it's replaced with "age"),
# "course_title" and "url" features are also excluded as the course is defined with "course_id" column
# "num_subscribers", "num_reviews" and "age" features are excluded as our business task is to prognose,
# wether course will be popular
list_features = list(df.columns)
list_features.remove('published_timestamp')
list_features.remove('course_title')
list_features.remove('url')
list_features.remove('num_subscribers')
list_features.remove('num_reviews')
list_features.remove('age')
list_features


# # Setting up the validation framework

df_full_train, df_test = train_test_split(df[list_features], test_size=0.2, random_state=42)
df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=42)

df_train = df_train.reset_index(drop=True)
df_val = df_val.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)

y_train = df_train.popularity.values
y_val = df_val.popularity.values
y_test = df_test.popularity.values

del df_train['popularity']
del df_val['popularity']
del df_test['popularity']

# convert 'popularity' to 0-1 values
def target_handle(y):
    popularity_threshold = np.median(y_train)
    y = (y<popularity_threshold).astype(int)
    return y

y_train = target_handle(y_train)
y_val = target_handle(y_val)
y_test = target_handle(y_test)


# # One-hot encoding

dv = DictVectorizer(sparse=False)

train_dict = df_train.to_dict(orient='records')
X_train = dv.fit_transform(train_dict)

val_dict = df_val.to_dict(orient='records')
X_val = dv.transform(val_dict)

# # Training model

rf = RandomForestClassifier(n_estimators=148,
                            max_depth=9,
                            min_samples_leaf=3,
                            random_state=1)
rf.fit(X_train, y_train)

y_pred = rf.predict_proba(X_val)[:, 1]
ras = roc_auc_score(y_val, y_pred)
print('validation roc-auc score =', ras)

# # Final model

df_full_train = df_full_train.reset_index(drop=True)
y_full_train = df_full_train.popularity.values
del df_full_train['popularity']
y_full_train = target_handle(y_full_train)

train_dict = df_full_train.to_dict(orient='records')
X_full_train = dv.fit_transform(train_dict)
test_dict = df_test.to_dict(orient='records')
X_test = dv.transform(test_dict)

rf.fit(X_full_train, y_full_train)
y_pred = rf.predict_proba(X_test)[:, 1]
ras_full = roc_auc_score(y_test, y_pred)
print('test roc-auc score =', ras_full)

# # Saving model

output_file = 'model.bin'
with open(output_file, 'wb') as f_out: 
    pickle.dump((dv, rf), f_out)