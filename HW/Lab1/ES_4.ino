float speed = 0;
const int FAN_PIN = 2;

void setup() {
  // put your setup code here, to run once:
  pinMode(FAN_PIN, OUTPUT);
  analogWrite(FAN_PIN, (int) speed);
}

void loop() {
  // put your main code here, to run repeatedly:
  char input = Serial.read();
  if(input == '+'){
    if(speed < 255){
      speed += 25.5;
    }
    else{
      Serial.println("Max speed");
    }
  }
  else if(input == '-'){
    if(speed > 0){
      speed -= 25.5;
    }
    else{
      Serial.println("Min speed");
    }
  }
  Serial.println(speed);
  analogWrite(FAN_PIN, (int) speed);
  delay(2000);
}
