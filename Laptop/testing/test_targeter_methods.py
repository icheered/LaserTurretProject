import unittest
from ..targeting.targeter import *
from ..messaging.test_messenger import Messenger
from ..data.values import Direction, Status
from multiprocessing import Queue


class TestTargeter(unittest.TestCase):
    messenger = Messenger()
    motion_queue = Queue()
    targeter = Targeter(None, motion_queue, None, messenger)

    def test_calculate_x_error(self):
        self.messenger.clear_queue()
        x = 50
        error = calculate_x_error(x)
        self.assertEqual(error, -270)
        x = 457
        error = calculate_x_error(x)
        self.assertEqual(error, 137)

    def test_calculate_y_error(self):
        self.messenger.clear_queue()
        y = 45
        error = calculate_y_error(y)
        self.assertEqual(error, -195)

    def test_get_x_speed(self):
        self.messenger.clear_queue()
        x_error = -320
        speed = get_x_speed(x_error)
        self.assertEqual(-100, speed)
        x_error = 0
        speed = get_x_speed(x_error)
        self.assertEqual(0, speed)

    def test_get_y_speed(self):
        self.messenger.clear_queue()
        y_error = 40
        speed = get_y_speed(y_error)
        self.assertEqual(17, speed)
        y_error = 0
        speed = get_y_speed(y_error)
        self.assertEqual(0, speed)

    def test_turn_to_new_target(self):
        self.messenger.clear_queue()
        direction = Direction.NORTH
        self.targeter.turn_to_new_target(direction)
        msg = self.messenger.get_message()
        correct = int.to_bytes(4, 1, 'big') + direction.value.to_bytes(2, 'big', signed=True)
        self.assertEqual(msg, correct)

    def test_read_motion_queue(self):
        self.messenger.clear_queue()
        direction = Direction.SOUTH
        byte = direction.value.to_bytes(1, 'big')
        self.motion_queue.put(byte)
        time.sleep(1)
        self.targeter.read_motion_queue()
        msg = self.messenger.get_message()
        correct = int.to_bytes(4, 1, 'big') + int.to_bytes(100, 2, 'big')
        self.assertEqual(correct, msg)
        direction = Direction.NORTHWEST
        byte = direction.value.to_bytes(1, 'big', signed=True)
        self.motion_queue.put(byte)
        time.sleep(1)
        self.targeter.read_motion_queue()
        msg = self.messenger.get_message()
        num = -25
        correct = int.to_bytes(4, 1, 'big') + num.to_bytes(2, 'big', signed=True)
        self.assertEqual(correct, msg)

    def test_fire(self):
        self.messenger.clear_queue()
        self.targeter.fire()
        msg = self.messenger.get_message()
        correct = int.to_bytes(5, 1, 'big') + int.to_bytes(0, 2, 'big')
        self.assertEqual(correct, msg)
        self.targeter.fire()
        time.sleep(5)
        self.targeter.fire()
        msg = self.messenger.get_message()
        correct = int.to_bytes(5, 1, 'big') + int.to_bytes(0, 2, 'big')
        self.assertEqual(correct, msg)

    def test_move_turret(self):
        self.messenger.clear_queue()
        x_error = -320
        y_error = 40
        self.targeter.move_turret(x_error, y_error)
        num = -100
        correct_x = int.to_bytes(2, 1, 'big') + num.to_bytes(2, 'big', signed=True)
        correct_y = int.to_bytes(0, 1, 'big') + int.to_bytes(17, 2, 'big')
        msg1 = self.messenger.get_message()
        msg2 = self.messenger.get_message()
        self.assertEqual(correct_x, msg1)
        self.assertEqual(correct_y, msg2)

    def test_determine_closest(self):
        self.messenger.clear_queue()
        t1 = (200, 150, 125, 290, 36250, time.time())
        t2 = (150, 304, 50, 200, 1000, time.time())
        t3 = (26, 146, 105, 146, 15330, time.time())
        self.targeter.targets = {1: t1, 2: t2, 3: t3}
        closest_id = self.targeter.determine_closest()
        self.assertEqual(closest_id, t1)

    def test_set_status(self):
        self.messenger.clear_queue()
        status = Status.OFFLINE
        self.targeter.set_status(status)
        correct = int.to_bytes(1, 1, 'big') + int.to_bytes(0, 2, 'big')
        msg = self.messenger.get_message()
        self.assertEqual(correct, msg)
        time.sleep(5)
        status = Status.READY
        self.targeter.set_status(status)
        correct = int.to_bytes(1, 1, 'big') + int.to_bytes(1, 2, 'big')
        msg = self.messenger.get_message()
        self.assertEqual(correct, msg)
        time.sleep(8)

