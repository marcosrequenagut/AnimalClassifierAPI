import pandas as pd
from fastapi import APIRouter, HTTPException
from sklearn.ensemble import RandomForestClassifier
import pickle
from pathlib import Path
import logging
from sklearn.model_selection import train_test_split

# The router is used to define the endpoints of the API
router = APIRouter()

# Path to overwrite the old model
model_path = "C:/Users/34651/Desktop/MASTER/LABORATORIOS/py_challenge/data-service/src/py_challenge_data_service/model/random_forest_model.pkl"


@router.post("/retrain", summary="Retrain the model with new data")
def retrain():
    try:
        # File path
        data = r"C:\Users\34651\Desktop\MASTER\LABORATORIOS\challenge_notebooks\data_cleaned.csv"

        # Read the data
        data = pd.read_csv(data, sep=",", header=0)

        if data.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty or no labeled data found")

        # Separate the label from the features
        X = data.drop("label", axis=1) # Take every column except the "label" one
        y = data["label"] # Goal column


        # Divide the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

        # Define the model (Random Forest Classifier)
        RFC = RandomForestClassifier(
            n_estimators = 100,
            max_depth = 7,
            random_state = 42
        )

        # Train the model
        RFC.fit(X_train, y_train)

        # Save the model

        with open(model_path, "wb") as f:
            pickle.dump(RFC, f)

        logging.info("Model retrained successfully")

        return {"message": "Model retrained successfully"}

    except Exception as e:
        logging.error(f"Error retraining the model: {e}")
        raise HTTPException(status_code=500, detail="Error retraining the model")