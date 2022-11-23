from abc import ABC, abstractmethod
from .Color import Color
from .Pieces_type import Piece_type


class Piece(ABC):
    def __init__(self, color:Color, x:int, y:int):
        self._color = color
        self.x = x
        self.y = y
        self._list_moves:list[list[int, int]] = []
        self._has_moved = False
        piece = type(self).__name__.upper()
        self.name = piece.lower()
        self.__id = Piece_type[piece].value + color.value

    @property
    def r_id(self) -> int:
        return self.__id

    @property
    def in_row_boundary(self) -> bool:
        """Checks if the piece is on the top or bottom edge of the board"""
        if self.y == 7 or self.y == 0:
            return True
        return False

    @property
    def in_column_boundary(self) -> bool:
        """Checks if the piece is on the left or right edge of the board"""
        if self.x == 7 or self.x == 0:
            return True
        return False

    @property
    def color(self) -> Color:
        return self._color

    @property
    def has_moved(self) -> bool:
        return self._has_moved

    @property
    def coords(self) -> tuple:
        return self.x, self.y

    def _update_position(self, target: list[int, int]) -> None:
        """Moves a piece to a target"""
        self.x = target[1]
        self.y = target[0]

    def update_situation(self, target: list[int, int], situation: list[[]]) -> list[[]]:
        """Updates the board situation after a move"""
        situation[self.y][self.x] = None
        self._update_position(target)
        situation[self.y][self.x] = self
        return situation

    @staticmethod
    def is_defended(target:list[int, int], situation:list[[]]) -> bool:
        """Checks if the square is defended by a piece"""
        try:
            for row in range(8):
                for piece in situation[row]:
                    if piece is not None and\
                            target in piece.legal_moves(situation):
                        return True
            return False
        except IndexError as e:
            print("Ops!", e, "Occurred")

    @property
    @abstractmethod
    def movement(self):
        """Returns the lists of potential moves in any given position"""
        return

    @abstractmethod
    def legal_moves(self, situation: list[[]]):
        """Restricts the list of movements to only legal moves.
        Receives the situation of the board, a matrix with all the instances in the game right now.
        Returns the legal moves"""
        return

    @abstractmethod
    def move(self, target: list[int, int], situation: list[[]]):
        """Executes the move of the piece.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now.
        Returns the new updated situation if the move was possible"""
        return

