class Player:
    def __init__(self, color): #color = "black" ou color = "white"
        if not color in ("black", "white"):
            raise ValueError("\"color\" must be \"black\" or \"white\".")

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