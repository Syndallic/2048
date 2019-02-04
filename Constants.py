from enum import Enum, auto

GRID_WIDTH = 4
GRID_HEIGHT = 4


class Direction(Enum):
    DOWN = auto()
    UP = auto()
    LEFT = auto()
    RIGHT = auto()