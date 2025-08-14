#include "thingProperties.h"
#include <Arduino_LSM6DS3.h>
#include <math.h>

const float ACC_THRESHOLD = 1.5; 

void setup() {
  Serial.begin(9600);
  delay(1500);  
  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}

void loop() {
  ArduinoCloud.update();

  float x, y, z;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    acc_x = x;
    acc_y = y;
    acc_z = z;

    float magnitude = sqrt(x * x + y * y + z * z);
    accMagnitude = magnitude;
    Serial.println(magnitude);

    if (magnitude > ACC_THRESHOLD) {
      alarmLED = true; 
    } else alarmLED = false;
  }

  delay(500); 
}
