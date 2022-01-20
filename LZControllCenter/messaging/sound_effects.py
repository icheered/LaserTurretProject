"""codeauthor:: Brand Hauser
Class for playing sound effects based on the current activity in the game."""

import random

from pydub import AudioSegment
from pydub.playback import play
import os


def play_hit_sound():
    """Randomly select and play a sound from the list generated for when the
    turret is shot by a player."""
    directory = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Sounds', 'free', 'hit'))
    sound_clip = AudioSegment.from_wav(directory + "/" + random.choice(os.listdir(directory)))
    play(sound_clip)


def play_start_sound():
    """Randomly select and play a sound from the list generated for when the
    turret starts."""
    directory = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Sounds', 'free', 'start'))
    sound_clip = AudioSegment.from_wav(directory + "/" + random.choice(os.listdir(directory)))
    play(sound_clip)


def play_target_detected_sound():
    """Randomly select and play a sound from the list generated for when
    a target is spotted."""
    directory = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Sounds', 'free', 'target found'))
    sound_clip = AudioSegment.from_wav(directory + "/" + random.choice(os.listdir(directory)))
    play(sound_clip)


def play_laser_fire_sound():
    """Randomly select and play a sound from the list generated for when the
    turret shoots at a player."""
    directory = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Sounds', 'free', 'fire'))
    sound_clip = AudioSegment.from_wav(directory + "/" + random.choice(os.listdir(directory)))
    play(sound_clip)


def play_target_lost_sound():
    """Randomly select and play a sound from the list generated for when the
    turret loses sight of the target."""
    directory = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Sounds', 'free', 'target lost'))
    sound_clip = AudioSegment.from_wav(directory + "/" + random.choice(os.listdir(directory)))
    play(sound_clip)


if __name__ == '__main__':
    play_hit_sound()
    play_start_sound()
    play_target_detected_sound()
    play_laser_fire_sound()
    play_target_lost_sound()
