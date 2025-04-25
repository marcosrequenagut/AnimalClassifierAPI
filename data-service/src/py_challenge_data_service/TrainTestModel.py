import numpy as np
import pandas as pd
import warnings
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from pathlib import Path
from minio import Minio

warnings.filterwarnings(action='ignore') 

""" Minio client, necessary to connect to the Minio server
It is usefull tu store the model in the Minio server. 
To run it, use this commando in the terminal:

docker run -p 9003:9000 -p 9004:9001 minio/minio server /data --console-address ":9001" 

We don't specify the access and secret key, because we are using the default ones.

We have to create a bucket called mpc in minio. To acces to the Minio server, we can use the browser and go to http://localhost:9004.
"""
client = Minio(
    "localhost:9003", # Minio server address
    access_key = "minioadmin", # Minio default access key
    secret_key = "minioadmin", # Minio default secret key
    secure = False,
)

# Load the data
df = pd.read_csv(r"C:\Users\34651\Desktop\MASTER\LABORATORIOS\challenge_notebooks\data_cleaned.csv", sep=",")
print(f"\n{df.head()}")

# View columns, view number of null/nan, sample data of each column,...
print(f"\n{df.info()}")

# Separate the label from the features
X = df.drop("label", axis=1) # Take every column except the "label" one
y = df["label"] # Goal column

print(f"\nX_shape: {X.shape}")
print(f"y_shpae: {y.shape}")

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
with open("random_forest_model.pkl", "wb") as f:
    pickle.dump(RFC, f)

client.fput_object("mpc", f"model/model.pkl", "random_forest_model.pkl")

# Crea la carpeta 'model' al mismo nivel que 'routes'
model_dir = Path(__file__).resolve().parent / "model"
model_dir.mkdir(parents=True, exist_ok=True)

# Define la ruta final del modelo
model_path = model_dir / "random_forest_model.pkl"

# Guarda el modelo
with open(model_path, "wb") as f:
    pickle.dump(RFC, f)

# Predict
y_pred = RFC.predict(X_test)

# Show the results
print("\n Random Forest Classifier Test Accuracy: " + str(np.round(metrics.accuracy_score(y_test, y_pred), 3)))

# Show some predictions
results = pd.DataFrame({
    "Real label": y_test.values,
    "Predicted label": y_pred
})

print("\n Showing some predictions: \n")
print(results.head(10))

# Let's show the more important features to classify the animals
importances = RFC.feature_importances_
features = X_train.columns

# Create a dataframe to order themm
feat_imp_df = pd.DataFrame({
    "Feature": features,
    "Importance": importances,
}).sort_values(by="Importance", ascending=False)

print(f"\n {feat_imp_df}")
