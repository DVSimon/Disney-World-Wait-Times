#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import math
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold
from sklearn.metrics import f1_score
from scipy import stats
from sklearn.metrics import explained_variance_score
import pickle


# In[2]:


df_initial = pd.read_csv('7_dwarfs_train.csv')
print(df_initial)


# In[3]:


print(df_initial.loc[0])


# In[4]:


print(df_initial.loc[0]['SACTMIN'])


# In[5]:


print(type(df_initial.loc[0]['datetime']))


# In[6]:


for index, row in df_initial.iterrows():
    if math.isnan(row['SPOSTMIN']):
        df_initial.loc[index,'SPOSTMIN'] = df_initial.loc[index, 'SACTMIN']
#     print(row['SPOSTMIN'], row['SACTMIN'])
df_initial = df_initial.drop(columns="SACTMIN")


# In[7]:


df_initial = df_initial[df_initial['SPOSTMIN'] != -999]


# In[8]:


print(df_initial)


# In[9]:


df_initial['Month'] = df_initial.date.str.split('/').str[0]
df_initial['Day'] = df_initial.date.str.split('/').str[1]
df_initial['Year'] = df_initial.date.str.rsplit('/', 1).str[1]
df_initial['Time_char'] = df_initial.datetime.str.split(' ').str[1]
df_initial['Hour'] = df_initial['Time_char'].str.split(':').str[0]
df_initial['Minute'] = df_initial['Time_char'].str.split(':').str[1]
df_initial = df_initial.drop(columns="Time_char")


# In[10]:


print(df_initial)


# In[11]:


df_initial['Month'] = (df_initial['Month']).astype(int)
df_initial['Day'] = (df_initial['Day']).astype(int)
df_initial['Year'] = (df_initial['Year']).astype(int)
df_initial['Hour'] = (df_initial['Hour']).astype(int)
df_initial['Minute'] = (df_initial['Minute']).astype(int)


# In[12]:


print(df_initial)


# In[13]:


print(type(df_initial.loc[0]['SPOSTMIN']))


# In[14]:


df_y = df_initial['SPOSTMIN']


# In[15]:


label_encoder_DOW = LabelEncoder()
DoW_feature = label_encoder_DOW.fit_transform(df_initial.DAYOFWEEK.iloc[:].values)


# In[16]:


# new_col = pd.Series(DoW_feature)
df_initial['DayOfWeek'] = DoW_feature
df_initial = df_initial.drop(columns=["DAYOFWEEK", "date", "datetime", "SPOSTMIN"])


# In[17]:


print(df_initial)


# In[18]:


print(max(df_initial.loc[:,'Month']))


# In[19]:


random_seed = 5
t_s = .20
X_train, X_test, y_train, y_test = train_test_split(df_initial, df_y, test_size = t_s, random_state = random_seed)


# In[20]:


param_grid = {'n_estimators': [100, 200, 300], #random int btwn 100 and 500 - removed
              'learning_rate': stats.uniform(0.01, 0.08), #.01 + loc, range of .01+/-.08
              'max_depth': [2, 4, 6, 8], #tree depths to check
              'colsample_bytree': stats.uniform(0.3, 0.7) #btwn .1 and 1.0    
}
kfold = KFold(n_splits=3, shuffle=True, random_state=random_seed)
model = XGBRegressor(tree_method='gpu_hist')


# In[21]:


rand_search = RandomizedSearchCV(model, param_distributions = param_grid, scoring = 'explained_variance', n_iter = 3, verbose = 10, cv=kfold)
rand_result = rand_search.fit(X_train, y_train)
print("Best: %f using %s" % (rand_result.best_score_, rand_result.best_params_))
best_XGB_estimator = rand_result.best_estimator_
pickle.dump(best_XGB_estimator, open("xgb_dwarves.pkl", 'wb'))


# In[22]:


xgb = XGBRegressor(n_estimators=300, learning_rate=0.08, gamma=0, subsample=0.75, colsample_bytree=1, max_depth=7)
xgb.fit(X_train,y_train)


# In[23]:


predictions = xgb.predict(X_test)
print(explained_variance_score(predictions,y_test))


# In[24]:


# pickle.dump(xgb, open('xgb_dwarves_nonsearch.pkl','wb'))


# In[25]:


print(type(X_test))


# In[26]:


print(type(X_test.iloc[0]))


# In[27]:


print(X_test)


# In[28]:


model = pickle.load(open('xgb_dwarves.pkl','rb'))
month = 6
day = 4
year = 2013
hour = 9
minute = 0
dayofweek = 5
data = [[month, day, year, hour, minute, dayofweek]]
print(data)


# In[29]:


input_df = pd.DataFrame(data, columns =['Month','Day','Year','Hour','Minute','DayOfWeek'])
print(input_df)


# In[31]:


prediction = model.predict(input_df)


# In[32]:


print(prediction)


# In[33]:


df_initial = pd.read_csv('alien_saucers.csv')
for index, row in df_initial.iterrows():
    if math.isnan(row['SPOSTMIN']):
        df_initial.loc[index,'SPOSTMIN'] = df_initial.loc[index, 'SACTMIN']
#     print(row['SPOSTMIN'], row['SACTMIN'])
df_initial = df_initial.drop(columns="SACTMIN")
df_initial = df_initial[df_initial['SPOSTMIN'] != -999]
df_initial['Month'] = df_initial.date.str.split('/').str[0]
df_initial['Day'] = df_initial.date.str.split('/').str[1]
df_initial['Year'] = df_initial.date.str.rsplit('/', 1).str[1]
df_initial['Time_char'] = df_initial.datetime.str.split(' ').str[1]
df_initial['Hour'] = df_initial['Time_char'].str.split(':').str[0]
df_initial['Minute'] = df_initial['Time_char'].str.split(':').str[1]
df_initial = df_initial.drop(columns="Time_char")
df_initial['Month'] = (df_initial['Month']).astype(int)
df_initial['Day'] = (df_initial['Day']).astype(int)
df_initial['Year'] = (df_initial['Year']).astype(int)
df_initial['Hour'] = (df_initial['Hour']).astype(int)
df_initial['Minute'] = (df_initial['Minute']).astype(int)
df_y = df_initial['SPOSTMIN']
label_encoder_DOW = LabelEncoder()
DoW_feature = label_encoder_DOW.fit_transform(df_initial.DAYOFWEEK.iloc[:].values)
# new_col = pd.Series(DoW_feature)
df_initial['DayOfWeek'] = DoW_feature
df_initial = df_initial.drop(columns=["DAYOFWEEK", "date", "datetime", "SPOSTMIN"])
random_seed = 5
t_s = .20
X_train, X_test, y_train, y_test = train_test_split(df_initial, df_y, test_size = t_s, random_state = random_seed)
param_grid = {'n_estimators': [100, 200, 300], #random int btwn 100 and 500 - removed
              'learning_rate': stats.uniform(0.01, 0.08), #.01 + loc, range of .01+/-.08
              'max_depth': [2, 4, 6, 8], #tree depths to check
              'colsample_bytree': stats.uniform(0.3, 0.7) #btwn .1 and 1.0    
}
kfold = KFold(n_splits=3, shuffle=True, random_state=random_seed)
model = XGBRegressor(tree_method='gpu_hist')
rand_search = RandomizedSearchCV(model, param_distributions = param_grid, scoring = 'explained_variance', n_iter = 3, verbose = 10, cv=kfold)
rand_result = rand_search.fit(X_train, y_train)
print("Best: %f using %s" % (rand_result.best_score_, rand_result.best_params_))
best_XGB_estimator = rand_result.best_estimator_
pickle.dump(best_XGB_estimator, open("xgb_alien_saucers.pkl", 'wb'))


# In[34]:


df_initial = pd.read_csv('dinosaur.csv')
for index, row in df_initial.iterrows():
    if math.isnan(row['SPOSTMIN']):
        df_initial.loc[index,'SPOSTMIN'] = df_initial.loc[index, 'SACTMIN']
#     print(row['SPOSTMIN'], row['SACTMIN'])
df_initial = df_initial.drop(columns="SACTMIN")
df_initial = df_initial[df_initial['SPOSTMIN'] != -999]
df_initial['Month'] = df_initial.date.str.split('/').str[0]
df_initial['Day'] = df_initial.date.str.split('/').str[1]
df_initial['Year'] = df_initial.date.str.rsplit('/', 1).str[1]
df_initial['Time_char'] = df_initial.datetime.str.split(' ').str[1]
df_initial['Hour'] = df_initial['Time_char'].str.split(':').str[0]
df_initial['Minute'] = df_initial['Time_char'].str.split(':').str[1]
df_initial = df_initial.drop(columns="Time_char")
df_initial['Month'] = (df_initial['Month']).astype(int)
df_initial['Day'] = (df_initial['Day']).astype(int)
df_initial['Year'] = (df_initial['Year']).astype(int)
df_initial['Hour'] = (df_initial['Hour']).astype(int)
df_initial['Minute'] = (df_initial['Minute']).astype(int)
df_y = df_initial['SPOSTMIN']
label_encoder_DOW = LabelEncoder()
DoW_feature = label_encoder_DOW.fit_transform(df_initial.DAYOFWEEK.iloc[:].values)
# new_col = pd.Series(DoW_feature)
df_initial['DayOfWeek'] = DoW_feature
df_initial = df_initial.drop(columns=["DAYOFWEEK", "date", "datetime", "SPOSTMIN"])
random_seed = 5
t_s = .20
X_train, X_test, y_train, y_test = train_test_split(df_initial, df_y, test_size = t_s, random_state = random_seed)
param_grid = {'n_estimators': [100, 200, 300], #random int btwn 100 and 500 - removed
              'learning_rate': stats.uniform(0.01, 0.08), #.01 + loc, range of .01+/-.08
              'max_depth': [2, 4, 6, 8], #tree depths to check
              'colsample_bytree': stats.uniform(0.3, 0.7) #btwn .1 and 1.0    
}
kfold = KFold(n_splits=3, shuffle=True, random_state=random_seed)
model = XGBRegressor(tree_method='gpu_hist')
rand_search = RandomizedSearchCV(model, param_distributions = param_grid, scoring = 'explained_variance', n_iter = 3, verbose = 10, cv=kfold)
rand_result = rand_search.fit(X_train, y_train)
print("Best: %f using %s" % (rand_result.best_score_, rand_result.best_params_))
best_XGB_estimator = rand_result.best_estimator_
pickle.dump(best_XGB_estimator, open("xgb_dinosaur.pkl", 'wb'))


# In[35]:


df_initial = pd.read_csv('expedition_everest.csv')
for index, row in df_initial.iterrows():
    if math.isnan(row['SPOSTMIN']):
        df_initial.loc[index,'SPOSTMIN'] = df_initial.loc[index, 'SACTMIN']
#     print(row['SPOSTMIN'], row['SACTMIN'])
df_initial = df_initial.drop(columns="SACTMIN")
df_initial = df_initial[df_initial['SPOSTMIN'] != -999]
df_initial['Month'] = df_initial.date.str.split('/').str[0]
df_initial['Day'] = df_initial.date.str.split('/').str[1]
df_initial['Year'] = df_initial.date.str.rsplit('/', 1).str[1]
df_initial['Time_char'] = df_initial.datetime.str.split(' ').str[1]
df_initial['Hour'] = df_initial['Time_char'].str.split(':').str[0]
df_initial['Minute'] = df_initial['Time_char'].str.split(':').str[1]
df_initial = df_initial.drop(columns="Time_char")
df_initial['Month'] = (df_initial['Month']).astype(int)
df_initial['Day'] = (df_initial['Day']).astype(int)
df_initial['Year'] = (df_initial['Year']).astype(int)
df_initial['Hour'] = (df_initial['Hour']).astype(int)
df_initial['Minute'] = (df_initial['Minute']).astype(int)
df_y = df_initial['SPOSTMIN']
label_encoder_DOW = LabelEncoder()
DoW_feature = label_encoder_DOW.fit_transform(df_initial.DAYOFWEEK.iloc[:].values)
# new_col = pd.Series(DoW_feature)
df_initial['DayOfWeek'] = DoW_feature
df_initial = df_initial.drop(columns=["DAYOFWEEK", "date", "datetime", "SPOSTMIN"])
random_seed = 5
t_s = .20
X_train, X_test, y_train, y_test = train_test_split(df_initial, df_y, test_size = t_s, random_state = random_seed)
param_grid = {'n_estimators': [100, 200, 300], #random int btwn 100 and 500 - removed
              'learning_rate': stats.uniform(0.01, 0.08), #.01 + loc, range of .01+/-.08
              'max_depth': [2, 4, 6, 8], #tree depths to check
              'colsample_bytree': stats.uniform(0.3, 0.7) #btwn .1 and 1.0    
}
kfold = KFold(n_splits=3, shuffle=True, random_state=random_seed)
model = XGBRegressor(tree_method='gpu_hist')
rand_search = RandomizedSearchCV(model, param_distributions = param_grid, scoring = 'explained_variance', n_iter = 3, verbose = 10, cv=kfold)
rand_result = rand_search.fit(X_train, y_train)
print("Best: %f using %s" % (rand_result.best_score_, rand_result.best_params_))
best_XGB_estimator = rand_result.best_estimator_
pickle.dump(best_XGB_estimator, open("xgb_expedition_everest.pkl", 'wb'))


# In[36]:


df_initial = pd.read_csv('flight_of_passage.csv')
for index, row in df_initial.iterrows():
    if math.isnan(row['SPOSTMIN']):
        df_initial.loc[index,'SPOSTMIN'] = df_initial.loc[index, 'SACTMIN']
#     print(row['SPOSTMIN'], row['SACTMIN'])
df_initial = df_initial.drop(columns="SACTMIN")
df_initial = df_initial[df_initial['SPOSTMIN'] != -999]
df_initial['Month'] = df_initial.date.str.split('/').str[0]
df_initial['Day'] = df_initial.date.str.split('/').str[1]
df_initial['Year'] = df_initial.date.str.rsplit('/', 1).str[1]
df_initial['Time_char'] = df_initial.datetime.str.split(' ').str[1]
df_initial['Hour'] = df_initial['Time_char'].str.split(':').str[0]
df_initial['Minute'] = df_initial['Time_char'].str.split(':').str[1]
df_initial = df_initial.drop(columns="Time_char")
df_initial['Month'] = (df_initial['Month']).astype(int)
df_initial['Day'] = (df_initial['Day']).astype(int)
df_initial['Year'] = (df_initial['Year']).astype(int)
df_initial['Hour'] = (df_initial['Hour']).astype(int)
df_initial['Minute'] = (df_initial['Minute']).astype(int)
df_y = df_initial['SPOSTMIN']
label_encoder_DOW = LabelEncoder()
DoW_feature = label_encoder_DOW.fit_transform(df_initial.DAYOFWEEK.iloc[:].values)
# new_col = pd.Series(DoW_feature)
df_initial['DayOfWeek'] = DoW_feature
df_initial = df_initial.drop(columns=["DAYOFWEEK", "date", "datetime", "SPOSTMIN"])
random_seed = 5
t_s = .20
X_train, X_test, y_train, y_test = train_test_split(df_initial, df_y, test_size = t_s, random_state = random_seed)
param_grid = {'n_estimators': [100, 200, 300], #random int btwn 100 and 500 - removed
              'learning_rate': stats.uniform(0.01, 0.08), #.01 + loc, range of .01+/-.08
              'max_depth': [2, 4, 6, 8], #tree depths to check
              'colsample_bytree': stats.uniform(0.3, 0.7) #btwn .1 and 1.0    
}
kfold = KFold(n_splits=3, shuffle=True, random_state=random_seed)
model = XGBRegressor(tree_method='gpu_hist')
rand_search = RandomizedSearchCV(model, param_distributions = param_grid, scoring = 'explained_variance', n_iter = 3, verbose = 10, cv=kfold)
rand_result = rand_search.fit(X_train, y_train)
print("Best: %f using %s" % (rand_result.best_score_, rand_result.best_params_))
best_XGB_estimator = rand_result.best_estimator_
pickle.dump(best_XGB_estimator, open("xgb_flight_of_passage.pkl", 'wb'))


# In[37]:


df_initial = pd.read_csv('kilimanjaro_safaris.csv')
for index, row in df_initial.iterrows():
    if math.isnan(row['SPOSTMIN']):
        df_initial.loc[index,'SPOSTMIN'] = df_initial.loc[index, 'SACTMIN']
#     print(row['SPOSTMIN'], row['SACTMIN'])
df_initial = df_initial.drop(columns="SACTMIN")
df_initial = df_initial[df_initial['SPOSTMIN'] != -999]
df_initial['Month'] = df_initial.date.str.split('/').str[0]
df_initial['Day'] = df_initial.date.str.split('/').str[1]
df_initial['Year'] = df_initial.date.str.rsplit('/', 1).str[1]
df_initial['Time_char'] = df_initial.datetime.str.split(' ').str[1]
df_initial['Hour'] = df_initial['Time_char'].str.split(':').str[0]
df_initial['Minute'] = df_initial['Time_char'].str.split(':').str[1]
df_initial = df_initial.drop(columns="Time_char")
df_initial['Month'] = (df_initial['Month']).astype(int)
df_initial['Day'] = (df_initial['Day']).astype(int)
df_initial['Year'] = (df_initial['Year']).astype(int)
df_initial['Hour'] = (df_initial['Hour']).astype(int)
df_initial['Minute'] = (df_initial['Minute']).astype(int)
df_y = df_initial['SPOSTMIN']
label_encoder_DOW = LabelEncoder()
DoW_feature = label_encoder_DOW.fit_transform(df_initial.DAYOFWEEK.iloc[:].values)
# new_col = pd.Series(DoW_feature)
df_initial['DayOfWeek'] = DoW_feature
df_initial = df_initial.drop(columns=["DAYOFWEEK", "date", "datetime", "SPOSTMIN"])
random_seed = 5
t_s = .20
X_train, X_test, y_train, y_test = train_test_split(df_initial, df_y, test_size = t_s, random_state = random_seed)
param_grid = {'n_estimators': [100, 200, 300], #random int btwn 100 and 500 - removed
              'learning_rate': stats.uniform(0.01, 0.08), #.01 + loc, range of .01+/-.08
              'max_depth': [2, 4, 6, 8], #tree depths to check
              'colsample_bytree': stats.uniform(0.3, 0.7) #btwn .1 and 1.0    
}
kfold = KFold(n_splits=3, shuffle=True, random_state=random_seed)
model = XGBRegressor(tree_method='gpu_hist')
rand_search = RandomizedSearchCV(model, param_distributions = param_grid, scoring = 'explained_variance', n_iter = 3, verbose = 10, cv=kfold)
rand_result = rand_search.fit(X_train, y_train)
print("Best: %f using %s" % (rand_result.best_score_, rand_result.best_params_))
best_XGB_estimator = rand_result.best_estimator_
pickle.dump(best_XGB_estimator, open("xgb_kilimanjaro_safaris.pkl", 'wb'))


# In[38]:


df_initial = pd.read_csv('navi_river.csv')
for index, row in df_initial.iterrows():
    if math.isnan(row['SPOSTMIN']):
        df_initial.loc[index,'SPOSTMIN'] = df_initial.loc[index, 'SACTMIN']
#     print(row['SPOSTMIN'], row['SACTMIN'])
df_initial = df_initial.drop(columns="SACTMIN")
df_initial = df_initial[df_initial['SPOSTMIN'] != -999]
df_initial['Month'] = df_initial.date.str.split('/').str[0]
df_initial['Day'] = df_initial.date.str.split('/').str[1]
df_initial['Year'] = df_initial.date.str.rsplit('/', 1).str[1]
df_initial['Time_char'] = df_initial.datetime.str.split(' ').str[1]
df_initial['Hour'] = df_initial['Time_char'].str.split(':').str[0]
df_initial['Minute'] = df_initial['Time_char'].str.split(':').str[1]
df_initial = df_initial.drop(columns="Time_char")
df_initial['Month'] = (df_initial['Month']).astype(int)
df_initial['Day'] = (df_initial['Day']).astype(int)
df_initial['Year'] = (df_initial['Year']).astype(int)
df_initial['Hour'] = (df_initial['Hour']).astype(int)
df_initial['Minute'] = (df_initial['Minute']).astype(int)
df_y = df_initial['SPOSTMIN']
label_encoder_DOW = LabelEncoder()
DoW_feature = label_encoder_DOW.fit_transform(df_initial.DAYOFWEEK.iloc[:].values)
# new_col = pd.Series(DoW_feature)
df_initial['DayOfWeek'] = DoW_feature
df_initial = df_initial.drop(columns=["DAYOFWEEK", "date", "datetime", "SPOSTMIN"])
random_seed = 5
t_s = .20
X_train, X_test, y_train, y_test = train_test_split(df_initial, df_y, test_size = t_s, random_state = random_seed)
param_grid = {'n_estimators': [100, 200, 300], #random int btwn 100 and 500 - removed
              'learning_rate': stats.uniform(0.01, 0.08), #.01 + loc, range of .01+/-.08
              'max_depth': [2, 4, 6, 8], #tree depths to check
              'colsample_bytree': stats.uniform(0.3, 0.7) #btwn .1 and 1.0    
}
kfold = KFold(n_splits=3, shuffle=True, random_state=random_seed)
model = XGBRegressor(tree_method='gpu_hist')
rand_search = RandomizedSearchCV(model, param_distributions = param_grid, scoring = 'explained_variance', n_iter = 3, verbose = 10, cv=kfold)
rand_result = rand_search.fit(X_train, y_train)
print("Best: %f using %s" % (rand_result.best_score_, rand_result.best_params_))
best_XGB_estimator = rand_result.best_estimator_
pickle.dump(best_XGB_estimator, open("xgb_navi_river.pkl", 'wb'))


# In[39]:


df_initial = pd.read_csv('pirates_of_caribbean.csv')
for index, row in df_initial.iterrows():
    if math.isnan(row['SPOSTMIN']):
        df_initial.loc[index,'SPOSTMIN'] = df_initial.loc[index, 'SACTMIN']
#     print(row['SPOSTMIN'], row['SACTMIN'])
df_initial = df_initial.drop(columns="SACTMIN")
df_initial = df_initial[df_initial['SPOSTMIN'] != -999]
df_initial['Month'] = df_initial.date.str.split('/').str[0]
df_initial['Day'] = df_initial.date.str.split('/').str[1]
df_initial['Year'] = df_initial.date.str.rsplit('/', 1).str[1]
df_initial['Time_char'] = df_initial.datetime.str.split(' ').str[1]
df_initial['Hour'] = df_initial['Time_char'].str.split(':').str[0]
df_initial['Minute'] = df_initial['Time_char'].str.split(':').str[1]
df_initial = df_initial.drop(columns="Time_char")
df_initial['Month'] = (df_initial['Month']).astype(int)
df_initial['Day'] = (df_initial['Day']).astype(int)
df_initial['Year'] = (df_initial['Year']).astype(int)
df_initial['Hour'] = (df_initial['Hour']).astype(int)
df_initial['Minute'] = (df_initial['Minute']).astype(int)
df_y = df_initial['SPOSTMIN']
label_encoder_DOW = LabelEncoder()
DoW_feature = label_encoder_DOW.fit_transform(df_initial.DAYOFWEEK.iloc[:].values)
# new_col = pd.Series(DoW_feature)
df_initial['DayOfWeek'] = DoW_feature
df_initial = df_initial.drop(columns=["DAYOFWEEK", "date", "datetime", "SPOSTMIN"])
random_seed = 5
t_s = .20
X_train, X_test, y_train, y_test = train_test_split(df_initial, df_y, test_size = t_s, random_state = random_seed)
param_grid = {'n_estimators': [100, 200, 300], #random int btwn 100 and 500 - removed
              'learning_rate': stats.uniform(0.01, 0.08), #.01 + loc, range of .01+/-.08
              'max_depth': [2, 4, 6, 8], #tree depths to check
              'colsample_bytree': stats.uniform(0.3, 0.7) #btwn .1 and 1.0    
}
kfold = KFold(n_splits=3, shuffle=True, random_state=random_seed)
model = XGBRegressor(tree_method='gpu_hist')
rand_search = RandomizedSearchCV(model, param_distributions = param_grid, scoring = 'explained_variance', n_iter = 3, verbose = 10, cv=kfold)
rand_result = rand_search.fit(X_train, y_train)
print("Best: %f using %s" % (rand_result.best_score_, rand_result.best_params_))
best_XGB_estimator = rand_result.best_estimator_
pickle.dump(best_XGB_estimator, open("xgb_pirates_of_caribbean.pkl", 'wb'))


# In[40]:


df_initial = pd.read_csv('rock_n_rollercoaster.csv')
for index, row in df_initial.iterrows():
    if math.isnan(row['SPOSTMIN']):
        df_initial.loc[index,'SPOSTMIN'] = df_initial.loc[index, 'SACTMIN']
#     print(row['SPOSTMIN'], row['SACTMIN'])
df_initial = df_initial.drop(columns="SACTMIN")
df_initial = df_initial[df_initial['SPOSTMIN'] != -999]
df_initial['Month'] = df_initial.date.str.split('/').str[0]
df_initial['Day'] = df_initial.date.str.split('/').str[1]
df_initial['Year'] = df_initial.date.str.rsplit('/', 1).str[1]
df_initial['Time_char'] = df_initial.datetime.str.split(' ').str[1]
df_initial['Hour'] = df_initial['Time_char'].str.split(':').str[0]
df_initial['Minute'] = df_initial['Time_char'].str.split(':').str[1]
df_initial = df_initial.drop(columns="Time_char")
df_initial['Month'] = (df_initial['Month']).astype(int)
df_initial['Day'] = (df_initial['Day']).astype(int)
df_initial['Year'] = (df_initial['Year']).astype(int)
df_initial['Hour'] = (df_initial['Hour']).astype(int)
df_initial['Minute'] = (df_initial['Minute']).astype(int)
df_y = df_initial['SPOSTMIN']
label_encoder_DOW = LabelEncoder()
DoW_feature = label_encoder_DOW.fit_transform(df_initial.DAYOFWEEK.iloc[:].values)
# new_col = pd.Series(DoW_feature)
df_initial['DayOfWeek'] = DoW_feature
df_initial = df_initial.drop(columns=["DAYOFWEEK", "date", "datetime", "SPOSTMIN"])
random_seed = 5
t_s = .20
X_train, X_test, y_train, y_test = train_test_split(df_initial, df_y, test_size = t_s, random_state = random_seed)
param_grid = {'n_estimators': [100, 200, 300], #random int btwn 100 and 500 - removed
              'learning_rate': stats.uniform(0.01, 0.08), #.01 + loc, range of .01+/-.08
              'max_depth': [2, 4, 6, 8], #tree depths to check
              'colsample_bytree': stats.uniform(0.3, 0.7) #btwn .1 and 1.0    
}
kfold = KFold(n_splits=3, shuffle=True, random_state=random_seed)
model = XGBRegressor(tree_method='gpu_hist')
rand_search = RandomizedSearchCV(model, param_distributions = param_grid, scoring = 'explained_variance', n_iter = 3, verbose = 10, cv=kfold)
rand_result = rand_search.fit(X_train, y_train)
print("Best: %f using %s" % (rand_result.best_score_, rand_result.best_params_))
best_XGB_estimator = rand_result.best_estimator_
pickle.dump(best_XGB_estimator, open("xgb_rock_n_rollercoaster.pkl", 'wb'))


# In[41]:


df_initial = pd.read_csv('slinky_dog.csv')
for index, row in df_initial.iterrows():
    if math.isnan(row['SPOSTMIN']):
        df_initial.loc[index,'SPOSTMIN'] = df_initial.loc[index, 'SACTMIN']
#     print(row['SPOSTMIN'], row['SACTMIN'])
df_initial = df_initial.drop(columns="SACTMIN")
df_initial = df_initial[df_initial['SPOSTMIN'] != -999]
df_initial['Month'] = df_initial.date.str.split('/').str[0]
df_initial['Day'] = df_initial.date.str.split('/').str[1]
df_initial['Year'] = df_initial.date.str.rsplit('/', 1).str[1]
df_initial['Time_char'] = df_initial.datetime.str.split(' ').str[1]
df_initial['Hour'] = df_initial['Time_char'].str.split(':').str[0]
df_initial['Minute'] = df_initial['Time_char'].str.split(':').str[1]
df_initial = df_initial.drop(columns="Time_char")
df_initial['Month'] = (df_initial['Month']).astype(int)
df_initial['Day'] = (df_initial['Day']).astype(int)
df_initial['Year'] = (df_initial['Year']).astype(int)
df_initial['Hour'] = (df_initial['Hour']).astype(int)
df_initial['Minute'] = (df_initial['Minute']).astype(int)
df_y = df_initial['SPOSTMIN']
label_encoder_DOW = LabelEncoder()
DoW_feature = label_encoder_DOW.fit_transform(df_initial.DAYOFWEEK.iloc[:].values)
# new_col = pd.Series(DoW_feature)
df_initial['DayOfWeek'] = DoW_feature
df_initial = df_initial.drop(columns=["DAYOFWEEK", "date", "datetime", "SPOSTMIN"])
random_seed = 5
t_s = .20
X_train, X_test, y_train, y_test = train_test_split(df_initial, df_y, test_size = t_s, random_state = random_seed)
param_grid = {'n_estimators': [100, 200, 300], #random int btwn 100 and 500 - removed
              'learning_rate': stats.uniform(0.01, 0.08), #.01 + loc, range of .01+/-.08
              'max_depth': [2, 4, 6, 8], #tree depths to check
              'colsample_bytree': stats.uniform(0.3, 0.7) #btwn .1 and 1.0    
}
kfold = KFold(n_splits=3, shuffle=True, random_state=random_seed)
model = XGBRegressor(tree_method='gpu_hist')
rand_search = RandomizedSearchCV(model, param_distributions = param_grid, scoring = 'explained_variance', n_iter = 3, verbose = 10, cv=kfold)
rand_result = rand_search.fit(X_train, y_train)
print("Best: %f using %s" % (rand_result.best_score_, rand_result.best_params_))
best_XGB_estimator = rand_result.best_estimator_
pickle.dump(best_XGB_estimator, open("xgb_slinky_dog.pkl", 'wb'))


# In[42]:


df_initial = pd.read_csv('soarin.csv')
for index, row in df_initial.iterrows():
    if math.isnan(row['SPOSTMIN']):
        df_initial.loc[index,'SPOSTMIN'] = df_initial.loc[index, 'SACTMIN']
#     print(row['SPOSTMIN'], row['SACTMIN'])
df_initial = df_initial.drop(columns="SACTMIN")
df_initial = df_initial[df_initial['SPOSTMIN'] != -999]
df_initial['Month'] = df_initial.date.str.split('/').str[0]
df_initial['Day'] = df_initial.date.str.split('/').str[1]
df_initial['Year'] = df_initial.date.str.rsplit('/', 1).str[1]
df_initial['Time_char'] = df_initial.datetime.str.split(' ').str[1]
df_initial['Hour'] = df_initial['Time_char'].str.split(':').str[0]
df_initial['Minute'] = df_initial['Time_char'].str.split(':').str[1]
df_initial = df_initial.drop(columns="Time_char")
df_initial['Month'] = (df_initial['Month']).astype(int)
df_initial['Day'] = (df_initial['Day']).astype(int)
df_initial['Year'] = (df_initial['Year']).astype(int)
df_initial['Hour'] = (df_initial['Hour']).astype(int)
df_initial['Minute'] = (df_initial['Minute']).astype(int)
df_y = df_initial['SPOSTMIN']
label_encoder_DOW = LabelEncoder()
DoW_feature = label_encoder_DOW.fit_transform(df_initial.DAYOFWEEK.iloc[:].values)
# new_col = pd.Series(DoW_feature)
df_initial['DayOfWeek'] = DoW_feature
df_initial = df_initial.drop(columns=["DAYOFWEEK", "date", "datetime", "SPOSTMIN"])
random_seed = 5
t_s = .20
X_train, X_test, y_train, y_test = train_test_split(df_initial, df_y, test_size = t_s, random_state = random_seed)
param_grid = {'n_estimators': [100, 200, 300], #random int btwn 100 and 500 - removed
              'learning_rate': stats.uniform(0.01, 0.08), #.01 + loc, range of .01+/-.08
              'max_depth': [2, 4, 6, 8], #tree depths to check
              'colsample_bytree': stats.uniform(0.3, 0.7) #btwn .1 and 1.0    
}
kfold = KFold(n_splits=3, shuffle=True, random_state=random_seed)
model = XGBRegressor(tree_method='gpu_hist')
rand_search = RandomizedSearchCV(model, param_distributions = param_grid, scoring = 'explained_variance', n_iter = 3, verbose = 10, cv=kfold)
rand_result = rand_search.fit(X_train, y_train)
print("Best: %f using %s" % (rand_result.best_score_, rand_result.best_params_))
best_XGB_estimator = rand_result.best_estimator_
pickle.dump(best_XGB_estimator, open("xgb_soarin.pkl", 'wb'))


# In[43]:


df_initial = pd.read_csv('spaceship_earth.csv')
for index, row in df_initial.iterrows():
    if math.isnan(row['SPOSTMIN']):
        df_initial.loc[index,'SPOSTMIN'] = df_initial.loc[index, 'SACTMIN']
#     print(row['SPOSTMIN'], row['SACTMIN'])
df_initial = df_initial.drop(columns="SACTMIN")
df_initial = df_initial[df_initial['SPOSTMIN'] != -999]
df_initial['Month'] = df_initial.date.str.split('/').str[0]
df_initial['Day'] = df_initial.date.str.split('/').str[1]
df_initial['Year'] = df_initial.date.str.rsplit('/', 1).str[1]
df_initial['Time_char'] = df_initial.datetime.str.split(' ').str[1]
df_initial['Hour'] = df_initial['Time_char'].str.split(':').str[0]
df_initial['Minute'] = df_initial['Time_char'].str.split(':').str[1]
df_initial = df_initial.drop(columns="Time_char")
df_initial['Month'] = (df_initial['Month']).astype(int)
df_initial['Day'] = (df_initial['Day']).astype(int)
df_initial['Year'] = (df_initial['Year']).astype(int)
df_initial['Hour'] = (df_initial['Hour']).astype(int)
df_initial['Minute'] = (df_initial['Minute']).astype(int)
df_y = df_initial['SPOSTMIN']
label_encoder_DOW = LabelEncoder()
DoW_feature = label_encoder_DOW.fit_transform(df_initial.DAYOFWEEK.iloc[:].values)
# new_col = pd.Series(DoW_feature)
df_initial['DayOfWeek'] = DoW_feature
df_initial = df_initial.drop(columns=["DAYOFWEEK", "date", "datetime", "SPOSTMIN"])
random_seed = 5
t_s = .20
X_train, X_test, y_train, y_test = train_test_split(df_initial, df_y, test_size = t_s, random_state = random_seed)
param_grid = {'n_estimators': [100, 200, 300], #random int btwn 100 and 500 - removed
              'learning_rate': stats.uniform(0.01, 0.08), #.01 + loc, range of .01+/-.08
              'max_depth': [2, 4, 6, 8], #tree depths to check
              'colsample_bytree': stats.uniform(0.3, 0.7) #btwn .1 and 1.0    
}
kfold = KFold(n_splits=3, shuffle=True, random_state=random_seed)
model = XGBRegressor(tree_method='gpu_hist')
rand_search = RandomizedSearchCV(model, param_distributions = param_grid, scoring = 'explained_variance', n_iter = 3, verbose = 10, cv=kfold)
rand_result = rand_search.fit(X_train, y_train)
print("Best: %f using %s" % (rand_result.best_score_, rand_result.best_params_))
best_XGB_estimator = rand_result.best_estimator_
pickle.dump(best_XGB_estimator, open("xgb_spaceship_earth.pkl", 'wb'))


# In[44]:


df_initial = pd.read_csv('splash_mountain.csv')
for index, row in df_initial.iterrows():
    if math.isnan(row['SPOSTMIN']):
        df_initial.loc[index,'SPOSTMIN'] = df_initial.loc[index, 'SACTMIN']
#     print(row['SPOSTMIN'], row['SACTMIN'])
df_initial = df_initial.drop(columns="SACTMIN")
df_initial = df_initial[df_initial['SPOSTMIN'] != -999]
df_initial['Month'] = df_initial.date.str.split('/').str[0]
df_initial['Day'] = df_initial.date.str.split('/').str[1]
df_initial['Year'] = df_initial.date.str.rsplit('/', 1).str[1]
df_initial['Time_char'] = df_initial.datetime.str.split(' ').str[1]
df_initial['Hour'] = df_initial['Time_char'].str.split(':').str[0]
df_initial['Minute'] = df_initial['Time_char'].str.split(':').str[1]
df_initial = df_initial.drop(columns="Time_char")
df_initial['Month'] = (df_initial['Month']).astype(int)
df_initial['Day'] = (df_initial['Day']).astype(int)
df_initial['Year'] = (df_initial['Year']).astype(int)
df_initial['Hour'] = (df_initial['Hour']).astype(int)
df_initial['Minute'] = (df_initial['Minute']).astype(int)
df_y = df_initial['SPOSTMIN']
label_encoder_DOW = LabelEncoder()
DoW_feature = label_encoder_DOW.fit_transform(df_initial.DAYOFWEEK.iloc[:].values)
# new_col = pd.Series(DoW_feature)
df_initial['DayOfWeek'] = DoW_feature
df_initial = df_initial.drop(columns=["DAYOFWEEK", "date", "datetime", "SPOSTMIN"])
random_seed = 5
t_s = .20
X_train, X_test, y_train, y_test = train_test_split(df_initial, df_y, test_size = t_s, random_state = random_seed)
param_grid = {'n_estimators': [100, 200, 300], #random int btwn 100 and 500 - removed
              'learning_rate': stats.uniform(0.01, 0.08), #.01 + loc, range of .01+/-.08
              'max_depth': [2, 4, 6, 8], #tree depths to check
              'colsample_bytree': stats.uniform(0.3, 0.7) #btwn .1 and 1.0    
}
kfold = KFold(n_splits=3, shuffle=True, random_state=random_seed)
model = XGBRegressor(tree_method='gpu_hist')
rand_search = RandomizedSearchCV(model, param_distributions = param_grid, scoring = 'explained_variance', n_iter = 3, verbose = 10, cv=kfold)
rand_result = rand_search.fit(X_train, y_train)
print("Best: %f using %s" % (rand_result.best_score_, rand_result.best_params_))
best_XGB_estimator = rand_result.best_estimator_
pickle.dump(best_XGB_estimator, open("xgb_toy_story_mania.pkl", 'wb'))


# In[ ]:




