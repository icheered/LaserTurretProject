import time
import unittest
from ..messaging.output_to_turret import OutputToTurret
from ..messaging.test_messenger import Messenger
from ..data.values import Direction, Status


class TestTargeter(unittest.TestCase):
    messenger = Messenger()
    output_msgr = OutputToTurret(messenger)

    def test_send(self):
        output = int.to_bytes(0, 1, 'big') + int.to_bytes(50, 2, 'big')
        self.output_msgr.send(output)
        msg = self.messenger.get_message()
        self.assertEqual(output, msg)

    def test_tilt_at_speed(self):
        speed = 50
        correct = int.to_bytes(0, 1, 'big') + int.to_bytes(50, 2, 'big')
        self.output_msgr.tilt_at_speed(speed)
        msg = self.messenger.get_message()
        self.assertEqual(msg, correct)
        speed = -20
        correct = int.to_bytes(0, 1, 'big') + speed.to_bytes(2, 'big', signed=True)
        self.output_msgr.tilt_at_speed(speed)
        msg = self.messenger.get_message()
        self.assertEqual(msg, correct)

    def test_tilt_special(self):
        command = Status.READY
        correct = int.to_bytes(1, 1, 'big') + int.to_bytes(1, 2, 'big')
        self.output_msgr.tilt_special(command)
        msg = self.messenger.get_message()
        self.assertEqual(msg, correct)
        command = Status.OFFLINE
        correct = int.to_bytes(1, 1, 'big') + int.to_bytes(0, 2, 'big')
        self.output_msgr.tilt_special(command)
        msg = self.messenger.get_message()
        self.assertEqual(msg, correct)

    def test_pan_at_speed(self):
        speed = 100
        correct = int.to_bytes(2, 1, 'big') + int.to_bytes(100, 2, 'big')
        self.output_msgr.pan_at_speed(speed)
        msg = self.messenger.get_message()
        self.assertEqual(msg, correct)
        speed = -60
        correct = int.to_bytes(2, 1, 'big') + speed.to_bytes(2, 'big', signed=True)
        self.output_msgr.pan_at_speed(speed)
        msg = self.messenger.get_message()
        self.assertEqual(msg, correct)

    def test_pan_relative_angle(self):
        angle = 45
        correct = int.to_bytes(3, 1, 'big') + int.to_bytes(25, 2, 'big')
        self.output_msgr.pan_relative_angle(angle)
        msg = self.messenger.get_message()
        self.assertEqual(msg, correct)
        angle = -90
        steps = -50
        correct = int.to_bytes(3, 1, 'big') + steps.to_bytes(2, 'big', signed=True)
        self.output_msgr.pan_relative_angle(angle)
        msg = self.messenger.get_message()
        self.assertEqual(msg, correct)

    def test_pan_absolute_angle(self):
        direction = Direction.NORTH
        correct = int.to_bytes(4, 1, 'big') + int.to_bytes(0, 2, 'big')
        self.output_msgr.pan_absolute_angle(direction)
        msg = self.messenger.get_message()
        self.assertEqual(msg, correct)
        direction = Direction.EAST
        correct = int.to_bytes(4, 1, 'big') + int.to_bytes(50, 2, 'big')
        self.output_msgr.pan_absolute_angle(direction)
        msg = self.messenger.get_message()
        self.assertEqual(msg, correct)
        direction = Direction.SOUTH
        correct = int.to_bytes(4, 1, 'big') + int.to_bytes(100, 2, 'big')
        self.output_msgr.pan_absolute_angle(direction)
        msg = self.messenger.get_message()
        self.assertEqual(msg, correct)
        direction = Direction.WEST
        angle = -50
        correct = int.to_bytes(4, 1, 'big') + angle.to_bytes(2, 'big', signed=True)
        self.output_msgr.pan_absolute_angle(direction)
        msg = self.messenger.get_message()
        self.assertEqual(msg, correct)

    def test_fire(self):
        self.output_msgr.fire()
        correct = int.to_bytes(5, 1, 'big') + int.to_bytes(0, 2, 'big')
        msg = self.messenger.get_message()
        self.assertEqual(msg, correct)
