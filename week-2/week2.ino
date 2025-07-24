#include "DHT.h"
#define DHTPIN 2     
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

float hum, temp;

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  hum = dht.readHumidity();
  temp = dht.readTemperature();
  Serial.println(String(hum) + "," + String(temp));
  delay(10000); 
}
