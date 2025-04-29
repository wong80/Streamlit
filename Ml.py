# imports
import pickle
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
import streamlit as st 
from datetime import datetime, timedelta
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
from time import sleep
FEATURES = ['hour','dayofweek','quarter','month','dayofyear','dayofmonth','weekofyear']

# Lag Features
def add_lags(df):
  df = df.copy()
  target_map = df['activePowerT'].to_dict()
  df['lag1'] = (df.index-pd.Timedelta('1 days')).map(target_map)
  df['lag2'] = (df.index-pd.Timedelta('2 days')).map(target_map)
  df['lag3'] = (df.index-pd.Timedelta('3 days')).map(target_map)
  df['lag4'] = (df.index-pd.Timedelta('4 days')).map(target_map)
  target_mapAA = df['activePowerA'].to_dict()
  target_mapCA = df['currentA'].to_dict()

  df['activePowerA_lag1']=(df.index-pd.Timedelta('1 days')).map(target_mapAA)
  df['currentA_lag1']=(df.index-pd.Timedelta('1 days')).map(target_mapCA)
  return df

# Feature Create
def create_features(df, label=None):
    """
    Creates time series features from datetime index
    """
    df=df.copy()
    df['hour'] = df.index.hour
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day
    df['weekofyear'] = df.index.isocalendar().week
    return df

# Obtain Data form xlsx file 
@st.cache_data
def get_data(filename) -> pd.DataFrame:
  df = pd.read_excel(filename)
  df['dateTime']= pd.to_datetime(df['dateTime'])
  df.set_index('dateTime', inplace=True)
  df['activePowerT'] = df['activePowerT'].astype(float)

  return df

# Create Future Dataframe
def create_future(df) -> pd.DataFrame:

  df = add_lags(df)
  df = create_features(df)

  future = pd.date_range('2024-12-07','2024-12-21',freq ='1h')
  future_df = pd.DataFrame(index=future)
  future_df['isFuture']= True
  df['isFuture']=False
  df_and_future = pd.concat([df,future_df])
  df_and_future = create_features(df_and_future)
  df_and_future = add_lags(df_and_future)
  future_w_features = df_and_future.query('isFuture').copy()

  return future_w_features

# Extract ML Model
@st.cache_resource
def getML_Model():
    pickle_in = open('XGBoost.pkl', 'rb') 
    return pickle.load(pickle_in)

# Make prediction 
def predict(future_w_features,classifier):
  future_w_features['pred']= classifier.predict(future_w_features[FEATURES])


  fig, ax = plt.subplots(figsize=(13,8))
  future_w_features['pred'].plot(figsize=(10,5),
                                ms=1,
                                lw=1,
                                title='Future Predictions',
                                ax=ax                   
                                )
  plt.show()



def get_recent_data(df,i=[0]):

    """Generate and return data from last timestamp to now, at most 60 seconds."""
    i[0]+=1
    df = df.iloc[:i[0]]
      

    data = df[['activePowerA','activePowerB','activePowerC']]

    return data



@st.fragment(run_every='0.1s')
def show_latest_data(df):

    last_timestamp = st.session_state.data.index[-1]
    st.session_state.data = pd.concat(
        [st.session_state.data, get_recent_data(df)]
    )
    st.session_state.data = st.session_state.data[-30:]
    
    st.line_chart(st.session_state.data,x_label="Time",y_label="ActivePower (kW)")


@st.fragment(run_every="1s")
def RTC():
    now = datetime.now()
    current_time = now.strftime("%D %H:%M:%S")
    
    st.metric(
        label="Current Time",
        value =current_time
    )

# Data Prepropcessing for ML
def preprocessing(df):
  df.reset_index(inplace=True)
  df['dateTime']= pd.to_datetime(df['dateTime'])
  df.set_index('dateTime')
  
  

  le = LabelEncoder()
  df['dateTime'] = le.fit_transform(df['dateTime'])
  df.drop(0,axis=1,inplace=True)

  imputer = KNNImputer(n_neighbors=5)
  df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns, index=df.index)
  df_imputed['dateTime'] = df_imputed['dateTime'].round().astype(int)
  df_imputed['dateTime'] = le.inverse_transform(df_imputed['dateTime'])
  print(df_imputed.head())
  df = df_imputed.groupby(pd.Grouper(key='dateTime', axis=0, freq='h',dropna=False)).mean(numeric_only =True)
  df['activePowerT']  = df['power1']+df['power2']+df['power3']
  
  # Create a full hourly range from 12 AM to 11 PM
  full_hours = pd.date_range("2025-03-17 00:00:00", "2025-04-17 23:00:00", freq='h')

  # Reindex to fill missing timestamps with NaN
  df_full = df.reindex(full_hours)
  df_full.fillna(0,inplace=True)
  return df_full

def preprocessing(df):
  df.reset_index(inplace=True)
  df['dateTime']= pd.to_datetime(df['dateTime'])
  df.set_index('dateTime')
  
  

  le = LabelEncoder()
  df['dateTime'] = le.fit_transform(df['dateTime'])
  df.drop(0,axis=1,inplace=True)

  imputer = KNNImputer(n_neighbors=5)
  df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns, index=df.index)
  df_imputed['dateTime'] = df_imputed['dateTime'].round().astype(int)
  df_imputed['dateTime'] = le.inverse_transform(df_imputed['dateTime'])
  print(df_imputed.head())
  df = df_imputed.groupby(pd.Grouper(key='dateTime', axis=0, freq='h',dropna=False)).mean(numeric_only =True)
  df['activePowerT']  = df['power1']+df['power2']+df['power3']
  
  # Create a full hourly range from 12 AM to 11 PM
  full_hours = pd.date_range("2025-03-17 00:00:00", "2025-04-17 23:00:00", freq='h')

  # Reindex to fill missing timestamps with NaN
  df_full = df.reindex(full_hours)
  df_full.fillna(0,inplace=True)
  return df_full


