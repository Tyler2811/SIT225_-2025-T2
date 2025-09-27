/*
 * HydroSync: Smart Water Intake Tracker - Serial Output Version
 * Student: Tan Tai Le (s224621011)
 * drinkCount++ when refill LED turns from ON to OFF
 * Outputs data in parseable format for Python
 */

#include <DHT.h>
#include <Arduino_LSM6DS3.h>

#define DHT_PIN 5
#define DHT_TYPE DHT22
#define TRIG_PIN 6
#define ECHO_PIN 7

DHT dht(DHT_PIN, DHT_TYPE);

// Cup parameters
const float CUP_HEIGHT = 12.0;
const float CUP_VOLUME = 665.0;
const float EMPTY_THRESHOLD = 11.5;
const float FULL_THRESHOLD = 2.0;

bool wasDrinking = false;
bool previousRefillLed = false;
unsigned long lastDrinkTime = 0;
const unsigned long DRINK_COOLDOWN = 3000;
float totalWaterConsumed = 0;
float dailyGoal = 2000.0;

float waterLevel = 0;
int drinkCount = 0;
String cupStatus = "";
bool refillLed = false;
float temperature = 0;
float humidity = 0;

void setup() {
  Serial.begin(9600);
  delay(1500);
  
  dht.begin();
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while(1);
  }
  
  cupStatus = "SYSTEM_READY";
  refillLed = false;
  previousRefillLed = false;
  
  Serial.println("HydroSync Serial Ready!");
  Serial.println("Format: WaterLevel:0,DrinkCount:0,Status:READY,LED:OFF,Temp:0,Hum:0");
}

void loop() {
  readUltrasonicSensor();
  readAccelerometer();
  readEnvironmentalData();
  outputSerialData();  // Send data to serial
  delay(2000);
}

void readUltrasonicSensor() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2;
  
  if (distance > 0 && distance < 20) {
    float currentWaterLevel = CUP_HEIGHT - distance;
    if (currentWaterLevel < 0) currentWaterLevel = 0;
    waterLevel = (currentWaterLevel / CUP_HEIGHT) * CUP_VOLUME;
    
    // Save previous state before updating
    bool oldRefillLed = refillLed;
    
    // Update LED based on water level
    if (distance >= EMPTY_THRESHOLD) {
      cupStatus = "EMPTY_REFILL_NEEDED";
      refillLed = true;
    } else if (distance <= FULL_THRESHOLD) {
      cupStatus = "FULL";
      refillLed = false;
    } else {
      cupStatus = "WATER_AVAILABLE";
      refillLed = false;
    }
    
    // Check if refill LED just turned from ON to OFF
    if (previousRefillLed && !refillLed) {
      drinkCount++;
      Serial.print("Refill counted! Total: ");
      Serial.println(drinkCount);
    }
    
    previousRefillLed = oldRefillLed;
  }
}

void readAccelerometer() {
  float x, y, z;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    detectDrinkingMotion(x, y, z);
  }
}

void detectDrinkingMotion(float x, float y, float z) {
  unsigned long currentTime = millis();
  float acceleration = sqrt(x*x + y*y + z*z);
  
  bool tippingMotion = (z < 0.5 && z > -0.8);
  bool movementDetected = (acceleration > 1.3 && acceleration < 3.0);
  
  if (tippingMotion && movementDetected) {
    if (!wasDrinking && (currentTime - lastDrinkTime > DRINK_COOLDOWN)) {
      totalWaterConsumed += 200;
      if (totalWaterConsumed > CUP_VOLUME) totalWaterConsumed = CUP_VOLUME;
      
      lastDrinkTime = currentTime;
      wasDrinking = true;
      cupStatus = "DRINKING_DETECTED";
      Serial.println("Drink detected!");
    }
  } else {
    wasDrinking = false;
  }
}

void readEnvironmentalData() {
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  
  if (!isnan(temp) && !isnan(hum)) {
    temperature = temp;
    humidity = hum;
  }
}
void outputSerialData() {
  Serial.print("WaterLevel:");
  Serial.print(waterLevel);
  Serial.print(",DrinkCount:");
  Serial.print(drinkCount);
  Serial.print(",Status:");
  Serial.print(cupStatus);
  Serial.print(",LED:");
  Serial.print(refillLed ? "ON" : "OFF");
  Serial.print(",Temp:");
  Serial.print(temperature);
  Serial.print(",Hum:");
  Serial.print(humidity);
  Serial.println(); 
}