from .Color import Color

class Player:
    def __init__(self, color):
        if not color in (Color.Black, Color.White):
            raise ValueError("\"color\" must be a core.Color.Color object.")

        self.color = color
        self.__played = False
        self.__defense = [[False for _ in range(8)] for _ in range(8)]

    def __bool__(self):
        return self.__played
        
    @property
    def played(self):
        return self.__played

    @played.setter
    def played(self, value):
        if not isinstance(value, bool):
            raise ValueError("The \"played\" attribute must be a bool.")

        self.__played = value

    @property
    def defense(self):
        return self.__defense

    @defense.deleter
    def defense(self):
        self.__defense = [[False for _ in range(8)] for _ in range(8)]

    def set_defended_pos(self, x:int, y:int):
        self.__defense[x][y] = True
