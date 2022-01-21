"""codeauthor:: Brand Hauser"""

import enum


class Status(enum.Enum):
    OFFLINE = 0
    READY = 1


class Direction(enum.Enum):
    NORTH = 0
    SOUTH = 100
    EAST = 50
    WEST = -50


class MotionDirection(enum.Enum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7
