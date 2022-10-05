from Rook import *
from Color import *


class King(Piece):
    def __init__(self, color, x, y):
        super(King, self).__init__(color, x, y)
        self.piece = None

    @property
    def movement(self):
        """Returns the lists of potential moves in any given position"""
        self._list_moves.clear()
        for square in range(self.x - 1, self.x + 2):
            if 0 <= square < 7:
                self._list_moves.append([square, self.y + 1])
            if 0 < square <= 7:
                self._list_moves.append([square, self.y - 1])
            if square != self.x:
                self._list_moves.append([square, self.y])
        return self._list_moves.copy()

    def _free_spaces(self, situation, rook):
        free = 1
        if rook.x == 7:
            for square in range(self.x, rook.x):
                if situation[square][self.y] is not None:
                    free = 0
        else:
            for square in range(rook.x, self.x):
                if situation[square][self.y] is not None:
                    free = 0
        if free:
            return True
        return False

    def castle(self, situation, rook):
        if not self.has_moved and not rook.has_moved:
            return self._free_spaces(situation, rook)

    def is_defended(self, target, situation):
        """Checks if the square is defended by a piece"""
        for piece in situation:
            if piece is not None:
                if target in piece.legal_moves(target, situation):
                    return True
        return False

    def legal_moves(self, target, situation, rook=None):
        """Restricts the list of movements to only legal moves.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now."""
        if isinstance(rook, Rook):
            if self.castle(situation, rook):
                if rook.x == 7:
                    self._list_moves.append([self.x + 2, self.y])
                else:
                    self._list_moves.append([self.x - 2, self.y])
        for move in self.movement:
            if self.is_defended(move, situation):
                self._list_moves.remove(move)

    def move(self, target, situation, piece=None):
        """Executes the move of the piece.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now.
        Returns the new updated situation if the move was possible"""
        self.piece = piece
        self.legal_moves(target, situation)
        # checking if the move is possible
        if target not in self.movement:
            return situation
        self._situation = self._update_situation(target, situation)
        return self._situation.copy()
