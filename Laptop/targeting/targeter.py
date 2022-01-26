"""codeauthor:: Brand Hauser"""

from Laptop.messaging.output_to_turret import OutputToTurret
from Laptop.data.values import Status, Direction, PanningOscillation

from Laptop.messaging.sound_effects import *
from tracker import *
import cv2
import multiprocessing
import time
import math
from Laptop.exceptions.InvalidDirectionException import InvalidDirectionException

cascPath = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'haarcascade_frontalface.xml'))
faceCascade = cv2.CascadeClassifier(cascPath)

minimum_speed = 5


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
    speed_factor = 0.06
    speed = x_error * speed_factor
    '''max = 20
    negative = speed < 0
    if abs(speed) > max:
        speed = max
        if negative:
            speed = -speed'''
    return speed


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
    negative = y_error < 0
    y_error = abs(y_error)
    if y_error < 49:
        speed_factor = 0
    elif y_error < 85:
        speed_factor = 1
    elif y_error < 117:
        speed_factor = 2
    elif y_error < 152:
        speed_factor = 4
    else:
        speed_factor = 4
    if not negative:
        speed_factor = - speed_factor
    return speed_factor


class Targeter(multiprocessing.Process):

    def __init__(self, command_queue, motion_queue, colors, pan_messenger, tilt_messenger):
        multiprocessing.Process.__init__(self)
        self.tracker = EuclideanDistTracker()
        self.pan_messenger = pan_messenger
        self.tilt_messenger = tilt_messenger
        self.turret = OutputToTurret(self.pan_messenger, self.tilt_messenger)
        self.command_queue = command_queue
        self.motion_queue = motion_queue
        self.colors = colors
        self.x_speed = 0  # tracks pan speed of last command sent to turret
        self.y_speed = 0  # tracks tilt speed of last command sent to turret
        self.last_target_count = 0
        self.last_target_time = None
        self.last_move_time = None
        self.last_sound_time = None
        self.count_shot_since_motion_move = 0
        self.shot_all = False
        self.status = Status.READY
        # Dict of target details.  Key = id#, value = tuple containing x and y
        # coordinates, width, height, area, and time first sighted
        self.targets = {}
        self.detections = []
        self.pan_status = PanningOscillation.CENTER
        self.pan_time_stamp = time.time()
        self.px_to_degrees = 15.1

    def run(self):
        """Begin object detection while loop.  Within loop, if targets are detected
        command the turret appropriately.  First check to see if turret is offline.
        If not offline look for RGB beacon for targeting. If beacon_found then fire
        at the beacon.  If no beacons within view look for human.  If human_found
        follow that human.  Choose the closest target."""
        cap = cv2.VideoCapture(4)
        self.last_sound_time = time.time()
        self.pan_time_stamp = time.time()
        while True:
            #print("loop")
            #self.targets.clear()
            self.detections.clear()
            beacon_found = False
            if self.status == Status.READY:
                _, frame = cap.read()
                self.find_beacon(frame)
                if len(self.detections) == 0:
                    self.find_human(frame)
                else:
                    beacon_found = True
                if len(self.detections) > 0:
                    self.last_target_time = time.time()
                    """boxes_ids = self.tracker.update(self.detections)  # track recurring targets by id
                    self.update_targets(boxes_ids)
                    if len(self.targets) > 0:"""
                    if self.shot_all:
                        self.shot_all = False
                        if self.read_motion_queue():
                            continue
                    if self.last_target_count == 0 and not beacon_found:
                        self.last_sound_time = play_target_detected_sound(self.last_sound_time)
                    self.last_target_count = len(self.targets)
                    x, y, w, h, area = self.determine_closest()
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.circle(frame, (320, 240), 5, (0, 255, 0), -1)
                    center_x = x + w//2
                    center_y = y + h//2
                    cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
                    x_error = calculate_x_error(center_x)
                    y_error = calculate_y_error(center_y)
                    #print("x: %2d, y: %2d" % (center_x, center_y))
                    #print("x_error: %5.2f, y_error: %5.2f" %(x_error, y_error))
                    if abs(get_x_speed(x_error)) < 5 and abs(y_error) < 49 and beacon_found:
                        self.move_turret(0, 0)
                        self.fire()
                        print("fire")
                        self.count_shot_since_motion_move += 1
                        if self.count_shot_since_motion_move == len(self.targets):
                            self.shot_all = True
                    else:
                        self.move_turret(x_error, y_error)
                        pass
                    '''else:
                        if self.last_target_count > 0:
                            self.last_sound_time = play_target_lost_sound(self.last_sound_time)'''
                else:
                    #self.turret.tilt_at_speed(0)
                    #if self.last_target_time is not None and time.time() - self.last_target_time > 2:
                    self.move_turret(0, 0)
                    if self.last_move_time is None or time.time() - self.last_move_time >= 2:
                        if self.read_motion_queue():
                            continue
                    self.last_sound_time = play_target_lost_sound(self.last_sound_time)
                    self.last_target_count = 0
                    # self.oscillate()
                cv2.imshow("frame", frame)
                key = cv2.waitKey(1)
                if key == 27:
                    break

    def oscillate(self):
        if self.pan_status == PanningOscillation.CENTER and time.time() - self.pan_time_stamp > 1:
            self.turret.pan_relative_angle(10)
            self.pan_time_stamp = time.time()
            self.pan_status = PanningOscillation.RIGHT
        elif self.pan_status == PanningOscillation.RIGHT and time.time() - self.pan_time_stamp > 1:
            self.turret.pan_relative_angle(-20)
            self.pan_time_stamp = time.time()
            self.pan_status = PanningOscillation.LEFT
        elif self.pan_status == PanningOscillation.LEFT and time.time() - self.pan_time_stamp > 1:
            self.turret.pan_relative_angle(20)
            self.pan_time_stamp = time.time()
            self.pan_status = PanningOscillation.RIGHT

    def fire(self):
        """Fire laser at target."""
        self.turret.fire()
        self.last_sound_time = play_laser_fire_sound(self.last_sound_time)

    def move_turret(self, x_error, y_error):
        """move the turret to the target.
        :param x_error: the difference between the target x coordinate and the center of the frame.
        :param y_error: the difference between the target y coordinate and the center of the frame."""
        x_angle = math.floor(x_error / self.px_to_degrees)
        x_speed = int(get_x_speed(x_error))
        y_speed = get_y_speed(y_error)
        #print("x_angle: %2d, y_speed: %2d" % (x_angle, y_speed))
        #self.turret.pan_relative_angle(x_angle)
        #print("x_speed: %2d, y_speed: %2d" % (x_speed, y_speed))
        self.turret.pan_at_speed(x_speed)
        self.turret.tilt_at_speed(y_speed)

    def determine_closest(self):
        """Determine which of the targets is closest based on their pixel area within
        the frame.
        :returns: the int id of the closest target"""
        largest_area = 0
        largest_id = None
        for i in range(len(self.detections)):
            if self.detections[i][4] > largest_area:
                largest_area = self.detections[i][4]
                largest_id = i
        return self.detections[largest_id]

    def find_targets(self, cap):
        """Detect targets within frame and collect/update target data."""
        _, frame = cap.read()
        cv2.imshow("frame", frame)
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
                if area > 100:
                    # cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
                    x, y, w, h = cv2.boundingRect(cnt)
                    self.detections.append([x, y, w, h, w*h])

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
            self.detections.append([x, y, w, h, w*h])

    def update_targets(self, boxes_ids):
        """Update target saved data by target id."""
        boxes = {}
        for box_id in boxes_ids:
            x, y, w, h, object_id = box_id
            boxes[object_id] = x
            # change x and y from top left corner of box to center of target
            if object_id not in self.targets:
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
        self.pan_time_stamp = time.time()
        self.pan_status = PanningOscillation.CENTER

    def read_motion_queue(self):
        """Checks if there is a message from the IR sensors and then rotates to that direction"""
        if not self.motion_queue.empty():
            direction, timestamp = self.motion_queue.get()
            if time.time() - timestamp > 5:
                return False
            self.turn_to_new_target(direction)
            self.shot_all = False
            self.count_shot_since_motion_move = 0
            self.last_move_time = time.time()
            self.last_target_count = 0
            return True
        else:
            return False

    def set_status(self, status):
        self.status = status
        #self.turret.tilt_at_speed(status)
        if status == Status.READY:
            self.last_sound_time = play_start_sound(self.last_sound_time)
        elif status == Status.OFFLINE:
            self.move_turret(0,0)
            play_hit_sound(None)
            self.turret.tilt_at_speed(-1)
            time.sleep(1.6)
            self.turret.tilt_at_speed(0)
            time.sleep(5)
            self.turret.tilt_at_speed(4)
            self.last_sound_time = play_start_sound(self.last_sound_time)
            time.sleep(0.9)
            self.turret.tilt_at_speed(0)
            self.status = Status.READY

    def get_last_sound_time(self):
        return self.last_sound_time
