/***********************************/
/* Karamel Quitayen                */
/* COMP3500 - Special Topics (IoT) */
/* Lab 2                           */
/***********************************/

//constants to set pin numbers
#define LED 4     //define led pin var
#define BUTTON 2  //define button pin var

//flag variable to keep track of LED state
int currentState = 0;

void setup() {
  //setup BUTTON pin for input
  pinMode(BUTTON, INPUT);
  
  //setup LED pin for output
  pinMode(LED, OUTPUT);
}

void loop() {
  //read state of button value
  int buttonState = digitalRead(BUTTON);
  Serial.println(buttonState);

  //check if button is pressed 
  if (buttonState == HIGH){
     if (currentState == 0){    //LED currently OFF
      digitalWrite(LED, HIGH);  //turn LED on
      currentState = 1;         //update currentState flag to OFF
      Serial.println("LED on");
    }
    else {                      //LED current ON
      digitalWrite(LED, LOW);   //turn LED off
      currentState = 0;         //update currentState flag to ON
      Serial.println("LED off");
    }
  }

}
