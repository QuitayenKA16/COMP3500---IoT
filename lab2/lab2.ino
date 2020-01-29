/***********************************/
/* Karamel Quitayen                */
/* COMP3500 - Special Topics (IoT) */
/* Lab 2                           */
/***********************************/

//constants to set pin numbers
#define LED 4     //define led pin var
#define BUTTON 5  //define button pin var

//variable to keep track of button state
int buttonState = 0;

void setup() {
  //setup BUTTON pin for input
  pinMode(BUTTON, INPUT);
  
  //setup LED pin for output
  pinMode(LED, OUTPUT);
}

void loop() {
  //read state of button value
  buttonState = digitalRead(BUTTON);

  //check if button is pressed 
  if (buttonState == HIGH){
    //turn LED on
    digitalWrite(LED, HIGH);
    Serial.println("LED on");
  }
  else { //(buttonState == LOW)
    //turn LED off
    digitalWrite(LED, LOW);
    Serial.println("LED off");
  }

}
