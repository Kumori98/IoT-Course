//Esercizio 2 (LED rosso e LED verde)

#include <MBED_RPi_Pico_TimerInterrupt.h>

const int RLED_PIN = 2;
const int GLED_PIN = 3;

const long R_HALF_PERIOD = 1500L;
const long G_HALF_PERIOD = 3500L;

volatile int redLedState = 0;
volatile int greenLedState = 0;

MBED_RPI_PICO_Timer ITimer1(1);

void blinkGreen(uint alarm_num){
  TIMER_ISR_START(alarm_num);
  digitalWrite(GLED_PIN, greenLedState);
  greenLedState = !greenLedState;
  TIMER_ISR_END(alarm_num);
}

void setup() {
  pinMode(RLED_PIN, OUTPUT);
  pinMode(GLED_PIN, OUTPUT);
  ITimer1.setInterval(G_HALF_PERIOD * 1000, blinkGreen);
  Serial.begin(9600);
  while(!Serial);
  Serial.println("Lab 1.2 Starting");
}

void serialPrintStatus() {
  if(Serial.available() > 0){ //byte disponibili sulla seriale
    char inByte = Serial.read();
    if(inByte == 'G'){
      if(greenLedState == 1)
        Serial.println("LED 3 Status: 1");
      else
        Serial.println("LED 3 Status: 0");
    }
    else if(inByte == 'R'){
      if(redLedState == 1)
        Serial.println("LED 2 Status: 1");
      else
        Serial.println("LED 2 Status: 0");
    }
    else{
      Serial.println("Errore");
    }
  }
}

void loop(){
  serialPrintStatus();
  digitalWrite(RLED_PIN, redLedState); 
  redLedState = !redLedState;
  delay(R_HALF_PERIOD);
}
