// SETTINGS
int pulsePin = 11;
int dirPin = 10;
int maxSpeed = 170;
int maxAcceleration = 17;
int maxAngle = 148;


// random variables
int incomingByte[3];
int angle, speed, count; 
int countLim, nextCountLim;

bool enable; // false = speed, true = angle;
int nextOutput, nextDir, direction, nextSpeed;

volatile short setValue;
volatile byte opMode;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  TCCR2A = 0b00000010;
  // 256 divisor
  TCCR2B = 0b00000110;
  // Sets 6.25Khz interrupt
  OCR2A = 10;
  ASSR &= ~(1<<AS2);
  // enable interrupts
  TIMSK2 = 0b00000011;

  // Set output pins
  pinMode(pulsePin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

void loop() {
  // check if 3 or more bytes are available
  if (Serial.available() > 2) {
    // read first three bytes
    for (int i=0; i<3; i++) {
      incomingByte[i] = Serial.read();
    }
    // check operation mode (speed or absolute angle)
    opMode = incomingByte[0];

    // retreive send value (16 bits)
    setValue = (incomingByte[1]<<8) + (incomingByte[2]); 
    Serial.println(setValue);
  }
}

// determine if we should decelerate to avoid going over limit
bool approachingLimits() {

}


// Maximum deceleration function
void maxAccelerate(int direction) {

}


//Speed control implementation 
void speedControl() {

}


// Angle control implementation
void angleControlAbs() {

}


// Angle control implementation relative
void angleControlRel() {

}


//ISR(TIMER2_OVF_vect) {
//  count = count + 1;
//}

// 6.25Khz timer interrupt
ISR(TIMER2_COMPA_vect) {
  // increment iteration counter
  count++;
  // write current output values to pins
  digitalWrite(pulsePin, nextOutput);
  digitalWrite(dirPin, nextDir);
  // reset counter if limit is achieved, and set next output to HIGH
  if (count >= countLim && enable == true) {
    Serial.println(setValue);
    count = 0;
    countLim = nextCountLim;
    nextOutput = 1;
    speed = nextSpeed;
    direction = nextDir;
    angle++;
    //Serial.println(speed);
  } else {
    // write 0 next interrupt if not taking a step
    nextOutput = 0;
  }
  // calculate steps left until hitting limit
  int stepsLeft = abs(angle) - maxAngle;
  // evaluate if needing to break due to hitting limit
  if (approachingLimits()) {
    maxAccelerate(0);
  } else if (opMode == 0) { // Speed control
    speedControl();
  } else if (opMode == 1) { // angle control
    angleControlRel();
  } else if (opMode == 2) {
    angleControlAbs();
  }
}
