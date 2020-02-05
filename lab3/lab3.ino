/***********************************/
/* Karamel Quitayen                */
/* COMP3500 - Special Topics (IoT) */
/* Lab 3                           */
/***********************************/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi/MQTT parameters
#define WLAN_SSID       "NameOfNetwork"
#define WLAN_PASS       "applepie"
#define BROKER_IP       "192.168.0.19"

//constants to set pin numbers
#define LED 5
#define BUTTON 4

// wifi client and mqtt client
WiFiClient client;
PubSubClient mqttclient(client);

// flags to keep track of LED/Button states
int ledState = HIGH;
char* prevState = "off";

void callback (char* topic, byte* payload, unsigned int length) {
  Serial.println(topic);
  Serial.write(payload, length); //print incoming messages
  Serial.println("");

  // add null terminator to byte payload to treat as string
  payload[length] = '\0';
  
  // TOGGLE LOGIC FROM ASSIGNMENT 2
  char* currState = (char *) payload;
    
  if (strcmp(currState, "on") == 0 && strcmp(prevState, "off") == 0)
    ledState = (ledState == HIGH ? LOW : HIGH);

  digitalWrite(LED, ledState);
  prevState = currState;
}

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
  mqttclient.setCallback(callback);
  connect();

  // setup pins
  pinMode(LED, OUTPUT);   //set LED pin as output
  pinMode(BUTTON, INPUT); //set button pin as input
  
}

void loop() {
  // make sure mqqt is connected
  if (!mqttclient.connected()) {
    connect();
  }

  // run client
  mqttclient.loop();
  
  // read current button state
  if (digitalRead(BUTTON) == HIGH)
    // tell Pi button was toggled on
    mqttclient.publish("/button", "on", false);
  else
    // tell Pi button was toggled off
    mqttclient.publish("/button", "off", false);
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
      mqttclient.subscribe("/button"); // subscribe to topic
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
