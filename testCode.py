import serial
import time

uart = serial.Serial("/dev/ttyACM0",115200)
count = 0
while count<10:
	uart.write(b'\x04' + int(100).to_bytes(2,'big',signed=True))
	print("sleep")
	time.sleep(1)
	uart.write(b'\x04' + int(0).to_bytes(2,'big',signed=True))
	time.sleep(1)
	count += 1
