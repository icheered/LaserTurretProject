import multiprocessing

from data.values import Status
from messaging.serial_listener import Messenger
import threading


class InputListener(threading.Thread):
    def __init__(self, motion_sensor, targeter):
        threading.Thread.__init__(self)
        self.listener = Messenger()
        self.motion_sensor = motion_sensor
        self.targeter = targeter

    def run(self):
        buffer = []
        readingMessage = False
        while True:
            received_bytes = self.listener.read()

            if readingMessage:
                buffer.append(received_bytes)
            
            if received_bytes[0] == 20:
                readingMessage = True
            
            if received_bytes[0] == 21:
                readingMessage == False

                if buffer[0] == 6:
                    self.motion_sensor.set_detected(buffer)
                elif buffer[0] == 7:
                    self.targeter.set_status(Status.OFFLINE)
                
                buffer = []
            
            

            
