import multiprocessing

from data.values import Status
from messaging.serial_messenger import Messenger
import threading


class InputListener(threading.Thread):
    def __init__(self, motion_sensor, targeter, messenger, hit_queue):
        threading.Thread.__init__(self)
        self.listener = messenger
        self.motion_sensor = motion_sensor
        self.targeter = targeter
        self.hit_queue = hit_queue

    def run(self):
        buffer = []
        readingMessage = False
        while True:
            received_bytes = self.listener.get_message()
            print(f"received: {received_bytes}")
            if received_bytes[0] == 21:
                print("Stopping to read message")
                readingMessage = False
                print(buffer)

                if int.from_bytes(buffer[0], 'big') == 6:
                    print("Motion detected")
                    self.motion_sensor.set_detected(buffer)
                elif int.from_bytes(buffer[0], 'big') == 7:
                    print("getHit dtected")
                    if self.hit_queue.empty():
                        self.hit_queue.put(1)
                else:
                    print(f"Uknown opcode: {buffer[0]}, type: {type(buffer[0])}")


                
                buffer = []

            if readingMessage:
                buffer.append(received_bytes)

            if received_bytes[0] == 20:
                print("Starting to read message")
                readingMessage = True
            
            

            
