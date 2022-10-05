from enum import Enum


class Color(Enum):
    Black = 1
    White = 0
    Dark = [i for i in range(0, 64, 2)]
    Light = [i for i in range(1, 64, 2)]
