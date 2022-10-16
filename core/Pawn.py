from .Piece import Piece
from .PromotionRoles import PromotionRoles
from .Color import Color
from typing import Optional


class Pawn(Piece):
    def __init__(self, color: Color, x: int, y: int):
        super(Pawn, self).__init__(color, x, y)
        self._has_moved2 = False
        self._en_passant_enable = False
        self._captures = []

    @property
    def has_moved2(self) -> bool:
        return self._has_moved2

    @property
    def movement(self) -> list:
        """Returns the lists of potential moves in any given position"""
        self._list_moves.clear()
        if self.in_row_boundary:
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
    def captures(self) -> list:
        """Returns the lists of potential captures in any given position"""
        self._captures.clear()
        if self.in_row_boundary:
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

    def legal_moves(self, situation: list[[]]) -> list:
        """Restricts the list of movements to only legal moves.
        Receives the situation of the board, a matrix with all the instances in the game right now.
        Returns the legal moves"""
        psb_moves = self.movement
        psb_captures = self.captures
        try:
            # checking if there is something in front of the pawn
            for move in psb_moves:
                if situation[move[0]][move[1]] is not None:
                    psb_moves.remove(move)
            # checking if there is something to be capture
            for move in psb_captures:
                if (situation[move[0]][move[1]] is None and not self.en_passant) or \
                        (situation[move[0]][move[1]].color == self.color):
                    psb_captures.remove(move)
        except IndexError as e:
            print("Ops!", e, "Occurred")
        finally:
            return psb_moves + psb_captures

    @property
    def en_passant(self) -> bool:
        """Checks if the pawn is capable of performing en passant"""
        if (self.color == Color.White and self.y == 4) or \
                (self.color == Color.Black and self.y == 3):
            self._en_passant_enable = True
        else:
            self._en_passant_enable = False
        return self._en_passant_enable

    def promotion(self, piece) -> bool:
        """Checks if it is a case for promotion"""
        if self.y == 7 or self.y == 0:
            if isinstance(piece, PromotionRoles):
                return True
        return False

    def move(self, target: list[int, int], situation: list[[]], piece: Optional[PromotionRoles] = None) -> list[[]]:
        """Executes the move of the piece.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now.
        Returns the new updated situation if the move was possible"""
        psb_moves = self.legal_moves(situation)
        # checking if the move is possible
        #if target not in psb_moves:
        #    return situation
        # updating attributes
        
        self._has_moved2 = True if target[1] == self.y + 2 or target[1] == self.y - 2 else False
        #self._has_moved2 = True
        self._has_moved = True

        new_situation = self.update_situation(target, situation)
        # checking promotion
        #if self.promotion:
        #    role = globals()[piece.name]
        #    new_role = role(self.color, self.x, self.y)
        #    new_situation[self.x][self.y] = new_role
        return new_situation
