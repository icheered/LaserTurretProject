"""codeauthor:: Brand Hauser
Class for receiving messages from a microcontroller over serial port."""

import serial


class Messenger:
    def __init__(self):
        self.port = None  # Find correct port on computer and enter name
        self.ser = serial.Serial()
        self.ser.port = self.port
        self.ser.baudrate = 19200

    def read(self):
        """Open the serial port to read a message and then close the port.
        :returns: the message read from the serial port"""
        self.ser.open()
        msg = self.ser.read()  # TODO decide length of message or change to readline and end message with \n
        self.ser.close()
        return msg
