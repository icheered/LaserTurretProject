import sys
import select
import tiltPwm

PWM_TILT_PIN = 14
TILT_PWM_OPCODE = 0

tiltMotor = tiltPwm.tiltMotor(PWM_TILT_PIN)
tiltSpeed = 0

p = select.poll()
p.register(sys.stdin)
message = bytearray()
count = 0
while True:
	if (len(p.poll(0)) > 0):
		message += sys.stdin.buffer.read(1)
		count += 1
	if (count > 2):
		print(message)
		if (message[0] == TILT_PWM_OPCODE):
			tiltSpeed = message[2] + (message[1]<<8)
			tiltMotor.setTilt(int(tiltSpeed/4))
			print(tiltSpeed)
		count = 0
		message = bytearray()
