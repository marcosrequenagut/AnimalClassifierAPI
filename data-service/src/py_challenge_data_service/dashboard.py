import streamlit as st
import requests
import pandas as pd

st.title("Animals Classification Dashboard")

st.write("Introduce the features of the animal to classify it.")

# Inputs
legs = st.number_input("Number of legs", min_value=0, max_value=4, value=2)
height = st.number_input("Height (m)", min_value=0.0, max_value=5.0, value=1.8)
weight = st.number_input("Weight (kg)", min_value=0.0, max_value=5000.0, value=80.0)

# Yes/No checkbox for has_wings
has_wings = st.radio("Does the animal has wings?", ("Yes", "No"))

# Url of my API
api_url = "http://127.0.0.1:8777"

# Url of my API with the endpoint predict
endpoint_pedrict = "/api/v1/predict/predict"
api_url_endpoint_predict = api_url + endpoint_pedrict

# Url of my API with the endpoint retrain
endpoint_retrain = "/api/v1/retrain/retrain"
api_url_endpoint_retrain = api_url + endpoint_retrain

# Url of my API with the endpoint store_prediction
endpoint_store_prediction = "/api/v1/store_prediction/store_prediction"
api_url_endpoint_store_prediction = api_url + endpoint_store_prediction

# Url of my API with the endpoint get_data_from_database
endpoint_get_data_from_database = "/api/v1/get_data_from_database/get_data_from_database"
api_url_endpoint_get_data_from_database = api_url + endpoint_get_data_from_database

# Button to make the prediction
if st.button("Predict"):
    # Prepare the input data
    input_data = {
        "walks_on_n_legs": legs,
        "height": height,
        "weight": weight,
        "has_wings": True if has_wings == "Yes" else False,
    }

    try:
        # Make the prediction request
        response = requests.post(api_url_endpoint_predict, json=input_data)

        # Check if the request was successful
        if response.status_code == 200:
            prediction = response.json().get("Predicted label", "unknown")
            st.success(f"It's a {prediction}!")
        else:
            st.error("Error in the prediction request")
            st.json(response.json()) # Show the error message from the API

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred when connecting with the API: {e}")

# Button to retrain the model
retrain_check = st.radio("Do you want to retrain the model?", ("Yes", "No"))

if retrain_check == "Yes":
    # If the user wants to retrain the model, show the button, else do not show it
    if st.button("Retrain"):
        try:
            # Make the retrain request
            response = requests.post(api_url_endpoint_retrain)

            # Check if the request was successful
            if response.status_code == 200:
                st.success("Model retrained succesfully!")
            else:
                st.error("Error in the retrain request")
                st.json(response.json()) # Show the error message from the API

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred when connecting with the API: {e}")

# Button to store the data and prediction in the SQL Database
store_check = st.radio("Do you want to store the data and prediction in the SQL Database?", ("Yes", "No"))

if store_check == "Yes":
    # If the user wants to store the data and prediction, show the button, else do not show it
    if st.button("Store data and prediction"):
        # Prepare the input data
        input_data = {
            "walks_on_n_legs": legs,
            "height": height,
            "weight": weight,
            "has_wings": has_wings,
        }

        try:
            # Make the store request
            response = requests.post(api_url_endpoint_store_prediction, json=input_data)

            # Check if the request was successful
            if response.status_code == 200:
                st.success("Data and prediction stored successfully!")
            else:
                st.error("Error in the store request")
                st.json(response.json()) # Show the error message from the API

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred when connecting with the API: {e}")

# Button to show the data from the SQL Database
show_data_check = st.radio("Do you want to show the data from the SQL database", ("Yes", "No"))

if show_data_check == "Yes":
    if st.button("Get the data"):
        try:
            # Make the GET request to fetch data from database
            response = requests.get(api_url_endpoint_get_data_from_database)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json() # This should be the list of records from the database
                
                if data:  # Check if data is not empty
                    # Change the format from json to Dataframe
                    df = pd.DataFrame(data)
                    
                    # Display the data in a dataframe
                    st.write(df)
                else:
                    st.warning("No data found in the database")
            else:
                st.error("Error in the get data request")
                st.json(response.json()) # Show the error message from the API

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred when connecting with the API: {e}")