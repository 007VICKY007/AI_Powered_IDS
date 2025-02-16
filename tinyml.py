import numpy as np
import tensorflow as tf
import pickle
import os

# Load the TFLite model
tflite_model_path = "trained_model.tflite"

if not os.path.exists(tflite_model_path):
    raise FileNotFoundError(f"Error: Model file '{tflite_model_path}' not found!")

interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# Get input and output tensor details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load scaler (for input normalization)
scaler_path = "scaler.pkl"
if not os.path.exists(scaler_path):
    raise FileNotFoundError(f"Error: Scaler file '{scaler_path}' not found!")

try:
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    if not hasattr(scaler, "transform"):
        raise ValueError("Loaded scaler is not a valid transformer object.")
except Exception as e:
    raise ValueError(f"Error loading scaler.pkl: {e}")

# Define sample input data (Replace with real input features)
raw_input_data = np.array([[1200.0, 3.5, 2.0]])  # Example input features

# Normalize input using the scaler
try:
    normalized_input = scaler.transform(raw_input_data)
except Exception as e:
    raise ValueError(f"Error normalizing input data: {e}")

# Set the input tensor
interpreter.set_tensor(input_details[0]['index'], normalized_input.astype(np.float32))

# Run inference
interpreter.invoke()

# Get the output tensor
prediction = interpreter.get_tensor(output_details[0]['index'])

# Display the prediction result
print(f"Predicted Value: {prediction[0][0]}")
