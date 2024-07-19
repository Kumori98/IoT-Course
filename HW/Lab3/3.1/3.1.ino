#include <WiFiNINA.h>
#include "arduino_secrets.h"

const int B = 4275;  const long int R0 = 100000;

const int led_pin = A2, temp_pin = A1;

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;

int status = WL_IDLE_STATUS;
WiFiServer server(80);

float readTemp(){
  float a = analogRead(temp_pin);
  float R = (1023/a - 1) * R0;
  float T = log(R/R0)/B + 1/298.15;
  T = 1/T;
  T -= 273.15;
  return T;
}

void process(WiFiClient client){
  String req_type = client.readStringUntil(' ');
  req_type.trim();
  String url = client.readStringUntil(' ');
  url.trim();

  if(url.startsWith("/led")){
    String led_val = url.substring(5);
    if(led_val == "0" || led_val == "1"){
      int int_val = led_val.toInt();
      digitalWrite(led_pin, int_val);
      printResponse(client, 200, senMlEncode("led", int_val, ""));
    }
    else {
      printResponse(client, 400, "Bad request");
    }
  }
  else if(url.startsWith("/temperature")){
      printResponse(client, 200, senMlEncode("temperature", readTemp(), "Cel"));
  }
  else
    printResponse(client, 404, "Not Found");
}

void printResponse(WiFiClient client, int code, String body){
  client.println("HTPP/1.1 " + String(code));

  if(code == 200){
    client.println("Content-type : application/json; charset=uft-8");
    client.println();
    client.println(body);
  }
  else{
    client.println("Content-type : application/json; charset=uft-8");
    client.println();
    client.println(body); //gestione errori
  }
}

String senMlEncode(String property, float value, String unit){
  String output = "{\"bn\": \"ArduinoGroup6\", \"e\":[{ \"t\": ";
  output.concat(String(millis()));
  output.concat(",\"n\": ");
  if(property == "led"){
    output.concat("\"led\", \"v\": ");
    output.concat(String(value));
    output.concat(", \"u\": null");
  }
  else{
    output.concat("\"temperature\", \"v\": ");
    output.concat(String(value));
    output.concat(", \"u\": \"Cel\"");
  }
  output.concat("}]}");
  return output;
}


void setup() {
  // put your setup code here, to run once:
  pinMode(led_pin, OUTPUT);
  pinMode(temp_pin, INPUT);


  while(status != WL_CONNECTED){
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }

  Serial.print("Connect with IP Address: ");
  Serial.println(WiFi.localIP());

  server.begin();

}

void loop() {
  // put your main code here, to run repeatedly:

  WiFiClient client = server.available();
  if(client) {
    process(client);
    client.stop();
  }
  delay(50);
}
