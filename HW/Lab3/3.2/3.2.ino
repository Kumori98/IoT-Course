#include <WiFiNINA.h>
#include "arduino_secrets.h"
#include <ArduinoHttpClient.h>

char server_address[] = "192.168.147.12"; //ip del computer
int server_port = 8080;

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;

int status = WL_IDLE_STATUS;

WiFiClient wifi;
HttpClient client = HttpClient(wifi, server_address, server_port);

const int B = 4275;  const long int R0 = 100000, temp_pin = A1;

float readTemp(){
  float a = analogRead(temp_pin);
  float R = (1023/a - 1) * R0;
  float T = log(R/R0)/B + 1/298.15;
  T = 1/T;
  T -= 273.15;
  return T;
}

String senMlEncode(float value){
  String output = "{\"bn\": \"ArduinoGroup6\", \"e\":[{ \"t\": ";
  output.concat(String(millis()));
  output.concat(",\"n\": ");
  output.concat("\"temperature\", \"v\": ");
  output.concat(String(value));
  output.concat(", \"u\": \"Cel\"");
  output.concat("}]}");
  return output;
}

void setup() {
  // put your setup code here, to run once:

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
  String body = senMlEncode(readTemp());
  client.beginRequest();
  client.post("/log");
  client.sendHeader("Content-type", "application/json");
  client.sendHeader("Content-Length", body.length());
  client.beginBody();
  client.print(body); //punto da svolgere
  client.endRequest();
  int ret = client.responseStatusCode();
  Serial.println(ret);
  delay(10000);
}
