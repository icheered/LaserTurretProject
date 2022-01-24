
#include <IRremoteESP8266.h>
#include <IRsend.h>
IRsend irsend(4);

#define encoderA 12   // D5
#define encoderB 14   // D6
#define encoderBTN 13 // D7
#define sendBTN 15    // D8

int aState;
int aLastState;  
int rotaryButtonState;
int sendButtonState;

int inValue = 0; // Keep track of changing state or value
int state = 0; // 0: Change team, 1: Change ammo, 2: Change lives
int value = 0;



void setup() {
  Serial.begin(115200, SERIAL_8N1, SERIAL_TX_ONLY);
  
  pinMode (encoderA,INPUT);
  pinMode (encoderB,INPUT);
  pinMode (encoderBTN,INPUT);
  aLastState = digitalRead(encoderA);
  rotaryButtonState = digitalRead(encoderBTN);
  
  irsend.begin();
}

int i = 0;
void loop() {
  
  i += 1;
  int encoderChange = getEncoderChange();
  updateStateOrValue(encoderChange);
  updateRotaryClicked();
  
  sendValue();

  if(i == 5000) {
    Serial.print("InValue: ");
    Serial.print(inValue);
    Serial.print(", State: ");
    Serial.print(state);
    Serial.print(", Value: ");
    Serial.println(value);
    i = 0;
  }
  
}

void updateRotaryClicked() {
  int readVal = digitalRead(encoderBTN);
  if(rotaryButtonState != readVal){
    if(rotaryButtonState) { // Pin went LOW (pressed down)
      inValue = !inValue;
    }
    rotaryButtonState = readVal;
  }
}

void sendValue() {
  int readVal = digitalRead(sendBTN);
  if(sendButtonState != readVal){
    if(readVal) { // Pin went HIGH (pressed down)
      Serial.print("Sending! Address: ");
      Serial.print(state);
      Serial.print(", Value: ");
      Serial.println(value);
      irsend.sendNEC(irsend.encodeNEC(state, value), 32);
    }
    sendButtonState = readVal;
  }
}

void updateStateOrValue(int encoderChange) {
  // Use encoder value to change the state or value parameter
  if(encoderChange == -1 || encoderChange == 1) {
    if(!inValue) { // Changing state
      state = (state + encoderChange) % 3;
      if(state < 0) {state = 0;}
      value = 0;
    } else { // Changing value
      if(state == 0) { value = (value + encoderChange) % 3;}      // Changing team
      else if(state == 1) { value = (value + encoderChange) % 99;}// Changing ammo
      else if(state == 2) { value = (value + encoderChange) % 9;} // Changing lives
      if(value < 0) {value = 0;}
    }
  }
}

int getEncoderChange() {
  // Check if the encoder has rotated
  aState = digitalRead(encoderA); 
  int returnVal = 0;
  if (aState != aLastState){     
    if (digitalRead(encoderB) != aState) { 
      returnVal = -1;
    } else {
      returnVal = 1;
    }
  } 
  aLastState = aState;
  return returnVal;
}
