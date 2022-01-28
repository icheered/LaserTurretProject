import unittest
from ..targeting.targeter import *
from ..messaging.serial_messenger import Messenger
from ..data.values import Direction
from multiprocessing import Queue


class TestTurret(unittest.TestCase):
    pan_messenger = Messenger("/dev/ttyACM0")
    motion_queue = Queue()
    targeter = Targeter(None, motion_queue, None, None, pan_messenger, None)
    turret = OutputToTurret(pan_messenger, None)

    def test_turret_rotate_from_motion(self):
        dirs = [Direction.NORTH, Direction.SOUTH, Direction.SOUTHEAST, Direction.EAST, Direction.NORTHEAST,
                Direction.NORTH, Direction.NORTHWEST, Direction.WEST, Direction.SOUTHWEST, Direction.SOUTH]
        for i in range(4):
            for direction in dirs:
                tuple = (direction, time.time())
                self.motion_queue.put(tuple)
                time.sleep(2)
                print(direction)
                self.targeter.read_motion_queue()
            i += 1

    def test_turret_rotate_by_relative_angle(self):
        time.sleep(1)
        for i in range(10):
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(45)
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(45)
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(45)
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(45)
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(-45)
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(-45)
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(-45)
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(-45)
            # time.sleep(1)
            """self.targeter.turret.pan_relative_angle(22)
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(22)
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(22)
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(22)
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(-22)
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(-22)
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(-22)
            time.sleep(1)
            self.targeter.turret.pan_relative_angle(-22)
            time.sleep(1)"""
            i += 1
        """
        """

    def test_tilt(self):
        y_error = 5
        for i in range(5):
            y_speed = get_y_speed(y_error)
            self.turret.tilt_at_speed(y_speed)
            print("y_error: %5.2f, y_speed: %5.2f" % (y_error, y_speed))
            time.sleep(.5)
            y_error = -y_error
            y_speed = get_y_speed(y_error)
            self.turret.tilt_at_speed(y_speed)
            print("y_error: %5.2f, y_speed: %5.2f" % (y_error, y_speed))
            time.sleep(.5)
            y_error = y_error + 10
