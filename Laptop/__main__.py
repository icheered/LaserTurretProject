"""codeauthor:: Brand Hauser"""

from data.values import Status
import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from communication.input_listener import InputListener
from targeting.targeter import Targeter
from data.values import Status, Direction
import time
from multiprocessing import Queue
from motion_sensing.motion_sensor import MotionSensor
from data.team_color import *
from messaging.sound_effects import *
from messaging.serial_messenger import Messenger

status = Status.READY


def build_target_colors():
    """Build a list of color values for each team in the game.
    :returns: list of team_color objects"""
    colors_list = []
    green = TeamColor("green")
    green.set_lower_hsv([44,88,128])
    green.set_upper_hsv([71, 201, 255])
    colors_list.append(green)
    green_gun = TeamColor("ggreen")
    green_gun.set_lower_hsv([44,35,190])
    green_gun.set_lower_hsv([69,255,255])
    #colors_list.append(green_gun)
    yellow = TeamColor("yellow")
    yellow.set_lower_hsv([8, 107, 106])
    yellow.set_upper_hsv([311, 230, 255])
    #colors_list.append(yellow)
    return colors_list


def run():
    """Runs the algorithm of the overall control.  Listens for messages from
    IR sensors as well as hits and responds accordingly."""
    targeter.join()
    print("joined")
    return


if __name__ == '__main__':
    command_queue = ()
    motion_queue = Queue(1)
    hit_queue = Queue()
    colors = build_target_colors()
    pan_messenger = Messenger("/dev/ttyACM0")
    tilt_messenger = Messenger("/dev/ttyUSB0")
    input_messenger = Messenger("/dev/ttyUSB1")
    targeter = Targeter(command_queue, motion_queue, hit_queue, colors, pan_messenger, tilt_messenger)
    targeter.daemon = True
    targeter.start()
    play_start_sound(None)

    # Create motion detector object
    motion_detector = MotionSensor(motion_queue)

    # Create IR listener
    motionListener = InputListener(motion_detector, targeter, input_messenger, hit_queue)
    motion_detector.setDaemon(True)
    motionListener.setDaemon(True)
    # Start required threads
    motionListener.start()
    motion_detector.start()
    run()

