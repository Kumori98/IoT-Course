#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "arduino_secrets.h"

const int led_pin = A2, temp_pin = A1;
const int B = 4275;  const long int R0 = 100000;

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;

String broker_address = "test.mosquitto.org";
int broker_port = 1883;

const String base_topic = "/tiot/group6";

int status = WL_IDLE_STATUS;

float readTemp(){
  float a = analogRead(temp_pin);
  float R = (1023/a - 1) * R0;
  float T = log(R/R0)/B + 1/298.15;
  T = 1/T;
  T -= 273.15;
  return T;
}

const int capacity = JSON_OBJECT_SIZE(2) + JSON_ARRAY_SIZE(4) + 100;
DynamicJsonDocument doc_snd(capacity);
DynamicJsonDocument doc_rec(capacity);

void callback(char* topic, byte* payload, unsigned int lenght) {
  DeserializationError err = deserializeJson(doc_rec, (char*) payload);
  if(err){ //Se ho errore
    Serial.print(F("deserializeJson() failed with code "));
    Serial.println(err.c_str());
  }

  if(doc_rec["e"][0]["n"] == "led"){
    int value = doc_rec["e"][0]["v"];
    digitalWrite(led_pin, value);
  }
}

WiFiClient wifi;
PubSubClient client(broker_address.c_str(), broker_port, callback, wifi);

String senMlEncode(String res, float v, String unit){
  doc_snd.clear();
  doc_snd["bn"] = "ArduinoGroup6";
  doc_snd["e"][0]["t"] = int(millis()/1000);
  doc_snd["e"][0]["n"] = res;
  doc_snd["e"][0]["u"] = unit;
  doc_snd["e"][0]["v"] = v;

  String output;
  serializeJson(doc_snd, output); //il json creato viene buttato al broker
  return output;
}

void reconnect(){
  
  while(client.state() != MQTT_CONNECTED){
    if(client.connect("TiotGroup6")){
      client.subscribe((base_topic + String("/led")).c_str());
    }
    else{
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println("try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
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
}

void loop() {

  if(client.state() != MQTT_CONNECTED){
    reconnect();
  }

  String body = senMlEncode("temperature", readTemp(), "Cel");
  client.publish((base_topic + String("/temperature")).c_str(), body.c_str());
  Serial.println("Mandato");
  client.loop();
  delay(5000);

}