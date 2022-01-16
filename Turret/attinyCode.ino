#include<SoftwareSerial.h>
SoftwareSerial swsri(3,4);
int angle;
int direction=1;

char string[2];

void setup() {
  // put your setup code here, to run once:
  swsri.begin(9600);
  //pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  TCCR0A=0b00100011;
  TCCR0B=0b00001101;
  OCR0A=6;
  OCR0B=1;
  TIMSK=0b01001100;

  TCCR1=0b10001111;
  GTCCR=0b00000000;
  OCR1C=49;
  OCR1A=10;
  
}

void loop() {
  // put your main code here, to run repeatedly:
}

ISR(TIMER0_COMPB_vect) {
  // angle = direction=1? angle+1 : angle-1;
}

ISR(TIMER1_COMPA_vect) {
    char input1 = swsri.read();
    char input2 = swsri.read();
    string[0] = input1; string[1] = input2;
    if (input1 != -1 && input2 != -1) {
      swsri.print(input1);
      swsri.print(input2);
    }
}
