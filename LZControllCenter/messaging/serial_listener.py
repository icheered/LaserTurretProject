"""codeauthor:: Brand Hauser"""

import serial


class Messenger:
    def __init__(self):
        self.port = None  # Find correct port on computer and enter name
        self.ser = serial.Serial()
        self.ser.port = self.port
        self.ser.baudrate = 19200

    def read(self):
        self.ser.open()
        self.ser.read()  # TODO decide length of message or change to readline and end message with \n
        self.ser.close()