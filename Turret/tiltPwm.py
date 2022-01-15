from machine import PWM
from machine import Pin


class tiltMotor():
    def __init__(self, PWM_TILT_PIN):
        self.pin = PWM_TILT_PIN
        # Init to standstill
        self.pwm = PWM(Pin(self.pin),freq=50,duty=77)

    def setTilt(self,tiltSpeed):
        # Set upper and lower bounds
        tiltSpeed = 25 if tiltSpeed > 25 else tiltSpeed
        tiltSpeed = -26 if tiltSpeed < -26 else tiltSpeed
        # rewrite to correct period
        period = tiltSpeed + 77
        self.pwm.duty(period)

    def __del__(self):
        self.pwm.deinit()
