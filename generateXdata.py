#!/usr/bin/env python
# coding: utf-8

# In[3]:


# IMport dependencies
import pandas as pd
from pandas import set_option
import numpy
import os
import csv

import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

# import required libraries related to xgBoost and sci-kit learn
import xgboost as xgb
from sklearn.metrics import mean_squared_error

# from keras.utils import to_categorical

# import preprocessing from sklearn
from sklearn import preprocessing

# DictVectorizer
from sklearn.feature_extraction import DictVectorizer


def generateX():    

    dataFilePath = "dataforfinalproject"
    filename = "RECS_COMBINED_DATA.csv"
    cols_file = "Final_Columns_withCat.csv"

    # read dataset wih all years combined data
    df_recs = pd.read_csv(os.path.join(dataFilePath, filename), low_memory= False)


    # read the columns from Columns csv
    df_cols = pd.read_csv(os.path.join(dataFilePath, cols_file))
#     df_cols.columns

    # Whittle down the dataset to contain only Features required for modeling - X 
    modelDF = df_recs[df_cols[df_cols.FEATURES_MODEL == "Y"].COLUMN_NAME]
    print(f" X Features shape : {modelDF.shape}")

    y_label = df_recs['TOTALBTU']
    print(f"y label shape : {y_label.shape}")

    ### Prepare Data

    # describe the dataframe that will be used for model
    descrDF = modelDF[df_cols[(df_cols.FEATURES_MODEL == "Y")].COLUMN_NAME].describe()
    
    # transpose to make it easier to obtain columns with values of 99 and <0
    descrDF = descrDF.transpose().reset_index()
#     descrDF
    # obtain column names with values 99. 99 indicates missing or unavailable info. this needs to be replaced with MOde
    cols99_2 = descrDF[(descrDF['max'] == 99.0) | (descrDF['min'] < 0) ]['index'].tolist()
    


    print(f"cols with values as 99 and -2: {cols99_2} \n")

    # print(f"cols with values as -2 : {cols_2} ")


    # For all categorical columns, that have 99 and -2 , replace with Columns Mode value#
    # step 1 - Fill na for thse values of 99 and -2
    # Step 2: Fillna with mode

    # step1 
    modelCopy = modelDF.copy()
    modelDF[cols99_2] = modelDF[cols99_2].applymap(lambda r : None if r in [99,-2] else r)


    #step2 :
    # modelDF[cols99_2].apply(lambda r : modes[r.name])
    modelDF[cols99_2] = modelDF[cols99_2].fillna(modelDF.mode().iloc[0])

    # just for Col EDishw, the values are in -ve  (-9, -8 )so replace it in a separate line
    modelDF['ESDISHW'] = modelDF['ESDISHW'].apply(lambda r : 0 if (r < 0) else r)

    # check if NAN exists
    print(f"Duplicate Count : {modelDF.isnull().values.sum()}")


    modelDF[df_cols[(df_cols.FEATURES_MODEL == "Y") & (df_cols.COLUMN_TYPE == "Categorical")].COLUMN_NAME].describe()

#     descrDF1 = modelDF[df_cols[(df_cols.FEATURES_MODEL == "Y")].COLUMN_NAME].describe()
#     # transpose to make it easier to obtain columns with values of 99 and -2
#     descrDF1 = descrDF1.transpose().reset_index()
# #     descrDF1[descrDF1['min'] < 0] 

    # XGBOOST - Predicting Total Consumption in BTU

    # Drop Price / Cost related Columns as it is only Consumption we are interested in 
    cost_cols = df_cols[(df_cols['COLUMN_NAME'].str.find("DOL") != -1) & (df_cols.FEATURES_MODEL == "Y")].COLUMN_NAME.tolist()
    cost_cols

    modelDF[cost_cols].head()

    modelDF_BTU = modelDF.copy()
    modelDF_BTU.drop(cost_cols, axis = 1, inplace = True)
    print(modelDF_BTU.shape)
    modelDF_BTU.columns

#     # assign target or output to y
#     y = modelDF_BTU['TOTALBTU']
#     print(f"shape of y is {y.shape}")

    # and drop TOTAL BTU from X set
    X = modelDF_BTU.drop(['TOTALBTU'], axis = 1)
    print(f"shape of X is {X.shape}")

    ### Apply dict vectorizer 

    X_dict = X.to_dict(orient = "records")
    X_dict

    # instantiate a Dictvectorizer object for X
    dv_X = DictVectorizer(sparse=False) 
    # sparse = False makes the output is not a sparse matrix

    # apply dv_X on X_dict
    X_encoded = dv_X.fit_transform(X_dict)
    # show X_encoded
    return X_encoded


# In[4]:


generateX()


# In[ ]:




