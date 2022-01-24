import unittest
from ..targeting.targeter import *
from ..messaging.serial_messenger import Messenger
from ..data.values import Direction
from multiprocessing import Queue


class TestTurret(unittest.TestCase):
    messenger = Messenger()
    motion_queue = Queue()
    targeter = Targeter(None, motion_queue, None, messenger)

    def test_turret_rotate_from_motion(self):
        dirs = [Direction.NORTH, Direction.SOUTH, Direction.SOUTHEAST, Direction.EAST, Direction.NORTHEAST,
                Direction.NORTH, Direction.NORTHWEST, Direction.WEST, Direction.SOUTHWEST, Direction.SOUTH]
        for direction in dirs:
            byte = direction.value.to_bytes(1, 'big', signed=True)
            self.motion_queue.put(byte)
            time.sleep(2)
            print(direction)
            self.targeter.read_motion_queue()

    def test_turret_rotate_by_speed(self):
        x_error = -150
        y_error = 0
        self.targeter.move_turret(x_error, y_error)
        time.sleep(.5)
        x_error = -50
        self.targeter.move_turret(x_error, y_error)
        time.sleep(.5)
        x_error = 0
        self.targeter.move_turret(x_error, y_error)
        time.sleep(.5)
        x_error = 150
        y_error = 0
        self.targeter.move_turret(x_error, y_error)
        time.sleep(.5)
        x_error = 50
        self.targeter.move_turret(x_error, y_error)
        time.sleep(.5)
        x_error = 0
        self.targeter.move_turret(x_error, y_error)

