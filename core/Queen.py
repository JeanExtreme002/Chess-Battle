from .Piece import Piece
from .Color import Color
from .Pieces_type import Piece_type


class Queen(Piece):
    def __init__(self, color: Color, x: int, y: int):
        super(Queen, self).__init__(color, x, y)
        self.__id = Piece_type.QUEEN.value + color.value

    @property
    def movement(self) -> list:
        """Returns the lists of potential moves in any given position"""
        self._list_moves.clear()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        # checking left-right, up-down and semi-diagonals
        for side in directions:
            x, y = self.x, self.y
            while True:
                x += side[0]
                y += side[1]
                in_board_boundary = 0 <= x < 8 and 0 <= y < 8
                if not in_board_boundary:
                    break
                else:
                    self._list_moves.append([x, y])
        return self._list_moves.copy()

    def legal_moves(self, situation: list[[]]) -> list:
        """Restricts the list of movements to only legal moves.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now.
        Returns the legal moves"""
        psb_moves = self.movement
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        try:
            # checking left-right, up-down and semi-diagonals
            for side in directions:
                x, y = self.x, self.y
                blocked = False
                while True:
                    x += side[0]
                    y += side[1]
                    in_board_boundary = 0 <= x < 8 and 0 <= y < 8
                    if not in_board_boundary:
                        break
                    if not blocked and situation[x][y] is not None:
                        blocked = True
                        if situation[x][y].color == self.color:
                            psb_moves.remove([x, y])
                    elif blocked:
                        psb_moves.remove([x, y])
        except IndexError as e:
            print("Ops!", e, "Occurred")
        finally:
            return psb_moves

    def move(self, target: list[int, int], situation: list[[]]) -> list[[]]:
        """Executes the move of the piece.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now.
        Returns the new updated situation if the move was possible"""
        psb_moves = self.legal_moves(situation)
        # checking if the move is possible
        if target not in psb_moves:
            return situation
        new_situation = self.update_situation(target, situation)
        return new_situation
