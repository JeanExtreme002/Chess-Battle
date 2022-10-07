from Piece import *


class Rook(Piece):
    def __init__(self, color, x, y):
        super(Rook, self).__init__(color, x, y)
        
    @property
    def movement(self):
        pass

    def legal_moves(self, situation):
        pass

    def move(self, target, situation):
        pass

    