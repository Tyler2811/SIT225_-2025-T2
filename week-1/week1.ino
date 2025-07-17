int blink_count;
int random_sleep;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
  while (!Serial); 
}

void loop() {
  if (Serial.available()) {
    blink_count = Serial.parseInt();

    while (Serial.available()) Serial.read();

    for (int i = 0; i < blink_count; i++) {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
      digitalWrite(LED_BUILTIN, LOW);
      delay(500);
    }

    random_sleep = random(1, 5);
    Serial.println(random_sleep);
  }
}