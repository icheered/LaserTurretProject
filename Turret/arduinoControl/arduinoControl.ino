// operation codes
#define PAN_SPEED 2
#define PAN_ANGLE_REL 3
#define PAN_ANGLE_ABS 4

// speed settings
#define COUNT_LIM_NUMERATOR 1000 // maxspeed * 5 for max ~180RPM
#define ACCEL_CONSTANT 40
#define MIN_SPEED 4
#define MOVEMENT_DETECTION 7


// SETTINGS
int pulsePin = 11;
int dirPin = 10;
int maxSpeed = 100; // relatively arbitraty variable indicating max speed that can be set
int maxAcceleration = 8;
int maxAngle = 148;


// random variables
int incomingByte[3];
int speed, count, nextCountLim, stepsLeft, stepsNeededToStop;
int countLim = 5;
unsigned long pulseTime;

int nextOutput, nextDir, direction, nextSpeed;

volatile short setValue, setAngle, angle;
volatile byte opMode;
volatile bool braking;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  TCCR2A = 0b00000010;
  // 256 divisor
  TCCR2B = 0b00000110;
  // Sets 6.25Khz interrupt
  OCR2A = 9;
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
    noInterrupts();
    // check operation mode (speed or absolute angle)
    opMode = incomingByte[0];

    // retreive send value (16 bits)
    if (opMode == PAN_SPEED) {
      setValue = (incomingByte[1]<<8) + (incomingByte[2]); 
      Serial.println(setValue);
    } else if (opMode == PAN_ANGLE_ABS) {
      setAngle = (incomingByte[1]<<8) + (incomingByte[2]); 
      braking = false;
      Serial.println(setAngle);
    } else if (opMode == PAN_ANGLE_REL) {
      braking = false;
      setAngle = angle + (incomingByte[1]<<8) + (incomingByte[2]); 
      Serial.println(setAngle);
    } else if (opMode == MOVEMENT_DETECTION) {
        short receivedAngle = (incomingByte[1]<<8) + incomingByte[2];
        short transformedAngle = angle;
        if (angle < 0) {
            transformedAngle = 148 - angle
        }
        short difference = transformedAngle - receivedAngle
        // Turn left
        if ((difference > 0 && ((transformedAngle - receivedAngle) < 74))
            || (difference < 0 && (abs(transformedAngle - receivedAngle) > 74)) ) {
            setValue = -10;
        } else {
            // Turn right
            setValue = 10;
        }
        Serial.println(setValue);

    }
    interrupts();
  }
}

int stepsToStop() {
  int calcValue = ((speed*speed) / 72);
  return calcValue; // 2083/15
}

// determine if we should decelerate to avoid going over limit
bool approachingLimits(byte operationMode) {
  // calculate steps left
  stepsLeft = maxAngle - abs(angle);
  // check if allready at max
  if (stepsLeft <= 0 && operationMode == PAN_SPEED) {
    if (angle > 0 && setValue < 0) {
      return false;
    } else if (angle < 0 && setValue > 0) {
      return false;
    } else {
      //Serial.println(setValue);
      return true;
    }
  }
  if (stepsLeft <= 0 && (operationMode == PAN_ANGLE_ABS || operationMode == PAN_ANGLE_REL)) {
    if (abs(setAngle) < maxAngle) {
      return false;
    }
  }
  // if stopped, return false
  if (speed == 0) {
    return false;
  }
  // if going in the opposite direction, return false
  if (direction == 1 && angle < 0) {
    return false;
  }
  if (direction == 0 && angle > 1) {
    return false;
  }
  // see if we need to stop / slow down
  if (stepsToStop() >= stepsLeft) { // apparently not +1???
    return true;
  } 
}



// Maximum deceleration function
// int 0 means ccw, 1 means cw
void maxAccelerate(int rotDirection) {
  if (rotDirection == 1) {
    nextSpeed = speed + (countLim / ACCEL_CONSTANT) + 1;
    if (nextSpeed > maxSpeed) nextSpeed = maxSpeed;
    if (abs(nextSpeed) < MIN_SPEED) nextSpeed = 0;
    //nextSpeed = (abs(speed + maxAcceleration) <= maxSpeed) ? speed + maxAcceleration : maxSpeed;
  } else if (rotDirection == 0) {
    nextSpeed = speed - (countLim / ACCEL_CONSTANT) - 1;
    if (nextSpeed < -maxSpeed) nextSpeed = -maxSpeed;
    if (abs(nextSpeed) < MIN_SPEED) nextSpeed = 0;
    //nextSpeed = (abs(speed - maxAcceleration) <= maxSpeed) ? speed - maxAcceleration : -maxSpeed;
  }
  nextDir = nextSpeed > 0 ? 1 : 0;
  nextCountLim = nextSpeed != 0 ? COUNT_LIM_NUMERATOR/abs(nextSpeed) : COUNT_LIM_NUMERATOR/MIN_SPEED;
}

void stopToZero() {
  if (direction == 1) {
    nextSpeed = speed - (countLim / ACCEL_CONSTANT) - 1;
    if (nextSpeed < MIN_SPEED) nextSpeed = 0;
    //nextSpeed = (speed - maxAcceleration) > 10 ? speed - maxAcceleration : 0;
  } else if (direction == 0) {
    nextSpeed = speed + (countLim / ACCEL_CONSTANT) + 1;
    if (nextSpeed > -MIN_SPEED) nextSpeed = 0;
    //nextSpeed = (speed + maxAcceleration) < -10 ? speed + maxAcceleration : 0;
  }
  nextDir = direction;
  nextCountLim = nextSpeed != 0 ? COUNT_LIM_NUMERATOR/abs(nextSpeed) : COUNT_LIM_NUMERATOR/MIN_SPEED;
}

void accelerateToValue(int accelValue) {
  nextSpeed = accelValue;
  nextDir = accelValue > 0 ? 1 : 0;
  nextCountLim = COUNT_LIM_NUMERATOR/(abs(nextSpeed));
}


//Speed control implementation 
void speedControl() {
  setValue = setValue <= maxSpeed ? setValue : maxSpeed;
  setValue = setValue >= -maxSpeed ? setValue : -maxSpeed;
  if (abs(setValue) < MIN_SPEED) {
    stopToZero();
  }
  else if (abs(setValue - speed) > maxAcceleration) {
    if ((setValue - speed) > 0) {
      maxAccelerate(1);
    } else if ((setValue - speed) < 0) {
      maxAccelerate(0);
    }
  }
  else {
    accelerateToValue(setValue);
  }
}


// Absolute ngle control implementation
void angleControlAbs() {
  stepsLeft = setAngle - angle;
  stepsNeededToStop = stepsToStop();;
  // check if allready at angle
  if (stepsLeft == 0) {
    nextSpeed = 0;
    nextCountLim = COUNT_LIM_NUMERATOR/MIN_SPEED;
  }
  else if (stepsNeededToStop + 1 >= abs(stepsLeft)) {
    braking = true;
    stopToZero();
  }
  else if (stepsLeft > 1 && braking == false) {
    maxAccelerate(1);
  }
  else if (stepsLeft < 1 && braking == false) {
    maxAccelerate(0);
  }

}


//ISR(TIMER2_OVF_vect) {
//  count = count + 1;
//}

// 6.25Khz timer interrupt
ISR(TIMER2_COMPA_vect) {
  static bool dirChangeTimeout;
  noInterrupts();
  // increment iteration counter
  count++;
  // write current output values to pins
  digitalWrite(pulsePin, nextOutput);
  digitalWrite(dirPin, nextDir);
  // reset counter if limit is achieved, and set next output to HIGH
  if (nextOutput == 1 && count <=4) {
    nextOutput = 1;
  }
  else if (count >= countLim) {
    dirChangeTimeout = false;
    //Serial.println(setValue);
    count = 0;
    countLim = nextCountLim;
    // check to prevent motor pulse if allready standing still
    nextOutput = ((speed == nextSpeed) && (nextSpeed == 0)) ? 0 : 1;
    if (!((speed == nextSpeed) && (nextSpeed == 0))) {
      angle = (nextDir == 1) ? angle + 1 : angle - 1;
      //Serial.println(nextSpeed);
    }
    speed = nextSpeed;
    direction = nextDir;
    //Serial.println(speed);
  } else {
    // write 0 next interrupt if not taking a step
    nextOutput = 0;
  }
  // evaluate if needing to break due to hitting limit
  if (approachingLimits(opMode)) {
    stopToZero();
  } else if (opMode == PAN_SPEED) { // Speed control
    speedControl();
  } else if (opMode == PAN_ANGLE_REL) { // angle control
    angleControlAbs();
  } else if (opMode == PAN_ANGLE_ABS) {    
    angleControlAbs();
  }
  if (nextDir != direction && dirChangeTimeout == false) {
    count -= 1000;
    dirChangeTimeout = true;
  }
  interrupts();
}
