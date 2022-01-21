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
    SOUTHWEST = -75
    WEST = -50
    NORTHWEST = -25
