"""codeauthor:: Brand Hauser
Class for playing sound effects based on the current activity in the game."""

import random

from play_sounds import play_file
import os
import time


def play_hit_sound(last_sound_time):
    """Randomly select and play a sound from the list generated for when the
    turret is shot by a player."""
    if last_sound_time is None or time.time() - last_sound_time > 5:
        directory = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Sounds', 'free', 'hit'))
        sound_clip = directory + "/" + random.choice(os.listdir(directory))
        play_file(sound_clip, block=False)


def play_start_sound(last_sound_time):
    """Randomly select and play a sound from the list generated for when the
    turret starts."""
    if last_sound_time is None or time.time() - last_sound_time > 5:
        directory = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Sounds', 'free', 'start'))
        sound_clip = directory + "/" + random.choice(os.listdir(directory))
        play_file(sound_clip, block=False)


def play_target_detected_sound(last_sound_time):
    """Randomly select and play a sound from the list generated for when
    a target is spotted."""
    if last_sound_time is None or time.time() - last_sound_time > 5:
        directory = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Sounds', 'free', 'target found'))
        sound_clip = directory + "/" + random.choice(os.listdir(directory))
        play_file(sound_clip, block=False)


def play_laser_fire_sound(last_sound_time):
    """Randomly select and play a sound from the list generated for when the
    turret shoots at a player."""
    if last_sound_time is None or time.time() - last_sound_time > 5:
        directory = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Sounds', 'free', 'fire'))
        sound_clip = directory + "/" + random.choice(os.listdir(directory))
        play_file(sound_clip, block=False)


def play_target_lost_sound(last_sound_time):
    """Randomly select and play a sound from the list generated for when the
    turret loses sight of the target."""
    if last_sound_time is None or time.time() - last_sound_time > 5:
        directory = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Sounds', 'free', 'target lost'))
        sound_clip = directory + "/" + random.choice(os.listdir(directory))
        play_file(sound_clip, block=False)
