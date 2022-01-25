from data.values import Direction
import threading
import time

TIME_FINE_GRAINED_DIR = 0.2


class MotionSensor(threading.Thread):
    def __init__(self, motion_queue):
        threading.Thread.__init__(self)
        self.directions = [0, 1, 2, 3]
        self.latestDirection = None
        self.motion_queue = motion_queue

        self.received_bytes = None
        self.last_received_dir = None

    def set_detected(self, set_bytes):
        self.received_bytes = set_bytes

    def run(self) -> None:
        while True:
            if self.received_bytes is not None:
                direction = self.received_bytes[1]
            else:
                direction = None
            if direction is not None and (direction != self.last_received_dir
                                          or self.last_received_dir is None):

                if direction == 0:
                    updated_direction = Direction.NORTH
                elif direction == 1:
                    updated_direction = Direction.EAST
                elif direction == 2:
                    updated_direction = Direction.SOUTH
                else:
                    updated_direction = Direction.WEST

                time.sleep(0.3)
                last_direction = direction
                direction = self.received_bytes[1]
                if direction != last_direction:
                    # Check if adjacent
                    if abs(direction - last_direction) % 3 == 1:
                        direction_val = direction ** 2 + last_direction ** 2
                        if direction_val == 1:
                            updated_direction = Direction.NORTHEAST
                        elif direction_val == 5:
                            updated_direction = Direction.SOUTHEAST
                        elif direction_val == 13:
                            updated_direction = Direction.SOUTHWEST
                        else:
                            updated_direction = Direction.NORTHWEST

                self.latestDirection = updated_direction
                self.received_bytes = None
                print(self.latestDirection)

                # Append to queue (possibly do nowait for faster performance)
                if not self.motion_queue.empty():
                    self.motion_queue.get()
                self.motion_queue.put((self.latestDirection, time.time()))
