#include <WiFiNINA.h>
#include <ArduinoMqttClient.h>
#include <Arduino_LSM6DS3.h>

const char ssid[] = "Tấn Tài's A35";    
const char pass[] = "abcxyz123"; 

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

const char broker[] = "broker.hivemq.com";
int port = 1883;
const char topic[] = "sit225/gyro-data";

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Initialize IMU
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // Connect to WiFi
  connectWiFi();
  
  // Connect to MQTT broker
  Serial.print("Attempting to connect to MQTT broker: ");
  Serial.println(broker);
  
  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());
    Serial.println("Possible causes:");
    Serial.println("- Incorrect broker address/port");
    Serial.println("- WiFi connection issues");
    Serial.println("- Network firewall blocking MQTT");
    while (1); // Stop here if connection fails
  }
  
  Serial.println("Connected to MQTT broker!");
}

void loop() {
  float x, y, z;
  
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x, y, z);
    
    // Create JSON payload
    String payload = "{\"x\":" + String(x) + ",\"y\":" + String(y) + ",\"z\":" + String(z) + "}";
    
    // Publish to MQTT
    mqttClient.beginMessage(topic);
    mqttClient.print(payload);
    mqttClient.endMessage();
    
    Serial.println("Published: " + payload);
  }
  
  delay(1000); // Send data every second

}

void connectWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, pass);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("\nFailed to connect to WiFi!");
    Serial.println("Please check your credentials and try again.");
    while (1); // Stop here if WiFi connection fails
  }
  
  Serial.println("\nConnected to WiFi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}