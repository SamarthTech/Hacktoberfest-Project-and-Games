#include <Servo.h>

#include <NewPing.h>

const int ServoPin = 10;
const int TriggerPin = 6;
const int EchoPin = 7;

// 100 = maxDistance
NewPing sonar (TriggerPin, EchoPin, 100);
Servo servo;

void setup() {
  Serial.begin(9600);
  servo.attach(ServoPin);
}

void loop() {
  int cm = sonar.ping_cm();
  Serial.println(cm);

  int angle = map(cm, 2, 15, 15, 100);
  servo.write(angle);

  delay(50);
}
