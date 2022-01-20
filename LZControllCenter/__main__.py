from .targeting.targeter import Targeter
from .data.values import Status, Direction
import time
from multiprocessing import Queue
from .data.team_color import *
from .messaging.sound_effects import SoundEffects


status = Status.READY


def build_target_colors():
    """Build a list of color values for each team in the game.
    :returns: list of team_color objects"""
    colors_list = []
    return colors_list


def run():
    """Runs the algorithm of the overall control.  Listens for messages from
    IR sensors as well as hits and responds accordingly."""
    pass


if __name__ == '__main__':
    command_queue = Queue()
    motion_queue = Queue()
    colors = build_target_colors()
    sound_fx = SoundEffects()
    targeter = Targeter(command_queue, colors)
    targeter.daemon = True
    targeter.start()
    sound_fx.play_start_sound()
    run()

