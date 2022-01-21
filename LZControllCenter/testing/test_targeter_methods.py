import unittest
from ..targeting.targeter import *
from ..messaging.test_messenger import Messenger
from ..data.values import Direction
from multiprocessing import Queue


class TestTargeter(unittest.TestCase):
    messenger = Messenger()
    motion_queue = Queue()
    targeter = Targeter(None, motion_queue, None, messenger)

    def test_determine_closest(self):
        targets = {1: (200, 150, 125, 290, 36250, time.time()), 2: (150, 304, 50, 200, 1000, time.time()),
                   3: (26, 146, 105, 146, 15330, time.time())}
        closest_id = determine_closest(targets)
        self.assertEqual(closest_id, 1)

    def test_calculate_x_error(self):
        x = 50
        error = calculate_x_error(x)
        self.assertEqual(error, -270)
        x = 457
        error = calculate_x_error(x)
        self.assertEqual(error, 137)

    def test_calculate_y_error(self):
        y = 45
        error = calculate_y_error(y)
        self.assertEqual(error, -195)

    def test_get_x_speed(self):
        x_error = -320
        speed = get_x_speed(x_error)
        self.assertEqual(-100, speed)

    def test_get_y_speed(self):
        y_error = 40
        speed = get_y_speed(y_error)
        self.assertEqual(20, speed)

    def test_turn_to_new_target(self):
        direction = Direction.NORTH
        self.targeter.turn_to_new_target(direction)
        msg = self.messenger.get_message()
        correct = int.to_bytes(4, 1, 'big') + direction.value.to_bytes(2, 'big', signed=True)
        self.assertEqual(msg, correct)

    def test_read_motion_queue(self):
        direction = 'S'
        byte = direction.encode('utf-8')
        self.motion_queue.put(byte)
        time.sleep(1)
        self.targeter.read_motion_queue()
        msg = self.messenger.get_message()
        correct = int.to_bytes(4, 1, 'big') + int.to_bytes(100, 2, 'big')
        self.assertEqual(correct, msg)
