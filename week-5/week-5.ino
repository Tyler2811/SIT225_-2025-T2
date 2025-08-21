#include <Arduino_LSM6DS3.h>

void setup() {
  Serial.begin(9600);
  while (!Serial) { ; }
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  Serial.println("gx,gy,gz");
}

void loop() {
  float gx, gy, gz;
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gx, gy, gz); 
    Serial.print(gx, 6); Serial.print(",");
    Serial.print(gy, 6); Serial.print(",");
    Serial.println(gz, 6);
    delay(500);
  }
}
