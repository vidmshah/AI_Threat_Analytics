import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

# Load the dataset
df = pd.read_csv("/Users/vidit/Downloads/AI_Threat_Analytics/processed_data/engineered_dataset.csv")

# Print available columns for debugging
print("Available columns in dataset:", df.columns.tolist())

# Drop only columns that exist in the dataset
columns_to_drop = ["Src IP", "Dst IP", "Timestamp"]
existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]

X = df.drop(columns=existing_columns_to_drop + ["Label"])  # Remove identifier columns
y = df["Label"]

# Check unique values in Label column
print("Unique values in Label column:", y.unique())

# Convert Label column to categorical if it's continuous
if np.issubdtype(y.dtype, np.number):
    print("Converting continuous labels to categorical...")
    y = pd.cut(y, bins=5, labels=False)  # Use pd.cut to ensure fixed bin counts

print("Labels after binning:", np.unique(y))

# Split the data into training and testing sets
if len(np.unique(y)) > 1:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
else:
    print("Warning: Only one class present after binning. Adjust binning strategy.")
    exit()

# Check Train-Test Distribution
print("y_train class distribution:\n", pd.Series(y_train).value_counts())
print("y_test class distribution:\n", pd.Series(y_test).value_counts())

# Train the model
print("Training the Random Forest Classifier...")
clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate the model
if len(np.unique(y_test)) > 1:
    print("Model Evaluation:")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
else:
    print("Warning: Model is predicting only one class. Check label processing.")

print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

# Ensure the directory exists before saving the model
model_dir = os.path.join(os.path.dirname(__file__), "../models")
os.makedirs(model_dir, exist_ok=True)

# Save the trained model
joblib.dump(clf, os.path.join(model_dir, "threat_classifier.pkl"))
print("Model saved successfully: ../models/threat_classifier.pkl")