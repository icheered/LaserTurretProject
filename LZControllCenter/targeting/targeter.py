"""codeauthor:: Brand Hauser"""

from ..messaging.output_to_turret import *
from ..data.values import Status, Direction
from .tracker import *
import cv2
import multiprocessing
import time


class Targeter(multiprocessing.Process):

    def __init__(self, command_queue, colors):
        multiprocessing.Process.__init__(self)
        self.tracker = EuclideanDistTracker()
        self.cap = cv2.VideoCapture(0)
        self.command_queue = command_queue
        self.colors = colors
        self.x_speed = 0  # tracks pan speed of last command sent to turret
        self.y_speed = 0  # tracks tilt speed of last command sent to turret
        self.closest_target = -1

    def run(self):
        """Begin object detection while loop.  Within loop, if targets are detected
        command the turret appropriately.  First check to see if turret is offline.
        If not offline look for RGB beacon for targeting. If beacon_found then fire
        at the beacon.  If no beacons within view look for human.  If human_found
        follow that human.  Choose the closest target."""
        # Dict of target details.  Key = id#, value = tuple containing x and y
        # coordinates, width, height, area, and time first sighted
        targets = {}
        target_locked = False
        beacon_detected = False
        human_detected = False
        while True:
            pass


def determine_closest(targets):
    """Determine which of the targets is closest based on their pixel area within
    the frame.
    :param targets: dictionary of target values
    :returns: the int id of the closest target"""
    pass


def calculate_x_error(x):
    """Calculate the pixel distance between the center of the frame and the x
    coordinate of the target.
    :param x: the x coordinate of the selected target
    :returns: pixel count difference. Negative error if target is left of center.
    Positive error if target is right of center."""
    pass


def get_x_speed(x_error):
    """Determine the appropriate speed for rotating the turret based on the error
    value along the horizontal plane.
    :param x_error: the number of pixels between the center of the frame and the
    target on the x plane
    :returns: the speed at which the turret should pan.  Negative speed turns left.
    Positive speed turns right."""
    pass


def calculate_y_error(y):
    """Calculate the pixel distance between the center of the frame and the y
    coordinate of the target.
    :param y: the y coordinate of the selected target
    :returns: pixel count difference. Negative error if target is below center.
    Positive error if target is above center."""
    pass


def get_y_speed(y_error):
    """Determine the appropriate speed for rotating the turret based on the error
    value along the verticalal plane.
    :param y_error: the number of pixels between the center of the frame and the
    target on the y plane
    :returns: the speed at which the turret should tilt.  Negative speed tilts down.
    Positive speed tilts up."""
    pass


def turn_to_new_target(direction):
    """Used to turn to an absolute angle based on IR sensor messaging if not currently
    tracking a target.
    :param direction: enum value from data.values.py - Direction"""
    pass
