import pandas as pd
import glob
import os
from logger import logger

logger.info("Data preprocessing started.")

# Define paths
DATA_DIR = "data"
PROCESSED_DIR = "processed_data"
MERGED_FILE = os.path.join(PROCESSED_DIR, "merged_dataset.csv")

# Ensure processed_data directory exists
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Get all CSV files in the data directory
file_paths = glob.glob(os.path.join(DATA_DIR, "*.csv"))

# Ensure files exist
if not file_paths:
    logger.error("No CSV files found in the specified directory.")
    raise FileNotFoundError("No CSV files found in the specified directory.")

column_sets = {}

# Step 1: Identify all unique columns across files
for file in file_paths:
    df = pd.read_csv(file, nrows=5)  # Read first 5 rows to check column names
    if df.empty:
        logger.warning(f"Skipping empty file: {file}")
        continue
    column_sets[file] = set(df.columns)

# Ensure we have at least one non-empty file
if not column_sets:
    logger.error("No valid CSV files with data.")
    raise ValueError("All CSV files are empty.")

# Get the union of all columns
all_columns = set.union(*column_sets.values())

# Step 2: Normalize column structure across all files
processed_files = []

for file in file_paths:
    df = pd.read_csv(file)
    
    # Skip empty files
    if df.empty:
        logger.warning(f"Skipping empty file: {file}")
        continue

    # Add missing columns with NaN values
    for col in all_columns:
        if col not in df.columns:
            df[col] = None  # Assign missing columns as NaN
    
    # Ensure column order matches `all_columns`
    df = df[list(all_columns)]
    
    # Save the processed file
    processed_file = os.path.join(PROCESSED_DIR, os.path.basename(file))
    df.to_csv(processed_file, index=False)
    processed_files.append(processed_file)
    logger.info(f"Processed and saved: {processed_file}")

# Step 3: Merge all processed CSV files
if processed_files:
    combined_df = pd.concat([pd.read_csv(file) for file in processed_files], ignore_index=True)
    
    # Save the final merged dataset
    combined_df.to_csv(MERGED_FILE, index=False)
    logger.info(f"Merged dataset saved at: {MERGED_FILE}")
    print(f"Data preprocessing completed. Merged dataset saved at: {MERGED_FILE}")
else:
    logger.error("No valid files to merge.")
    print("No valid files to merge.")