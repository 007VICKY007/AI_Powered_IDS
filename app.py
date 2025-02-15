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
