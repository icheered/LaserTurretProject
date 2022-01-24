"""codeauthor:: Brand Hauser"""

from ..messaging.output_to_turret import OutputToTurret
from ..data.values import Status, Direction
from .tracker import *
import cv2
import multiprocessing
import time
from ..exceptions.InvalidDirectionException import InvalidDirectionException
from ..messaging.sound_effects import *

cascPath = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'haarcascade_frontalface.xml'))
faceCascade = cv2.CascadeClassifier(cascPath)


minimum_speed = 10


def calculate_x_error(x):
    """Calculate the pixel distance between the center of the frame and the x
    coordinate of the target.
    :param x: the x coordinate of the selected target
    :returns: pixel count difference. Negative error if target is left of center.
    Positive error if target is right of center."""
    error = x - 320
    return error


def get_x_speed(x_error):
    """Determine the appropriate speed for rotating the turret based on the error
    value along the horizontal plane.
    :param x_error: the number of pixels between the center of the frame and the
    target on the x plane
    :returns: the speed at which the turret should pan.  Negative speed turns left.
    Positive speed turns right."""
    speed_factor = round(100 / 320 * x_error)
    if minimum_speed > speed_factor > 0:
        speed_factor = minimum_speed
    elif 0 > speed_factor > -minimum_speed:
        speed_factor = -minimum_speed
    return speed_factor


def calculate_y_error(y):
    """Calculate the pixel distance between the center of the frame and the y
    coordinate of the target.
    :param y: the y coordinate of the selected target
    :returns: pixel count difference. Negative error if target is below center.
    Positive error if target is above center."""
    error = y - 240
    return error


def get_y_speed(y_error):
    """Determine the appropriate speed for rotating the turret based on the error
    value along the verticalal plane.
    :param y_error: the number of pixels between the center of the frame and the
    target on the y plane
    :returns: the speed at which the turret should tilt.  Negative speed tilts down.
    Positive speed tilts up."""
    speed_factor = round(100 / 240 * y_error)
    if minimum_speed > speed_factor > 0:
        speed_factor = minimum_speed
    elif 0 > speed_factor > -minimum_speed:
        speed_factor = -minimum_speed
    return speed_factor


class Targeter(multiprocessing.Process):

    def __init__(self, command_queue, motion_queue, colors, messenger):
        multiprocessing.Process.__init__(self)
        self.tracker = EuclideanDistTracker()
        self.messenger = messenger
        self.turret = OutputToTurret(self.messenger)
        self.cap = cv2.VideoCapture(0)
        self.command_queue = command_queue
        self.motion_queue = motion_queue
        self.colors = colors
        self.x_speed = 0  # tracks pan speed of last command sent to turret
        self.y_speed = 0  # tracks tilt speed of last command sent to turret
        self.last_target_time = None
        self.last_move_time = None
        self.last_sound_time = None
        self.status = Status.READY
        # Dict of target details.  Key = id#, value = tuple containing x and y
        # coordinates, width, height, area, and time first sighted
        self.targets = {}
        self.detections = []

    def run(self):
        """Begin object detection while loop.  Within loop, if targets are detected
        command the turret appropriately.  First check to see if turret is offline.
        If not offline look for RGB beacon for targeting. If beacon_found then fire
        at the beacon.  If no beacons within view look for human.  If human_found
        follow that human.  Choose the closest target."""
        while True:
            if self.status == Status.READY:
                fired = False
                frame = self.find_targets()
                if len(self.targets) > 0:
                    closest_target = self.determine_closest()
                    cv2.rectangle(frame, (closest_target[0], closest_target[1]),
                                  (closest_target[0] + closest_target[2], closest_target[1] + closest_target[3]),
                                  (0, 255, 0), 3)
                    cv2.imshow("frame", frame)
                    x_error = calculate_x_error(closest_target[0])
                    y_error = calculate_y_error(closest_target[1])
                    if abs(x_error) < 10 and abs(y_error) < 10:
                        self.fire()
                        fired = True
                    else:
                        self.move_turret(x_error, y_error)
                else:
                    if fired == True  or self.last_move_time is None or time.time() - self.last_move_time >= 2:
                        self.read_motion_queue()
                # TODO check commands and motion queue

    def fire(self):
        """Fire laser at target."""
        self.turret.fire()
        play_laser_fire_sound(self.last_sound_time)
        self.last_sound_time = time.time()

    def move_turret(self, x_error, y_error):
        """move the turret to the target.
        :param x_error: the difference between the target x coordinate and the center of the frame.
        :param y_error: the difference between the target y coordinate and the center of the frame."""
        pan_speed = get_x_speed(x_error)
        tilt_speed = get_y_speed(y_error)
        self.turret.pan_at_speed(pan_speed)
        self.turret.tilt_at_speed(tilt_speed)

    def determine_closest(self):
        """Determine which of the targets is closest based on their pixel area within
        the frame.
        :returns: the int id of the closest target"""
        largest_area = 0
        largest_id = None
        for key in self.targets:
            if self.targets[key][4] > largest_area:
                largest_area = self.targets[key][4]
                largest_id = key
        self.last_target_time = self.targets[largest_id][5]
        return self.targets[largest_id]

    def find_targets(self):
        """Detect targets within frame and collect/update target data."""
        _, frame = self.cap.read()
        self.find_beacon(frame)
        if len(self.detections) == 0:
            self.find_human(frame)
        if len(self.detections) == 0:
            return
        boxes_ids = self.tracker.update(self.detections)  # track recurring targets by id
        self.update_targets(boxes_ids)
        return frame

    def find_beacon(self, frame):
        """Detect RGB beacons in frame and collect target data."""
        for color in self.colors:
            lower_hsv, upper_hsv = color.get_hsv_window()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # window to show masking - black where colors outside bounds
            mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

            # window to show masking - blacks out all colors outside bounds
            result = cv2.bitwise_and(frame, frame, mask=mask)

            _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                # Calculate area and remove small elements
                area = cv2.contourArea(cnt)
                if area > 10:
                    # cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
                    x, y, w, h = cv2.boundingRect(cnt)
                    self.detections.append([x, y, w, h])

    def find_human(self, frame):
        """Detect human faces in frame and collect target data."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        for (x, y, w, h) in faces:
            self.detections.append([x, y, w, h])

    def update_targets(self, boxes_ids):
        """Update target saved data by target id."""
        boxes = {}
        for box_id in boxes_ids:
            x, y, w, h, object_id = box_id
            boxes[object_id] = x
            # change x and y from top left corner of box to center of target
            x = x + (w//2)
            y = y + (h//2)
            if self.targets[object_id] is None:
                self.targets[object_id] = [x, y, w, h, w * h, time.time()]
            else:
                time_stamp = self.targets[object_id][5]
                self.targets[object_id] = [x, y, w, h, w * h, time_stamp]

    def turn_to_new_target(self, direction):
        """Used to turn to an absolute angle based on IR sensor messaging if not currently
        tracking a target.
        :param direction: enum value from data.values.py - Direction"""
        self.last_move_time = time.time()
        self.turret.pan_absolute_angle(direction)

    def read_motion_queue(self):
        """Checks if there is a message from the IR sensors and then rotates to that direction"""
        if not self.motion_queue.empty():
            byte = self.motion_queue.get()
            direction = Direction(int.from_bytes(byte, 'big', signed=True))
            self.turn_to_new_target(direction)
        else:
            return

    def set_status(self, status):
        self.status = status
        self.turret.tilt_special(status)
        if status == Status.READY:
            play_start_sound(self.last_sound_time)
            self.last_sound_time = time.time()

    def get_last_sound_time(self):
        return self.last_sound_time
