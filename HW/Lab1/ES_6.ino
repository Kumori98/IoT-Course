#include <LiquidCrystal_PCF8574.h>

const int TEMP_PIN = A0;
const int B = 4275;
const long int R0 = 100000;
float R;
LiquidCrystal_PCF8574 lcd(0x20);

void setup() {
  // put your setup code here, to run once:
  lcd.begin(16, 2);
  lcd.setBacklight(255);
  lcd.home();
  
  Serial.println("Lab 1 - Es 6 starting");
}

void loop() {
  // put your main code here, to run repeatedly:
  float a = analogRead(TEMP_PIN);
  R = (1023/a - 1) * R0;
  float T = log(R/R0)/B + 1/298.15;
  T = 1/T;
  T -= 273.15;
  lcd.clear();
  lcd.print("Temp: ");
  lcd.print(T);
  delay(10000);
}
