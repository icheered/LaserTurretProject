import tiltPwm
import time

PWM_TILT_PIN = 14

tiltMotor = tiltPwm.tiltMotor(PWM_TILT_PIN)
while True:
    tiltMotor.setTilt(0)
    print("Set stop")
    time.sleep(1)
    tiltMotor.setTilt(25)
    print("Set forward")
    time.sleep(1)
    tiltMotor.setTilt(-25)
    print("Set backward")
    time.sleep(1)
