"""codeauthor:: Brand Hauser"""
import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from targeting.targeter import Targeter
from data.values import Status, Direction
import time
from multiprocessing import Queue
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
    #colors_list.append(green)
    yellow = TeamColor("yellow")
    yellow.set_lower_hsv([8, 107, 106])
    yellow.set_upper_hsv([311, 230, 255])
    colors_list.append(yellow)
    return colors_list


def run():
    """Runs the algorithm of the overall control.  Listens for messages from
    IR sensors as well as hits and responds accordingly."""
    lives = 5
    start_time = time.time()
    while True:
        if lives == 0 or time.time() - start_time >= 300:
            break


if __name__ == '__main__':
    command_queue = ()
    motion_queue = Queue(1)
    colors = build_target_colors()
    pan_messenger = Messenger("/dev/ttyACM0")
    tilt_messenger = Messenger("/dev/ttyUSB0")
    targeter = Targeter(command_queue, motion_queue, colors, pan_messenger, tilt_messenger)
    targeter.daemon = True
    targeter.start()
    play_start_sound(None)
    run()
