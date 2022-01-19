#include<SoftwareSerial.h>
SoftwareSerial swsri(3,4);
int angle, speed;
int direction=1;
int nextPwm = 50;
int maxAcc = 40;

char string[2];

void setup() {
  // put your setup code here, to run once:
  swsri.begin(9600);
  //pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  TCCR0A=0b00100011;
  TCCR0B=0b00001101;
  OCR0A=50;
  OCR0B=1;
  TIMSK=0b01001100;

  TCCR1=0b10001111;
  GTCCR=0b00000000;
  OCR1C=48;
  OCR1A=10;
  
}

void loop() {
  // put your main code here, to run repeatedly:
}

/*ISR(TIMER0_COMPB_vect) {
   angle = direction=1? angle+1 : angle-1;
}*/

ISR(TIMER1_COMPA_vect) {
    OCR0A=nextPwm;
    int input1 = swsri.read();
    int input21 = swsri.read();
    int input22 = swsri.read();
    
    // speed control
    if (input1 != -1 && input1 == 1) {
        if (input21 !=-1 && input22 !=-1) {
          int setSpeed = input21 << 8 + input22;
          setSpeed = setSpeed*5;
          if (setSpeed > 30) {
            direction=1;
            nextPwm = 7905 / setSpeed;
          } else if (setSpeed < -30) {
            direction=0;
            nextPwm = 7905 / setSpeed;
          }
          else {
            speed = 0;
          }
        }
    // angle control
    } else if (input1 != -1 && input1 == 1) {

    }
}
