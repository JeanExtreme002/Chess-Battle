from Piece import *
from Pieces_type import Piece_type


class Rook(Piece):
    
    def __init__(self, color, x, y,r_id):
        super(Rook, self).__init__(color, x, y,r_id)
        self.__id =int(Piece_type.ROOK)+color
    @property
    def movement(self):
        pass

    def legal_moves(self, situation):
        pass

    def move(self, target, situation):
        pass

    