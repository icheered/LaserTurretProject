"""codeauthor:: Brand Hauser"""

import numpy as np


class TeamColor:
    """Object to designate HSV windows for each team color in the game."""

    def __init__(self, color):
        """:param color: the name of the team color"""
        self.color = color
        self.l_s = 0
        self.l_h = 0
        self.l_v = 0
        self.u_h = 360
        self.u_s = 255
        self.u_v = 255

    def set_lower_hsv(self, hsv):
        """Set the lower hsv values of the window for targeting.
        :param hsv: list of the three values - Hue, Saturation, Value"""
        self.l_h = hsv[0]
        self.l_s = hsv[1]
        self.l_v = hsv[2]

    def set_upper_hsv(self, hsv):
        """Set the upper hsv values of the window for targeting.
        :param hsv: list of the three values - Hue, Saturation, Value"""
        self.u_h = hsv[0]
        self.u_s = hsv[1]
        self.u_v = hsv[2]

    def get_hsv_window(self):
        """Gets the hsv window values for the target.
        :returns: a list of the 6 values."""
        return np.array([self.l_h, self.l_s, self.l_v]), np.array([self.u_h, self.u_s, self.u_v])
