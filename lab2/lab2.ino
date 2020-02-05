/***********************************/
/* Karamel Quitayen                */
/* COMP3500 - Special Topics (IoT) */
/* Lab 2                           */
/***********************************/

//constants to set pin numbers
#define LED 5     //define led pin var
#define BUTTON 4  //define button pin var

//flag variable to keep track of button state
int light = HIGH;
int prevState = LOW;

void setup() {
  //setup BUTTON pin for input
  pinMode(BUTTON, INPUT);
  
  //setup LED pin for output
  pinMode(LED, OUTPUT);

  Serial.begin(115200);
}

void loop() {
  // read button state
  int currState = digitalRead(BUTTON);

  // if button toggled 
  if (currState == HIGH && prevState == LOW){
    Serial.println("button press");
    if (light == HIGH)  //if LED was off
      light = LOW;      //turn it on
    else                //if LED was on
      light = HIGH;     //turn it off
  }

  //set button state (on or off) based on above logic
  digitalWrite(LED, light);

  //update previous state
  prevState = currState;
}
