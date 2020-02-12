/***********************************/
/* Karamel Quitayen                */
/* COMP3500 - Special Topics (IoT) */
/* Lab 4                           */
/***********************************/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi/MQTT parameters
#define WLAN_SSID       "NETGEAR87"
#define WLAN_PASS       "I1t9t7r5litjf?"
#define BROKER_IP       "192.168.0.19"

//constant for analog sensor
#define SENSOR A0

// wifi client and mqtt client
WiFiClient client;
PubSubClient mqttclient(client);

// variables
int lightstate;

void setup() {
  Serial.begin(115200);
  
  // connect to wifi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(F("."));
  }

  // print wifi info
  Serial.println(F("WiFi connected"));
  Serial.println(F("IP address: "));
  Serial.println(WiFi.localIP());

  // connect to mqtt server
  mqttclient.setServer(BROKER_IP, 1883);
  connect();
}

void loop() {
  // make sure mqqt is connected
  if (!mqttclient.connected()) {
    connect();
  }

  // run client
  mqttclient.loop();

  // vars to keep track of time
  static const unsigned long REFRESH_INTERVAL = 1000; //ms
  static unsigned long lastRefreshTime = 0;

  // if elapsed update time more than time interval
  if (millis() - lastRefreshTime >= REFRESH_INTERVAL){

    // update refresh time
    lastRefreshTime += REFRESH_INTERVAL;
    
    // read analog state
    lightstate = analogRead(SENSOR);
    
    // publish to pi light sensor value
    mqttclient.publish("/sensor", (char *)lightstate, false);
  }
}

// connect to mqtt
void connect() {
  
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println(F("Wifi issue"));
    delay(3000);
  }
  
  Serial.print(F("Connecting to MQTT server... "));
  while(!mqttclient.connected()) {
    if (mqttclient.connect(WiFi.macAddress().c_str())) {
      Serial.println(F("MQTT server Connected!"));
    }
    
    else {
      Serial.print(F("MQTT server connection failed! rc="));
      Serial.print(mqttclient.state());
      Serial.println("try again in 10 seconds");
      // Wait 5 seconds before retrying
      delay(20000);
    }
  }
}
