import unittest
from ..targeting.targeter import *


class TestTargeter(unittest.TestCase):
    def test_determine_closest(self):
        targets = {}
        determine_closest(targets)

    def test_calculate_x_error(self):
        x = 0
        calculate_x_error(x)

    def test_calculate_y_error(self):
        y = 0
        calculate_y_error(y)

    def test_get_x_speed(self):
        x_error = 0
        get_x_speed(x_error)

    def test_get_y_speed(self):
        y_error = 0
        get_y_speed(y_error)

    def test_turn_to_new_target(self):
        direction = Direction.NORTH
        turn_to_new_target(direction)
