<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the trained model
model = tf.keras.models.load_model("trained_model.h5")

# Global variable to store network data
network_data = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global network_data
    if request.method == 'GET':
        return jsonify({"networks": network_data}), 200

    elif request.method == 'POST':
        data = request.get_json()
        if not data or "networks" not in data:
            return jsonify({"error": "No valid JSON data received"}), 400

        network_data = data["networks"]  # Store received data
        print("Received data:", network_data)
        
        # Process network data using the model
        predictions = []
        for network in network_data:
            try:
                input_features = np.array(network, dtype=np.float32).reshape(1, -1)  # Ensure input shape
                prediction = model.predict(input_features)
                is_malicious = bool(prediction[0][0] > 0.5)  # Assuming binary classification
                predictions.append({"network": network, "malicious": is_malicious})
            except Exception as e:
                predictions.append({"network": network, "error": str(e)})
        
        return jsonify({"message": "Data received successfully", "results": predictions}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
=======
import serial
import requests
import json
from flask import Flask, jsonify

# Initialize Flask App
app = Flask(__name__)

# Serial Port Configuration (Change COM5 if needed)
SERIAL_PORT = "COM5"
BAUD_RATE = 9600
server_url = "http://your-server.com/upload"  # Change to actual server URL

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
except Exception as e:
    print(f"Error: Could not open {SERIAL_PORT}. {str(e)}")

def read_serial_data():
    """Read data from Serial Port and forward it via HTTP."""
    try:
        if ser.in_waiting:
            raw_data = ser.readline().decode("utf-8", errors="ignore").strip()
            if raw_data:
                print(f"📡 Received from ESP32: {raw_data}")

                # Send to server via HTTP
                response = requests.post(server_url, json=json.loads(raw_data))
                print(f"✅ Server Response: {response.status_code}, {response.text}")

    except json.JSONDecodeError:
        print("⚠️ JSON Decoding Error")
    except Exception as e:
        print(f"⚠️ Serial Read Error: {str(e)}")

@app.route("/")
def home():
    return jsonify({"message": "ESP32 Serial Wi-Fi Scanner Running!"})

if __name__ == "__main__":
    print("🚀 Flask Server Running...")
    while True:
        read_serial_data()  # Continuously read and process serial data
>>>>>>> 51023e523ad1f8530130cb6715e08b340e6329cb
