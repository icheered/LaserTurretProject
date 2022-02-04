import sys
import select
import tiltPwm
from struct import unpack

PWM_TILT_PIN = 14
TILT_PWM_OPCODE = 0

# instantiate tiltMotor instance and set speed to 0 
tiltMotor = tiltPwm.tiltMotor(PWM_TILT_PIN)
tiltSpeed = 0

# Enable polling to check how many bytes in buffer
p = select.poll()
p.register(sys.stdin)
# Dict that corrolates input speed to PWM speed
speed_dict = {-5: -43, -4: -32, -2: -24, -1: -16, 0: 0, 1: 12, 2: 18, 4: 24, 5: 36}
opcode = bytearray()
message = bytearray()
count = 0
while True:
	# Check if byte is available at UART interface
	if (len(p.poll(0)) > 0):
		# Read first byte as opcode
		if count < 1:
			opcode += sys.stdin.buffer.read(1)
		# Read other bytes as value
		else:
			message += sys.stdin.buffer.read(1)
		count += 1
	# If 3 bytes have been received check for correct opcode and write value to PWM motor
	if (count > 2):
		if (opcode[0] == TILT_PWM_OPCODE):
			tiltSpeed = unpack('>h', message)
			tiltMotor.setTilt(int(speed_dict.get(tiltSpeed[0])/4))
		count = 0
		message = bytearray()
