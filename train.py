import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Specify the path where you want to save the models
save_path = "D:\\Projects\\KOchi\\"

# Load the dataset
file_path = "C:/Users/vigne/OneDrive/New folder/2025-02-08T11-10_export.csv"
df = pd.read_csv(file_path)
df = df.drop(columns=["Unnamed: 0"], errors='ignore')

# Print original DataFrame shape
print(f"Original DataFrame shape: {df.shape}")

def security_mapping(x):
    if isinstance(x, str):
        x = x.lower().strip()
        if x in ["open", "unencrypted", "u"]:
            return 1
        elif x in ["wpa2-personal", "wpa2/wpa3-personal", "wpa3-personal"]:
            return 0
        else:
            return -1
    return -1

df["Security_Label"] = df["Security"].apply(security_mapping)

# Check unique values in Security_Label
print(f"Unique Security Labels: {df['Security_Label'].unique()}")

expected_columns = {'RSSI', 'Channel', 'Security_Label'}
if not expected_columns.issubset(df.columns):
    raise KeyError(f"Missing required columns. Found: {df.columns.tolist()}")

df['RSSI'] = pd.to_numeric(df['RSSI'], errors='coerce')
df['Channel'] = pd.to_numeric(df['Channel'], errors='coerce')

# Print shape after converting to numeric
print(f"DataFrame shape after numeric conversion: {df.shape}")

# Print the DataFrame before dropping NaNs
print("DataFrame before dropping NaNs:")
print(df[['RSSI', 'Channel', 'Security_Label']].head(10))  # Show first 10 rows

df = df.dropna(subset=['RSSI', 'Channel'])

# Print shape after dropping NaN values
print(f"DataFrame shape after dropping NaNs: {df.shape}")

# Check for remaining unique values
print("Remaining unique values in RSSI and Channel:")
print(f"Unique RSSI values: {df['RSSI'].unique()}")
print(f"Unique Channel values: {df['Channel'].unique()}")

X = df[['RSSI', 'Channel']].values
y = df['Security_Label'].values

# Check number of samples
num_samples = len(X)
print(f"Number of samples: {num_samples}")

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save the scaler regardless of the number of samples
joblib.dump(scaler, save_path + "scaler.pkl")

# Train the model if there are enough samples
if num_samples < 2:
    print("Warning: Not enough samples to train a model. Proceeding to save a placeholder model.")
    # Create a placeholder model
    rf_model = RandomForestClassifier()  # Placeholder model, not trained
else:
    rf_model = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
    X_train, y_train = X_scaled, y  # Use the single sample for training
    rf_model.fit(X_train, y_train)

# Save the model
joblib.dump(rf_model, save_path + "wifi_model.pkl")

# Create and save a simple neural network model
nn_model = Sequential([
    Dense(64, activation='relu', input_shape=(X_scaled.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

nn_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Fit the model even if there's one sample (not meaningful, but for saving)
nn_model.fit(X_scaled, y, epochs=1, batch_size=1)  # Use batch_size=1 for a single sample

# Save the neural network model
nn_model.save(save_path + "trained_model.h5")

print("Models saved successfully in:", save_path)
