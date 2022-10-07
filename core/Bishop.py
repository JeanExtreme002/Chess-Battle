from Piece import Piece
from Color import Color


class Bishop(Piece):
    def __init__(self, color, x, y):
        super(Bishop, self).__init__(color, x, y)
    @property
    def movement(self):
        pass

    def legal_moves(self, situation: list[[]]):
        pass

    def move(self, target: list[int, int], situation: list[[]]):
        pass