from .Color import Color
from .King import King

class Player:
    def __init__(self, color):
        if not color in (Color.Black, Color.White):
            raise ValueError("O atributo \"color\" deve ser um objeto do tipo \"core.Color.Color\".")

        self.color = color
        self.__played = False
        self.__defense = [[False for _ in range(8)] for _ in range(8)]
        self.__king = None

    def __bool__(self):
        return self.__played
        
    @property
    def played(self):
        return self.__played

    @played.setter
    def played(self, value):
        if not isinstance(value, bool):
            raise ValueError("O atributo \"played\" deve ser um bool.")

        self.__played = value

    @property
    def defense(self):
        return self.__defense

    @defense.setter
    def defense(self, table):
        self.__defense = table

    @property
    def king(self) -> King:
        return self.__king
    
    @king.setter
    def king(self, k:King):
        if not isinstance(k, King):
            raise ValueError("O atributo \"king\" deve ser um objeto do tipo \"core.King.King\".")

        if k.color != self.color:
            raise AttributeError("A cor do rei deve ser a mesma do jogador!")

        self.__king = k

    def set_defended_pos(self, x:int, y:int):
        self.__defense[x][y] = True
