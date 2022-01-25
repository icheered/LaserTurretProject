"""codeauthor:: Brand Hauser"""
from motion_sensing.ir_listener import IRListener
from targeting.targeter import Targeter
from data.values import Status, Direction
import time
from multiprocessing import Queue
from data.team_color import *
from messaging.sound_effects import *
from messaging.test_messenger import Messenger
from motion_sensing.motion_sensor import MotionSensor
import _thread

status = Status.READY


def build_target_colors():
    """Build a list of color values for each team in the game.
    :returns: list of team_color objects"""
    colors_list = []
    return colors_list


def run():
    """Runs the algorithm of the overall control.  Listens for messages from
    IR sensors as well as hits and responds accordingly."""
    while True:
        pass


if __name__ == '__main__':
    # command_queue = ()
    # motion_queue = Queue(1)
    # colors = build_target_colors()
    # messenger = Messenger()
    # targeter = Targeter(command_queue, motion_queue, colors, messenger)
    # targeter.daemon = True
    # targeter.start()
    # play_start_sound()

    # Create motion detector object
    motion_detector = MotionSensor()

    # Start listener
    motionListener = IRListener(motion_detector)

    motionListener.start()
    motion_detector.start()
    run()
