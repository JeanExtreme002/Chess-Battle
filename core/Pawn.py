from Piece import *
from PromotionRoles import *
from Color import *


class Pawn(Piece):
    def __init__(self, color, x, y):
        super(Pawn, self).__init__(color, x, y)
        self.piece = None
        self.has_moved2 = 0
        self.en_passant_enable = 0
        self._captures = []

    @property
    def movement(self):
        """Returns the lists of potential moves in any given position"""
        self._list_moves.clear()
        if self.row_boundary:
            return self._list_moves.copy()
        if self.color == Color.White:
            self._list_moves.append([self.x, self.y + 1])
            if not self.has_moved:
                self._list_moves.append([self.x, self.y + 2])
        else:
            self._list_moves.append([self.x, self.y - 1])
            if not self.has_moved:
                self._list_moves.append([self.x, self.y - 2])
        return self._list_moves.copy()

    @property
    def captures(self):
        """Returns the lists of potential captures in any given position"""
        self._captures.clear()
        if self.row_boundary:
            return self._captures.copy()
        if self.color == Color.White:
            for square in range(self.x - 1, self.x + 2, 2):
                if 0 <= square < 7:
                    self._captures.append([square, self.y + 1])
        else:
            for square in range(self.x - 1, self.x + 2, 2):
                if 0 <= square <= 7:
                    self._captures.append([square, self.y - 1])
        return self._captures.copy()

    def legal_moves(self, target, situation):
        """Restricts the list of movements to only legal moves.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now."""
        psb_moves = self.movement
        psb_captures = self.captures
        for move in psb_moves:
            if situation[move[0]][move[1]] is not None:
                psb_moves.remove(move)
        for move in psb_captures:
            if situation[move[0]][move[1]] is None and not self.en_passant:
                psb_captures.remove(move)

    @property
    def en_passant(self):
        # checking if the target is right next the piece
        row = self.piece.x == self.x - 1 or self.piece.x == self.x + 1
        column = self.piece.y == self.y
        target = row and column
        # checking if the target is a pawn
        target_class = isinstance(self.piece, Pawn)
        allowed = target and target_class
        if self.color == Color.White:
            if self.y == 4 and allowed:
                return True
        else:
            if self.y == 3 and allowed:
                return True
        return False

    @property
    def promotion(self):
        """Checks if it is a case for promotion"""
        if self.y == 7 or self.y == 0:
            if isinstance(self.piece, PromotionRoles):
                return True
        return False

    def move(self, target, situation, piece=None):
        """Executes the move of the piece.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now.
        Returns the new updated situation if the move was possible"""
        self.piece = piece
        self.legal_moves(target, situation)
        # checking if the move is possible
        if target not in self.movement + self.captures:
            return situation
        self._situation = self._update_situation(target, situation)
        # checking promotion
        if self.promotion:
            role = globals()[self.piece.name]
            new_role = role(self.color, self.x, self.y)
            self._situation[self.x][self.y] = new_role
        return self._situation.copy()
