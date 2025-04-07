import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.datasets import load_wine
warnings.filterwarnings(action='ignore') 


# Load the data
df = pd.read_csv(r"C:\Users\34651\Desktop\MASTER\LABORATORIOS\challenge_notebooks\data_cleaned.csv", sep=",")

# Separate the label from the features
X = df.drop("label", axis=1) # Take every column except the "label" one
y = df["label"] # Goal column

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
