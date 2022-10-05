from abc import ABC, abstractmethod
from Color import *


class Piece(ABC):
    def __init__(self, color, x, y):
        self._color = color
        self._color_complex = None
        self.x = x
        self.y = y
        self._list_moves = []
        self._situation = [[]]
        self.has_moved = 0

    @property
    def row_boundary(self):
        # checks if the piece is on the border of the board
        if self.y == 7 or self.y == 0:
            return True
        return False

    @property
    def column_boundary(self):
        # checks if the piece is on the border of the board
        if self.x == 7 or self.x == 0:
            return True
        return False

    @property
    def situation(self):
        return self._situation

    @property
    def color(self):
        return self._color

    @property
    def color_complex(self):
        """Returns the color of the square"""
        if self.x + self.y in Color.Dark.value:
            self._color_complex = Color.Dark
        else:
            self._color_complex = Color.Light
        return self.color_complex

    def _update_position(self, target):
        self.x = target[0]
        self.y = target[1]

    def _update_situation(self, target, situation):
        situation[self.x][self.y] = 0
        self._update_position(target)
        situation[self.x][self.y] = self
        return situation

    @abstractmethod
    @property
    def movement(self):
        """Returns the lists of potential moves in any given position"""
        return

    @abstractmethod
    def legal_moves(self, target, situation):
        """Restricts the list of movements to only legal moves.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now."""
        pass

    @abstractmethod
    def move(self, target, situation):
        """Executes the move of the piece.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now.
        Returns the new updated situation if the move was possible"""
        pass
