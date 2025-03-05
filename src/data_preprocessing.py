import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split

# Define file path
file_path = "processed_data/merged_dataset.csv"  # Update if needed

# Load dataset with error handling
try:
    df = pd.read_csv(file_path)
    print("✅ Dataset loaded successfully!\n")
except FileNotFoundError:
    print(f"❌ Error: File not found at {file_path}")
    exit()
except Exception as e:
    print(f"❌ Error loading file: {e}")
    exit()

# Display basic info
print("Dataset Info:\n", df.info())
print("\nFirst 5 Rows:\n", df.head())

# Handle missing values
print("\nMissing Values Before Filling:\n", df.isnull().sum()[df.isnull().sum() > 0])

# Fill missing values with column median (numeric columns only)
df.fillna(df.median(numeric_only=True), inplace=True)

# Drop duplicate rows
df.drop_duplicates(inplace=True)

# Convert categorical columns (except 'Label') to numerical
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
if 'Label' in categorical_cols:
    categorical_cols.remove('Label')

if categorical_cols:
    print(f"\nEncoding categorical columns: {categorical_cols}")
    df = pd.get_dummies(df, columns=categorical_cols)

# Encode 'Label' column if it exists
if 'Label' in df.columns:
    le = LabelEncoder()
    df['Label'] = le.fit_transform(df['Label'])
    print("\nLabel Encoding Mapping:\n", dict(zip(le.classes_, le.transform(le.classes_))))

# Normalize numerical features
scaler = MinMaxScaler()
X = df.drop(columns=['Label'], errors='ignore')  # Drop label column if exists
y = df['Label'].values if 'Label' in df.columns else None  # Convert to NumPy array

X_scaled = scaler.fit_transform(X)

# Split data into training and testing sets (if label exists)
if y is not None:
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
    print("\nDataset Shapes:")
    print(f"X_train: {X_train.shape}, X_test: {X_test.shape}")
    print(f"y_train: {y_train.shape}, y_test: {y_test.shape}")

    # Save processed data
    pd.DataFrame(X_train).to_csv("processed_data/X_train.csv", index=False)
    pd.DataFrame(X_test).to_csv("processed_data/X_test.csv", index=False)
    pd.DataFrame(y_train, columns=["Label"]).to_csv("processed_data/y_train.csv", index=False)
    pd.DataFrame(y_test, columns=["Label"]).to_csv("processed_data/y_test.csv", index=False)

    print("\n✅ Data Preprocessing Completed Successfully!")
else:
    print("\n⚠️ Warning: No 'Label' column found. Skipping train-test split.")