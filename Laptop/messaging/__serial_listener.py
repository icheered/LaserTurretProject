"""codeauthor:: Brand Hauser
Class for receiving messages from a microcontroller over serial port."""

import serial


class Messenger:
    def __init__(self):
        self.port = "COM9"  # Find correct port on computer and enter name
        self.ser = serial.Serial()
        self.ser.port = self.port
        self.ser.baudrate = 115200

    def read(self):
        """Open the serial port to read a message and then close the port.
        :returns: the message read from the serial port"""
        self.ser.open()
        msg = self.ser.read(2)
        self.ser.close()
        return msg
