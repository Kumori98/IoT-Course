#include <PDM.h>
#include <LiquidCrystal_PCF8574.h>
#include <MBED_RPi_Pico_TimerInterrupt.h>

const int FAN_PIN = A1, TEMP_PIN = A0, LED_PIN = A2, PIR_PIN = 4, GREEN_PIN =2;
short sampleBuffer[256];
LiquidCrystal_PCF8574 lcd(0x20);

const int B = 4275;  const long int R0 = 100000;  //parametri per termometro
volatile int samplesRead = -1;
const int timeout_pir = 10000;
const int timeout_sound_max = 8000;
const int sound_threshold = 150;
const int clap_threshold = 2200;
const int n_sound_events = 2;
int sound_events = 0;

int last_presence = 0;
int last_sound = 0;
int last_clap = 0;

bool personDetected = false;

int AC_np[] = {25, 30}, AC_p[] = {20, 25}, H_np[] = {10, 15}, H_p[] = {15, 20};
int AC[] = {25, 30}, H[] = {25, 30};
float offset = 127.5; //Potenza minima per far partire la ventola
const long lcdPeriod = 5000L;
MBED_RPI_PICO_Timer ITimer1(1);
bool lcdState = false;
bool greenLedState = false;


//Controllo velocità ventola
float fanSpeed(float temp){

  if(temp > AC[1])
    return 255;

  if(temp <= AC[1] && temp >= AC[0])
    return offset * (1 + ((float)temp - AC[0])/(AC[1] - AC[0]));

  return 0;
}

//Controllo luminosità led
float ledLight(float temp){
  int offset = 255;

  if(temp < H[0])
    return 255;
  
  if(temp > H[1])
    return 0;
  
  return offset * (1 - ((float)temp - AC[0])/(AC[1] - AC[0]));
}

//Calcolo della temperatura con sensore esterno
float readTemp(){
  float a = analogRead(TEMP_PIN);
  float R = (1023/a - 1) * R0;
  float T = log(R/R0)/B + 1/298.15;
  T = 1/T;
  T -= 273.15;
  return T;
}

//Modifica modalità 
void switchMode(){
  if(personDetected == true){
    AC[0] = AC_p[0];
    AC[1] = AC_p[1];
    H[0] = H_p[0];
    H[1] = H_p[1];
  }
  else{
    AC[0] = AC_np[0];
    AC[1] = AC_np[1];
    H[0] = H_np[0];
    H[1] = H_np[1];
  }
  return;
}

//Controllo presenze con sensore PIR
void checkPresence(){  
  int presence = digitalRead(PIR_PIN);
  if(presence == 1){    
    personDetected = true;
    last_presence = millis();
    switchMode();
  }
}

//Lettura dati microfono
void onPDMdata(){
  int bytesAvailable = PDM.available();
  PDM.read(sampleBuffer, bytesAvailable);
  samplesRead = bytesAvailable/2;
}

void printMic(){
  for(int i=0; i<samplesRead; i++){
    Serial.println(abs(sampleBuffer[i]));
    Serial.print("Min:0,Max:");
    Serial.println(clap_threshold);
  }
}

//Modifica soglie di temperatura 
void changeValue(String user_input){
  int space = user_input.indexOf(' ');

  if(space == -1){
    Serial.println("ERRORE NEL COMANDO");
    return;
  }

  String first = user_input.substring(0, space);
  float second = user_input.substring(space + 1).toFloat();

  Serial.println(first);
  Serial.println(second);

  if(first.equals("ACm")){
    AC_np[0] = second;
    return;
  }

  if(first.equals("ACM")){
    AC_np[1] = second;
    return;
  }
  if(first.equals("Hm")){
    H_np[0] = second;
    return;
  }
  if(first.equals("HM")){
    H_np[1] = second;
    return;
  }

  if(first.equals("ACmP")){
    AC_p[0] = second;
    return;
  }
  
  if(first.equals("ACMP")){
    AC_p[1] = second;
    return;
  }
  
  if(first.equals("HmP")){
    H_p[0] = second;
    return;
  }
  
  if(first.equals("HMP")){
    H_p[1] = second;
    return;
  }

  Serial.println("ERRORE NEL COMANDO");
  return;
}

//Controllo presenza con microfono
/*void checkSounds(){
    if(samplesRead){
    for(int i=0; i<samplesRead; i++){
      if(sampleBuffer[i] > abs(sound_threshold)){
        if(sound_events == 0)
          last_sound = millis();
        sound_events++;
        if(sound_events>n_sound_events){
          personDetected = true;
          switchMode();
        }
        break;
      }
    }
    samplesRead=0;
  }
  return;
}*/

//Controllo timeout PIR e microfono
void checkTimeout(){
  if(millis() - last_presence > timeout_pir /*&& millis() - last_sound > timeout_sound_max && personDetected*/){
    //sound_events = 0;
    personDetected = false;
    greenLedState = false;
    switchMode();
  }
}

//stampa valori a schermo
void printLCD(float light, float speed, float temp){
  int lightPerc, speedPerc;
  lightPerc = (light/255)*100;
  if(speed < offset)
    speedPerc = 0;
  else
    speedPerc = ((speed - offset)/(255 - offset))*100;
  lcd.clear();
  
  if(lcdState){
    lcd.print("T:");
    lcd.print(temp);
    lcd.print(" Pres:");
    lcd.print(personDetected);
    lcd.setCursor(0,1);
    lcd.print("AC:");
    lcd.print(speedPerc);
    lcd.print("% ");
    lcd.print("HT:");
    lcd.print(lightPerc);
    lcd.print("%");
  }

  else{
    lcd.print("AC m:");
    lcd.print(AC[0]);
    lcd.print(" M:");
    lcd.print(AC[1]);
    lcd.setCursor(0,1);
    lcd.print("HT m:");
    lcd.print(H[0]);
    lcd.print(" M:");
    lcd.print(H[1]);
  }
}

void switchScreen(uint lcd_time){
  TIMER_ISR_START(lcd_time);
  lcdState = !lcdState;
  TIMER_ISR_END(lcd_time);
}

//riconosce il doppio battito
bool clapDetected(){
  if(samplesRead){
    for(int i = 0; i < samplesRead; i++){
      if(sampleBuffer[i] > abs(clap_threshold) && millis() - last_clap >= 1000){
        Serial.print("CLAP! ");
        Serial.println(sampleBuffer[i]);
        Serial.println(millis());
        if (millis() - last_sound > 200 && millis() - last_sound < 500){
          Serial.print("TRUE! ");
          Serial.println(millis() - last_sound);
          last_sound=0;
          last_clap = millis();
          return true;
        }
        else
          last_sound = millis();
          return false;
      }
    }
  }
  return false;
}


void setup() {
  lcd.begin(16, 2);
  lcd.setBacklight(255);
  lcd.home();
  pinMode(FAN_PIN, OUTPUT);
  analogWrite(FAN_PIN, 0);
  pinMode(LED_PIN, OUTPUT);
  pinMode(PIR_PIN, INPUT);
  pinMode(GREEN_PIN, OUTPUT);
  Serial.begin(9600);
  while(!Serial);
  attachInterrupt(digitalPinToInterrupt(PIR_PIN), checkPresence, CHANGE);
  PDM.onReceive(onPDMdata);
  if(!PDM.begin(1, 16000)){
    Serial.println("Failed to start PDM");
    while(1);
  }
  ITimer1.setInterval(lcdPeriod*1000,switchScreen);
}
void loop(){
  // put your main code here, to run repeatedly:
  float temp = readTemp();
  float fs = fanSpeed(temp);
  float light = ledLight(temp);
  String user_input;

  if(Serial.available()){
    user_input = Serial.readString();
    changeValue(user_input);
  }

  if(clapDetected()){
    greenLedState = !greenLedState;
    last_sound = 0;
  }
  digitalWrite(GREEN_PIN, greenLedState);

  analogWrite(FAN_PIN, fs);
  analogWrite(LED_PIN, light);

  printLCD(light,fs,temp);
  //printMic();
  //Serial.print("AC: ");Serial.print(AC[0]); Serial.print(", "); Serial.println(AC[1]);
  //Serial.print("H: "); Serial.print(H[0]); Serial.print(", "); Serial.println(H[1]);

  checkTimeout();
  //checkSounds();
}
