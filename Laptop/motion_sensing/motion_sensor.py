from messaging.serial_listener import Messenger
from data.values import Direction
import datetime

class MotionSensor:
    def __init__(self):
        self.listener = Messenger()
        self.lastMessageTuple = ()
        self.directions = [0,1,2,3]
        self.latestDirection = None

    def detector(self):
        received_bytes = self.listener.read()
        print(received_bytes)
        detected = int.from_bytes(received_bytes[0], "big") == 6
        updated_direction = None
        if detected:
            direction = int.from_bytes(received_bytes[1], "big")
            if len(self.lastMessageTuple) != 0:
                cur_time = datetime.datetime.now()
                if (cur_time - self.lastMessageTuple[1]).total_seconds() * 1000 <= 1500:
                    last_direction = self.lastMessageTuple[0]
                    # Check if adjacent
                    if abs(direction - last_direction) % 3 == 1:
                        direction_val = direction**2 + last_direction**2
                        if direction_val == 1:
                            updated_direction = Direction.NORTHEAST
                        elif direction_val == 5:
                            updated_direction = Direction.SOUTHEAST
                        elif direction_val == 13:
                            updated_direction = Direction.SOUTHWEST
                        elif direction_val == 9:
                            updated_direction = Direction.NORTHWEST

            if updated_direction is None:
                if direction == 0:
                    updated_direction = Direction.NORTH
                elif direction == 1:
                    updated_direction = Direction.EAST
                elif direction == 2:
                    updated_direction = Direction.SOUTH
                else:
                    updated_direction = Direction.WEST

            self.latestDirection = updated_direction
            self.lastMessageTuple = (direction, datetime.datetime.now())






