
const int TEMP_PIN = A0;
const int B = 4275;
const long int R0 = 100000;
float R;

void setup() {
  // put your setup code here, to run once:
  Serial.println("Lab 1 - Es 5 starting");
}

void loop() {
  // put your main code here, to run repeatedly:
  float a = analogRead(TEMP_PIN);
  R = (1023/a - 1) * R0;
  float T = log(R/R0)/B + 1/298.15;
  T = 1/T;
  T -= 273.15;
  Serial.print("Temperature = ");
  Serial.println(T);
  delay(1000);
}
