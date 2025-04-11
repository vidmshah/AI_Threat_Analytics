import pandas as pd
from prophet import Prophet
import os
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("/Users/vidit/Downloads/AI_Threat_Analytics/processed_data/merged_dataset.csv")
print(f"Loaded dataset with {len(df)} rows.")

# Ensure required columns exist
if 'Timestamp' not in df.columns or 'Label' not in df.columns:
    raise ValueError("Dataset must contain 'Timestamp' and 'Label' columns.")

# Convert Timestamp to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df = df.dropna(subset=['Timestamp'])  # Drop rows with invalid timestamps
print(f"Remaining rows after cleaning timestamps: {len(df)}")

# Forecast total number of attacks per day
df['Date'] = df['Timestamp'].dt.date
daily_attacks = df.groupby('Date').size().reset_index(name='y')
daily_attacks.rename(columns={'Date': 'ds'}, inplace=True)

print(f"Number of unique dates: {daily_attacks['ds'].nunique()}")
if len(daily_attacks) < 2:
    raise ValueError("Not enough data for time series forecasting. Ensure the dataset spans multiple dates.")

# Train Prophet model
model = Prophet()
model.fit(daily_attacks)

# Make future dataframe
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Create forecast directory
output_dir = os.path.join(os.path.dirname(__file__), "../forecasts")
os.makedirs(output_dir, exist_ok=True)

# Save and plot forecast
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(os.path.join(output_dir, "daily_attack_forecast.csv"), index=False)
fig1 = model.plot(forecast)
fig1.savefig(os.path.join(output_dir, "daily_attack_forecast.png"))

# Forecast number of each type of attack
attack_types = df['Label'].unique()
for attack in attack_types:
    subset = df[df['Label'] == attack]
    subset['Date'] = subset['Timestamp'].dt.date
    type_attacks = subset.groupby('Date').size().reset_index(name='y')
    type_attacks.rename(columns={'Date': 'ds'}, inplace=True)

    if len(type_attacks) < 2:  # Prophet requires at least two data points
        print(f"Skipping attack type '{attack}' due to insufficient data.")
        continue

    model_type = Prophet()
    model_type.fit(type_attacks)
    future_type = model_type.make_future_dataframe(periods=30)
    forecast_type = model_type.predict(future_type)

    forecast_type[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(
        os.path.join(output_dir, f"{attack}_forecast.csv"), index=False
    )
    fig2 = model_type.plot(forecast_type)
    fig2.savefig(os.path.join(output_dir, f"{attack}_forecast.png"))

if len(attack_types) == 0:
    print("Warning: No attack types found in dataset.")

print("Forecasts generated and saved in 'forecasts/' directory.")