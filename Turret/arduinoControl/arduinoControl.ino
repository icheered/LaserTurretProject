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

volatile int setValue;
volatile bool opMode = false;

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
    if (incomingByte[0] == 1) opMode = true;
    if (incomingByte[0] == 0) opMode = false;
    // retreive send value (16 bits)
    setValue = (incomingByte[1]<<8) + (incomingByte[2]); 
    Serial.println(setValue);
  }
}


//ISR(TIMER2_OVF_vect) {
//  count = count + 1;
//}

// 6.25Khz timer interrupt
ISR(TIMER2_COMPA_vect) {
  // increment iteration counter
  count = count + 1;
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
  if ((speed/(stepsLeft)) >= maxAcceleration || (stepsLeft == 0 && speed !=0) || stepsLeft == 1) {
    // set next speed
    if ((speed - maxAcceleration) > 0) {
      nextSpeed = speed-maxAcceleration;
      nextCountLim = 2550/abs(nextSpeed);
      enable = true;
    } else {
      enable = false;
      speed = 0;
    }
  } else if (opMode == false) { // Speed control
    // check if speed is too small
      if (abs(setValue - speed) > maxAcceleration) { // acceleration / deceleration limiter
      // set max acceleration to 40 Hz and check direction
      nextSpeed = ((setValue - speed) > 0) ? (speed + maxAcceleration) : (speed-maxAcceleration);
      // Set direction
      nextDir = (nextSpeed) > 0 ? 1 : 0;
      // calculate next count limit for speed
      nextCountLim = 2550/abs(nextSpeed);
      enable = true;
    } else if (abs(setValue) < 5) {
      enable = false;
      speed = 0;
    } else {
      enable = true;
      nextSpeed = setValue;
      nextDir = (nextSpeed) > 0 ? 0 : 1;
      nextCountLim = 2550/abs(nextSpeed);
      //Serial.println(nextSpeed);
    }
  } else if (opMode == true) { // angle control
    int stepsLeft = abs(setValue - angle);
    if (setValue - angle < 0 && direction == 1) {
      // need to change direction
      if ((speed - maxAcceleration) > 0) {
        
      }
    } else {
      // going into right direction allready
      // Check if we have to decelerate
      if ((speed/(stepsLeft+1)) > maxAcceleration) {
        // set next speed
        nextSpeed = (speed - maxAcceleration) > 0 ? maxAcceleration : 0;
        // calculate next count limit for speed
        nextCountLim = 2550/abs(nextSpeed);
        enable = true;
      } else if (false) {
        // we can speed up
      }
    }
  }
}
