import pickle
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
import streamlit as st 
from datetime import datetime, timedelta

FEATURES = ['hour','dayofweek','quarter','month','dayofyear','dayofmonth','weekofyear']

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

@st.cache_data
def get_data(filename) -> pd.DataFrame:
  df = pd.read_excel(filename)
  df['dateTime']= pd.to_datetime(df['dateTime'])
  df.set_index('dateTime', inplace=True)
  df['activePowerT'] = df['activePowerT'].astype(float)

  return df

def create_future(df) -> pd.DataFrame:

  df = add_lags(df)
  df = create_features(df)

  future = pd.date_range('2024-07-01','2024-07-15',freq ='1h')
  future_df = pd.DataFrame(index=future)
  future_df['isFuture']= True
  df['isFuture']=False
  df_and_future = pd.concat([df,future_df])
  df_and_future = create_features(df_and_future)
  df_and_future = add_lags(df_and_future)
  future_w_features = df_and_future.query('isFuture').copy()

  return future_w_features

@st.cache_resource
def getML_Model():
    pickle_in = open('XGBoost.pkl', 'rb') 
    return pickle.load(pickle_in)


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



def get_recent_data(last_timestamp,df):

    """Generate and return data from last timestamp to now, at most 60 seconds."""
    now = datetime.now()
    if now - last_timestamp > timedelta(seconds=60):
        last_timestamp = now - timedelta(seconds=60)
    sample_time = timedelta(seconds=0.5)  # time between data points
    next_timestamp = last_timestamp + sample_time
    timestamps = np.arange(next_timestamp, now, sample_time)
    sample_values = np.random.randn(len(timestamps), 2)

    data = df[['activePowerT']]
    
    return data



@st.fragment(run_every='0.5s')
def show_latest_data(df):

    last_timestamp = st.session_state.data.index[-1]
    st.session_state.data = pd.concat(
        [st.session_state.data, get_recent_data(last_timestamp,df)]
    )
    st.session_state.data = st.session_state.data[-100:]
    
    st.line_chart(st.session_state.data)





