from fastapi import APIRouter
from py_challenge_data_service.models import AnimalNoTail
import numpy as np
import pickle
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import oracledb

# Load the DB credentials
load_dotenv()

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
sid = os.getenv("sid")

def get_db_connection():
    return oracledb.connect(user=USERNAME, password=PASSWORD, host=HOST, sid=sid)

# Load the model using a relative path
model_path = Path(__file__).resolve().parent.parent / "model" / "random_forest_model.pkl"

with open(model_path, "rb") as f:
    model = pickle.load(f)

# Register the router
router = APIRouter()

# Define the endpoint to store the data and prediction in the SQL Database
@router.post("/store_prediction", summary="Store the prediction and animal data")
def store_prediction(animal: AnimalNoTail):
    """
    This endpoint stores the animal data and its prediction in the database.
    - **walks_on_n_legs**: The number of legs the animal walks on
    - **height**: The height of the animal in meters
    - **weight**: The weight of the animal in kilograms
    - **has_wings**: Whether the animal has wings
    """
    # Prepare the input data for prediction
    input_data = np.array([
        animal.walks_on_n_legs,
        animal.height,
        animal.weight,
        int(animal.has_wings)  # Transform boolean to int
    ]).reshape(1, -1)

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Store data and prediction in the database
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO NEW_DATA (walks_on_n_legs, height, weight, has_wings, prediction)
    VALUES (:walks_on_n_legs, :height, :weight, :has_wings, :prediction)
    """

    cursor.execute(query, {
        "walks_on_n_legs": animal.walks_on_n_legs,
        "height": animal.height,
        "weight": animal.weight,
        "has_wings": 1 if animal.has_wings else 0,
        "prediction": prediction
    })

    # Commit the transaction to save data
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": "Prediction and data stored successfully", "prediction": prediction}
