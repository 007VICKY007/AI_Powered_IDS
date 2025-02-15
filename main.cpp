#include <Arduino.h>
#include <WiFi.h>

const char* ssid = "Lucifer";
const char* password = "123456789";

void setup() {
  Serial.begin(115200);
  delay(10);

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  Serial.println("Setup done");

  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  Serial.println("Scanning for available networks...");
  int n = WiFi.scanNetworks();
  Serial.println("Scan done");
  if (n == 0) {
    Serial.println("No networks found");
  } else {
    Serial.print(n);
    Serial.println(" networks found");
    for (int i = 0; i < n; ++i) {
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(") ");
      Serial.print(WiFi.BSSIDstr(i));
      Serial.print(" ");
      Serial.print(WiFi.channel(i));
      Serial.print(" ");
      Serial.print(WiFi.encryptionType(i) == WIFI_AUTH_OPEN ? "Malicious" : "Safe");
      Serial.println();
      delay(10);
    }
  }
  delay(5000);
}
