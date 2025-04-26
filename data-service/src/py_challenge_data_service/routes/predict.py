from fastapi import APIRouter
from py_challenge_data_service.models import AnimalNoTail
import numpy as np
import pickle
from pathlib import Path

# Load the model using a relative path
model_path = Path(__file__).resolve().parent.parent / "model" / "random_forest_model.pkl"

with open(model_path, "rb") as f:
    model = pickle.load(f)

# Register the router, it use to define the endpoints of the API
router = APIRouter()   

# Define the prediction endpoint
@router.post("/predict", summary="Predict the class of an animal")
def predict(animal: AnimalNoTail):
    """
    This endpoint predict the class of an animal based on its characteristics. 

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
        int(animal.has_wings) # Transform boolean to int
    ]).reshape(1, -1)

    # Make prediction
    prediction = model.predict(input_data)[0]

    return {"Predicted label": prediction}