import multiprocessing
from messaging.serial_listener import Messenger
import threading


class IRListener(threading.Thread):
    def __init__(self, motion_sensor):
        threading.Thread.__init__(self)
        self.listener = Messenger()
        self.motion_sensor = motion_sensor

    def run(self):
        while True:
            received_bytes = self.listener.read()
            if received_bytes[0] == 6:
                self.motion_sensor.set_detected(received_bytes)