import enum


class Status(enum.Enum):
    OFFLINE = 0
    READY = 1


class Direction(enum.Enum):
    NORTH = 0
    SOUTH = 100
    EAST = 50
    WEST = -50
