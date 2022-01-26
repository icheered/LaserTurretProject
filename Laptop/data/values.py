"""codeauthor:: Brand Hauser"""

import enum


class Status(enum.Enum):
    OFFLINE = 0
    READY = 1


class Direction(enum.Enum):
    NORTH = 0
    NORTHEAST = 25
    EAST = 50
    SOUTHEAST = 75
    SOUTH = 100
    SOUTHWEST = 125
    WEST = 150
    NORTHWEST = 175


class SoundFX(enum.Enum):
    START = 0
    HIT = 1
    FIRE = 2
    TFOUND = 3
    TLOST = 4


class PanningOscillation(enum.Enum):
    CENTER = 0
    RIGHT = 1
    LEFT = 2
