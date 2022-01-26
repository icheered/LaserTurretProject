import sys
import select
import tiltPwm
from struct import unpack

PWM_TILT_PIN = 14
TILT_PWM_OPCODE = 0

tiltMotor = tiltPwm.tiltMotor(PWM_TILT_PIN)
tiltSpeed = 0

p = select.poll()
p.register(sys.stdin)
speed_dict = {-5: -43, -4: -32, -2: -24, -1: -16, 0: 0, 1: 12, 2: 18, 4: 24, 5: 36}
opcode = bytearray()
message = bytearray()
count = 0
while True:
	if (len(p.poll(0)) > 0):
		if count < 1:
			opcode += sys.stdin.buffer.read(1)
		else:
			message += sys.stdin.buffer.read(1)
		count += 1
	if (count > 2):
		print(message)
		if (opcode[0] == TILT_PWM_OPCODE):
			tiltSpeed = unpack('>h', message)
			tiltMotor.setTilt(int(speed_dict.get(tiltSpeed[0])/4))
		count = 0
		message = bytearray()
