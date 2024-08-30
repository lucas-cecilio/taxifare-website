import streamlit as st
import requests
from datetime import datetime

# Define the URL for the taxi fare prediction API
base_url = 'https://taxifare-98034930128.europe-west1.run.app/predict'

# Streamlit user interface
st.title("Taxi Fare Predictor")

# Input for pickup datetime with default value as now
pickup_date = st.date_input("Pickup Date", value=datetime.today())
pickup_time = st.time_input("Pickup Time", value=datetime.now())
pickup_datetime = str(pickup_date) + ' ' + str(pickup_time)

# Inputs for pickup and dropoff locations
## Set location boundaries
min_lat, max_lat = 40.5, 40.9
min_lon, max_lon = -74.3, -73.7

## Input the values
pickup_latitude = st.number_input("Pickup Latitude", value=40.71427, min_value=min_lat, max_value=max_lat)
pickup_longitude = st.number_input("Pickup Longitude", value=-74.00597, min_value=min_lon, max_value=max_lon)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.802, min_value=min_lat, max_value=max_lat)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.956, min_value=min_lon, max_value=max_lon)

# Input for passenger count with the restrictions values that API has
passenger_count = st.multiselect(
    "Passenger Count",
    options=list(range(1, 9)), # allow to select between 1 and 8
    default=[1], # initial value as 1
    max_selections=1 
)

# Button to get prediction
if st.button('Get Fare'):
    # Params dictionary with input data
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_latitude": pickup_latitude,
        "pickup_longitude": pickup_longitude,
        "dropoff_latitude": dropoff_latitude,
        "dropoff_longitude": dropoff_longitude,
        "passenger_count": passenger_count
    }
    
    # Sending request to the API
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        fare = response.json().get('fare')
        st.success(f'Predicted Fare: ${fare:.2f}')
    else:
        st.error(f"Error: {response.status_code}")