#include <WiFi.h>
#include <ArduinoJson.h>

// Wi-Fi Credentials
const char* ssid = "Rahul";    
const char* password = "12345678";    

void setup() {
  Serial.begin(9600);  
  WiFi.mode(WIFI_STA);  // Ensure ESP32 is in Station mode
  
  Serial.print("🔗 Connecting to WiFi...");
  WiFi.begin(ssid, password);

  unsigned long startAttemptTime = millis(); // Timeout for WiFi connection
  
  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < 15000) { // 15s timeout
    Serial.print(".");
    delay(1000);
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ Connected to WiFi!");
  } else {
    Serial.println("\n❌ Failed to connect to WiFi");
  }
}

void scanWiFiNetworks() {
  Serial.println("🔍 Scanning for Wi-Fi networks...");
  
  int numNetworks = WiFi.scanNetworks();
  if (numNetworks == 0) {
    Serial.println("{\"status\":\"No networks found\"}");
  } else {
    JsonDocument jsonDoc;  // Use the new method instead of DynamicJsonDocument
    JsonArray networksArray = jsonDoc["networks"].to<JsonArray>();  // New approach

    for (int i = 0; i < numNetworks; i++) {
      JsonObject network = networksArray.add<JsonObject>();
      network["SSID"] = WiFi.SSID(i);
      network["BSSID"] = WiFi.BSSIDstr(i);
      network["RSSI"] = WiFi.RSSI(i);
      network["Encryption"] = (WiFi.encryptionType(i) != WIFI_AUTH_OPEN) ? "Encrypted" : "Unencrypted";
    }

    String jsonString;
    serializeJson(jsonDoc, jsonString);
    Serial.println(jsonString);  // Send JSON via Serial
  }
}

void loop() {
  scanWiFiNetworks();
  delay(10000);  // Scan every 10 seconds
}
