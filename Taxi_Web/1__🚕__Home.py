import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="NYC Taxi Analysis", initial_sidebar_state='expanded', page_icon='🚕', layout='wide')

# Header
st.markdown("""
    <div style="text-align: center; font-size: 50px; font-weight: bold; color: white;">
        NYC <span style="color: #F7C300;">Taxi Analysis</span>
    </div>
    <div style="display: flex; justify-content: center;">
        <img src="https://media.giphy.com/media/Vr6j9eVXirZg4/giphy.gif" alt="Taxi GIF" style="width: 80%; max-width: 900px;">
    </div>
""", unsafe_allow_html=True)

# Create three tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Dataset", "Prediction"])

# Content for the Overview tab
with tab1:
    st.markdown('''
    ## 🚖 Explore the NYC TLC Trip Record Data

    * Welcome to the NYC Taxi Analysis dashboard! This application allows you to delve into the rich dataset from the New York City Taxi and Limousine Commission (TLC).
    * Our goal is to uncover insights about NYC's taxi services and understand various patterns and trends.

    ### Key Analysis Areas

    - **Total Trips**:
        - Analyze the number of taxi trips across different periods: daily, monthly, and yearly.
        - Identify trends and peak usage times.

    - **Trip Duration Analysis**:
        - Investigate how trip durations vary throughout the day and under different traffic conditions.
        - Determine the efficiency of various routes.

    - **Distance Analysis**:
        - Assess the typical length of trips and popular routes.
        - Understand how distance impacts overall taxi service.

    - **Fare Analysis**:
        - Explore fare amounts including surcharges, tolls, and tips.
        - Examine pricing trends and fare distribution.

    - **Passenger Behavior**:
        - Study the number of passengers per trip, payment methods, and location patterns.
        - Identify travel trends and high-demand areas.

    - **Temporal Patterns**:
        - Analyze how taxi usage changes by time of day, day of the week, and season.
        - Discover peak hours and low-demand periods.

    This analysis provides a comprehensive view of NYC's taxi services, helping optimize transportation planning and service delivery.
    ''')

# Content for the Dataset tab
with tab2:
    st.markdown('''
    ## 📊 NYC Taxi Trip Dataset Overview

    The NYC TLC Trip Record dataset contains detailed information on each taxi trip. Here are the key fields:

    | Column Name            | Description                                                        |
    |------------------------|--------------------------------------------------------------------|
    | **VendorID**           | Identifier for the taxi service provider.                         |
    | **tpep_pickup_datetime** | Date and time when the meter was engaged.                         |
    | **tpep_dropoff_datetime** | Date and time when the meter was disengaged.                      |
    | **Passenger_count**    | Number of passengers in the vehicle.                               |
    | **Trip_distance**      | Distance of the trip measured by the taximeter.                    |
    | **PULocationID**       | Pick-up location ID.                                               |
    | **DOLocationID**       | Drop-off location ID.                                              |
    | **RatecodeID**         | Rate code applied to the trip.                                     |
    | **store_and_fwd_flag** | Indicates if the trip record was stored before being sent to the vendor. |
    | **Payment_type**       | Method of payment (e.g., cash, credit card).                       |
    | **Fare_amount**        | Fare calculated by time and distance.                              |
    | **Extra**              | Additional charges like surcharges.                                |
    | **MTA_tax**            | MTA tax applied based on location.                                 |
    | **Improvement_surcharge** | Surcharge for the Improvement Fund.                               |
    | **Tip_amount**         | Tip amount given (if paid by credit card).                         |
    | **Tolls_amount**       | Total amount of tolls paid during the trip.                        |
    | **Total_amount**       | Total amount paid, including all charges.                          |

    ### Dataset Source

    For more detailed information, visit the [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) page.

    ### Sample Data

    Click the button below to view a sample of the dataset. This will help you understand the structure and content of the data.
    ''')

    # Button to show a sample of the dataset
    if st.button('Show Sample Data'):
        # Load the dataset (replace with actual path or URL)
        df = pd.read_csv('sample.csv')  # Update this line with your dataset path
        st.dataframe(df, use_container_width=True)

# Content for the Prediction tab
with tab3:
    st.markdown("""
    ## 🎯 Discover Accurate Fare Predictions!

    Welcome to the **Prediction Section**! 🌟 Here, you can seamlessly access our **advanced prediction tool** designed to provide you with precise taxi fare estimates based on various parameters.

    ### How It Works:
    - **Step 1: Enter Your Details**: Input the required parameters on the prediction page to get started.
    - **Step 2: Get Instant Results**: Receive accurate fare estimates in real-time based on your inputs.
    - **Step 3: Benefit from Advanced Algorithms**: Our sophisticated algorithms ensure high accuracy for your fare predictions.

    **Ready to make your predictions?** 
    Click the button below to explore the prediction tool and start your journey!

    [Access Prediction Tool](https://yellowtaxiassistant.netlify.app/)
    """)
