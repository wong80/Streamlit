
import streamlit as st 
import plotly.express as px  # interactive charts
import plotly.graph_objects as go
import Ml
import firebase
import time
from datetime import datetime, timedelta


# Page Config
st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)


# Dataframe Preparation
df = Ml.get_data("Combined.xlsx")
future_w_features = Ml.create_future(df)

# Import Machine Learning Model
classifier = Ml.getML_Model()

# Plot Predictions 
Ml.predict(future_w_features,classifier)

# dashboard title
st.title(r"$\textsf{\large Energy Consumption Monitoring and Prediction System}$")



data_tab, prediction_tab, realtime_tab= st.tabs(["Data","Predictions","Real Time"])



# Data Display Tab
with data_tab:
    # top-level filters
    month_filter = st.selectbox(r"$\textsf{\large Choose the Month:}$", ("January","February","March","April","May","June","July","August","September","October","November","December"))

    # df filter
    match month_filter:
        case "January":
            month_no = 1
        case "February":
            month_no = 2
        case "March":
            month_no = 3
        case "April":
            month_no = 4
        case "May":
            month_no = 5
        case "June":
            month_no = 6
        case "July":
            month_no = 7
        case "August":
            month_no = 8
        case "September":
            month_no = 9
        case "October":
            month_no = 10
        case "November":
            month_no = 11
        case "December":
            month_no = 12
    
    # creating a single-element container
    month_df = df.loc[df.index.month == month_no]
    # create three columns
    kpi1, kpi2= st.columns(2)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="Average Hourly Power Consumption",
        value= f"{round(month_df['activePowerT'].mean(),2)} kW"

    )
    
    kpi2.metric(
        label="Average Hourly Current",
        value= f"{round(month_df['currentA'].mean(),2)} A"

    )   

    st.metric(
        label="Last Recorded Data",
        value = str(df.index.max())
    )
    


    st.markdown(r"$\textsf{\Large Hourly Power Consumption Data}$")   
    fig = px.line(month_df, 
                x=month_df.index, 
                y="activePowerT",
                labels=dict(dateTime="Date",activePowerT="Active Power (kW)"),
                )

    st.write(fig)

    st.markdown(r"$\textsf{\Large Daily Power Consumption Data}$")  

    daily = month_df.iloc[:,:].resample('D').mean()   
    fig2 = px.line(daily, 
                x=daily.index, 
                y="activePowerT",
                color_discrete_sequence=['orange'],
                markers=True,
                labels=dict(dateTime="Date",activePowerT="Active Power (kW)"),
)
    st.write(fig2)  

    st.markdown(r"$\textsf{\Large Detailed Data View}$") 
    st.dataframe(df)

# Predictions Tab
with prediction_tab:
    fig3 = go.Figure()
    st.header("Predictions")
    fig3 = px.line(future_w_features['pred'],
                x=future_w_features.index,
                y="pred",
                    color_discrete_sequence=['purple'],
                    markers=True,
                    labels=dict(dateTime="Date",activePowerT="Active Power (kW)")
                    )
    
    fig3.update_layout(
        xaxis=dict(
            title=dict(
                text="Date"
            )
        ),
        yaxis=dict(
        title=dict(
            text="Active Power Predictions (kW)"
        )
     )
    )

    
    st.write(fig3)

# Real-Time Monitoring Tab
with realtime_tab:
    st.header("Real Time Data")
    Ml.RTC()
    # df = firebase.test(1,30)
    df = Ml.get_data("Combined.xlsx")
    print(df.tail())
    # df = Ml.preprocessing(df)
    st.session_state.data = Ml.get_recent_data(df)
    Ml.show_latest_data(df)
    st.dataframe(df)