// Este programa envia por medio de una url los datos de humedad y temperatura

#include "DHT.h"
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

#define DHTPIN 0     // D3 en la tarjeta
#define DHTTYPE DHT11   // DHT 11 tipo de sensor humedad temperatura

const char* ssid = "xxxx";
const char* password = "xxxx";
String serverName = "https://url_deploy:8080/get_data_esp/";
String source = "'Sensor2'";

WiFiClient wifiClient;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  // Conexión wifi
  while (WiFi.status() != WL_CONNECTED) {

    delay(1000);
    Serial.println("Connecting..");

    }

  // Mensaje exito conexión
  Serial.println("======================================");
  Serial.print("Conectado a:\t");
  Serial.println(WiFi.SSID());
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());
  Serial.println("======================================");

  dht.begin();
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);


  int h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h, false);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h);

  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status

    HTTPClient http;  //Declare an object of class HTTPClient
    String serverPath = serverName + "?humidity=" + h + "&temp=" + t + "&source=" + source;

    http.begin(wifiClient, serverPath);                         //Specify request destination
    int httpCode = http.GET();                                  //Send the request
    Serial.println("request OK");

    if (httpCode > 0) { //Check the returning code

      String payload = http.getString();   //Get the request response payload
      Serial.println(payload);             //Print the response payload

  }

  http.end();   //Close connection

}

  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.println(F("°C "));
  Serial.println(serverName + "?humidity=" + h + "&temp=" + t + "&source=" + source);


  delay(30000); // Espera de un minuto entre dato y dato
}