const int LED_PIN = 2;
const int PIR_PIN = 4;

volatile int tot_count = 0;

void setup() {
  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(PIR_PIN), checkPresence, CHANGE);
  while(!Serial);
  Serial.println("Lab 1.3 Starting");
}

void checkPresence(){  
  int led_state = digitalRead(PIR_PIN);
  digitalWrite(LED_PIN, led_state); 
  if(led_state == 1){    
    tot_count++;
  }
}


void loop() {
     Serial.print("Total people count: ");
     Serial.println(tot_count);
     delay(30000);
}
