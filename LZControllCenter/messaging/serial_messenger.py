"""codeauthor:: Brand Hauser"""

import serial


class Messenger:
    def __init__(self):
        self.port = None  # Find correct port on computer and enter name
        self.ser = serial.Serial()
        self.ser.port = self.port
        self.ser.baudrate = 19200

    def send(self, msg):
        self.ser.open()
        self.ser.write(msg)
        self.ser.close()
