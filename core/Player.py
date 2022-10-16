from .Color import Color

class Player:
    def __init__(self, color):
        if not color in (Color.Black, Color.White):
            raise ValueError("\"color\" must be a core.Color.Color object.")

        self.color = color
        self.__played = False

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