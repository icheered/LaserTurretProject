"""codeauthor:: Brand Hauser"""

import serial


class Messenger:
    def __init__(self):
        self.port = '/dev/ttyACM0'  # Find correct port on computer and enter name
        self.ser = serial.Serial()
        self.ser.port = self.port
        self.ser.baudrate = 115200

    def send(self, msg):
        """Open serial port to send a message and then close it."""
        self.ser.open()
        self.ser.write(msg)
        self.ser.close()

    def get_message(self):
        """Open the serial port to read a message and then close the port.
        :returns: the message read from the serial port"""
        self.ser.open()
        msg = self.ser.read(1)
        self.ser.close()
        return msg
