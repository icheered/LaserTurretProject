from machine import PWM
from machine import Pin


class tiltMotor():
    def __init__(self, PWM_TILT_PIN):
        self.pin = PWM_TILT_PIN
        self.pwm = PWM(Pin(self.pin),freq=50,duty=77)

    def setTilt(self,tiltSpeed):
        if (abs(tiltSpeed) > 25):
            tiltSpeed = 25 if tiltSpeed > 0 else -25
        period = tiltSpeed + 77
        self.pwm.duty(period)

    def __del__(self):
        self.pwm.deinit()
