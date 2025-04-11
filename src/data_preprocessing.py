import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

# 📌 Define file paths
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../processed_data")
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "../processed_data")

input_file = os.path.join(DATA_FOLDER, "merged_dataset.csv")  # Use merged dataset
output_file = os.path.join(OUTPUT_FOLDER, "cleaned_dataset.csv")  # Save location

def load_and_preprocess_data():
    """Loads and preprocesses the merged dataset."""
    
    # 🔹 Load the dataset
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"❌ File not found: {input_file}")
    
    print(f"📌 Loading dataset: {input_file}")
    df = pd.read_csv(input_file, dtype=str, low_memory=False)

    # 🔹 Handle missing values using forward fill
    df.ffill(inplace=True)

    # 🔹 Convert numeric columns back to proper types
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])  # Convert to numeric type if possible
        except ValueError:
            pass  # Keep as string if conversion fails

    # 🔹 Normalize numerical columns
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns
    if len(num_cols) > 0:
        scaler = StandardScaler()
        df[num_cols] = scaler.fit_transform(df[num_cols])

    # 🔹 Encode categorical columns
    cat_cols = df.select_dtypes(include=['object']).columns
    encoder = LabelEncoder()
    for col in cat_cols:
        df[col] = df[col].astype(str)  # Convert everything to string before encoding
        df[col] = encoder.fit_transform(df[col])

    return df

if __name__ == "__main__":
    # 🔹 Process the dataset
    processed_data = load_and_preprocess_data()
    print("✅ Data preprocessing complete!")

    # 🔹 Ensure output directory exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # 🔹 Save processed data
    processed_data.to_csv(output_file, index=False)

    print(f"✅ Processed data saved to: {output_file}")



# import pandas as pd

# # Load the cleaned dataset
# df = pd.read_csv("/Users/vidit/Downloads/AI_Threat_Analytics/processed_data/cleaned_dataset.csv")

# # Display basic info
# print(df.info())
# print(df.head())

# # Check for missing values
# print(df.isnull().sum())

# # Check class distribution
# if 'threat_type' in df.columns:
#     print(df['threat_type'].value_counts())