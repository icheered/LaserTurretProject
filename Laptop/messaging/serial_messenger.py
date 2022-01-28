"""codeauthor:: Brand Hauser"""

import serial
from serial import SerialException


class Messenger:
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(self.port, 115200)

    def send(self, msg):
        """Open serial port to send a message and then close it."""
        #print(msg)
        self.ser.write(msg)

    def get_message(self):
        """Open the serial port to read a message and then close the port.
        :returns: the message read from the serial port"""
        #try:
        msg = self.ser.read(1)
        """except SerialException:

            print("Serial exception")
            print(self.port)
            self.ser = serial.Serial(self.port, 115200)
            msg = "0"
            """
        
        return msg
