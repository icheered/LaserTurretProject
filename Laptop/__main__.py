"""codeauthor:: Brand Hauser"""
import futures

from .targeting.targeter import Targeter
from .data.values import Status, Direction, SoundFX
import time
import concurrent.futures as cf
from multiprocessing import Queue
from .data.team_color import *
from .messaging.sound_effects import *
from .messaging.test_messenger import Messenger

status = Status.READY


def build_target_colors():
    """Build a list of color values for each team in the game.
    :returns: list of team_color objects"""
    colors_list = []
    return colors_list


def play_sound(sound):
    with cf.ThreadPoolExecutor(1) as executor:
        if sound == SoundFX.START:
            executor.submit(sound_player.play_start_sound())
        elif sound == SoundFX.HIT:
            executor.submit(sound_player.play_hit_sound())
        elif sound == SoundFX.FIRE:
            executor.submit(sound_player.play_laser_fire_sound())
        elif sound == SoundFX.TFOUND:
            executor.submit(sound_player.play_target_detected_sound())
        elif sound == SoundFX.TLOST:
            executor.submit(sound_player.play_target_lost_sound())


def run():
    """Runs the algorithm of the overall control.  Listens for messages from
    IR sensors as well as hits and responds accordingly."""
    pass


if __name__ == '__main__':
    command_queue = ()
    motion_queue = Queue(1)
    colors = build_target_colors()
    messenger = Messenger()
    sound_player = SoundPlayer()
    targeter = Targeter(command_queue, motion_queue, colors, messenger, sound_player)
    targeter.daemon = True
    targeter.start()
    play_sound(SoundFX.START)
    run()
