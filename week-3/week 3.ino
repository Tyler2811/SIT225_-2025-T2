#include "thingProperties.h"
#include <Arduino_LSM6DS3.h>

void setup() {
  Serial.begin(9600);
  delay(1500);  // Allow time for serial connection
  initProperties();  // Start Arduino IoT Cloud sync
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}

void loop() {
  ArduinoCloud.update();  // Sync with Arduino IoT Cloud

  float x, y, z;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    // Send to IoT Cloud variables
    acc_x = x;
    acc_y = y;
    acc_z = z;

    Serial.println(String(x) + "," + String(y) + "," + String(z));
  }

  delay(5000);  // Update every 1 second
}
