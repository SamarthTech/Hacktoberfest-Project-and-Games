void setup() {
  // put your setup code here, to run once:
pinMode(2,INPUT);//IR1
pinMode(3,INPUT);//IR2
pinMode(4,OUTPUT);//m1in1
pinMode(5,OUTPUT);//m1in2
pinMode(6,OUTPUT);//m2in1
pinMode(7,OUTPUT);//m2in2
pinMode(9,OUTPUT);//en1 m1
pinMode(10,OUTPUT);//en2 m2
pinMode(12,OUTPUT);//led
pinMode(13,OUTPUT);//led
//analogWrite(9,85);//speed m1
//analogWrite(10,85);//speed m2
Serial.begin(9600);
}

void loop() {
  

  if(digitalRead(3)==LOW && digitalRead(2)==LOW)
{//FORWARD
  digitalWrite(4,LOW);//M1 IN1
   digitalWrite(5,HIGH);//M1 IN2
   analogWrite(9,200);
    digitalWrite(6,LOW);//M2 IN1
     digitalWrite(7,HIGH);//M2 IN2
     analogWrite(10,200);
     Serial.println("Start");
}
 if(digitalRead(3)==HIGH && digitalRead(2)==LOW)
{
  digitalWrite(4,LOW);//M1 IN1
   digitalWrite(5,HIGH);//M1 IN2
    digitalWrite(6,HIGH);//M2 IN1
     digitalWrite(7,LOW);//M2 IN2
     Serial.println("Stop");
}
if(digitalRead(3)==LOW && digitalRead(2)==HIGH)
{
  digitalWrite(4,HIGH);//M1 IN1
   digitalWrite(5,LOW);//M1 IN2
   analogWrite(9,190);
    digitalWrite(7,HIGH);//M2 IN1
     digitalWrite(6,LOW);//M2 IN2
     analogWrite(10,150);
     Serial.println("Right");
}
else{

digitalWrite(4,LOW);//M1 IN1
   digitalWrite(5,HIGH);//M1 IN2
   analogWrite(9,0);
    digitalWrite(7,HIGH);//M2 IN1
     digitalWrite(6,LOW);//M2 IN2
     analogWrite(10,0);

}

}
