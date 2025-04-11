import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

# 📌 Define file paths
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../processed_data")
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "../processed_data")

input_file = os.path.join(DATA_FOLDER, "cleaned_dataset.csv")  # Use cleaned dataset
output_file = os.path.join(OUTPUT_FOLDER, "engineered_dataset.csv")  # Save location

def feature_engineering():
    """Performs feature engineering on the dataset."""
    
    # 🔹 Load the cleaned dataset
    df = pd.read_csv(input_file, low_memory=False)
    print(f"📌 Loaded dataset: {input_file}, Shape: {df.shape}")

    # 🔹 Drop unnecessary columns
    drop_cols = ["Flow ID", "Timestamp", "Src IP", "Dst IP"]
    df.drop(columns=drop_cols, inplace=True, errors='ignore')
    
    # 🔹 Create new features
    df["Threat Intensity"] = df["Flow Byts/s"] / (df["Flow Duration"] + 1)  # Prevent division by zero
    df["Packet Ratio"] = df["Tot Fwd Pkts"] / (df["Tot Bwd Pkts"] + 1)

    # 🔹 Normalize numerical columns
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])

    # 🔹 Save processed data
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"✅ Feature engineering complete! Data saved to {output_file}")

if __name__ == "__main__":
    feature_engineering()