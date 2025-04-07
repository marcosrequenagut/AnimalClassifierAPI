import streamlit as st
import requests

st.title("Animals Classification Dashboard")

st.write("Introduce the features of the animal to classify it.")

# Inputs
legs = st.number_input("Number of legs", min_value=0, max_value=4, value=2)
height = st.number_input("Height (m)", min_value=0.0, max_value=5.0, value=1.0)
weight = st.number_input("Weight (kg)", min_value=0.0, max_value=5000.0, value=50.0)
has_wings = st.checkbox("Has wings?")

# Url of my API
api_url = "http://127.0.0.1:8777/api/v1/predict/predict"

# Button to make the prediction
if st.button("Predict"):
    # Prepare the input data
    input_data = {
        "walks_on_n_legs": legs,
        "height": height,
        "weight": weight,
        "has_wings": has_wings,
    }

    try:
        # Make the prediction request
        response = requests.post(api_url, json=input_data)

        # Check if the request was successful
        if response.status_code == 200:
            prediction = response.json().get("Predicted label", "unknown")
            st.success(f"The predicted label is: {prediction}")
        else:
            st.error("Error in the prediction request")

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred when connecting with the API: {e}")