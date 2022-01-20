import random

from pydub import AudioSegment
from pydub.playback import play
import os


class SoundEffects:

    def __init__(self):
        self.hit_sounds = build_hit_sound_list()
        self.start_sounds = build_start_sound_list()

    def play_hit_sound(self):
        sound_clip = random.choice(self.hit_sounds)
        play(sound_clip)

    def play_start_sound(self):
        sound_clip = random.choice(self.start_sounds)
        play(sound_clip)


def build_hit_sound_list():
    hit_list = []
    no_no_aaaa = AudioSegment.from_wav(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Sounds', 'no,no,aaaa.wav')))
    hit_list.append(no_no_aaaa)
    return hit_list


def build_start_sound_list():
    do_ya_punk = AudioSegment.from_wav(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Sounds', 'do-you-punk.wav')))
    say_hello = AudioSegment.from_wav(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'Sounds', 'Little Friend.wav')))
    start_list = [do_ya_punk, say_hello]
    return start_list








if __name__ == '__main__':
    play_hit_sound()
