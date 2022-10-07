from Piece import Piece
from Rook import Rook
from Color import Color


class King(Piece):
    def __init__(self, color: Color, x: int, y: int):
        super(King, self).__init__(color, x, y)
        self.is_checked = False
        self.is_mated = False

    @property
    def movement(self) -> list:
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

    def _free_spaces(self, situation: list[[]], rook: Rook) -> bool:
        """Private auxiliary function to check if the squares between the king and rook are free"""
        free = True
        if rook.x == 7:
            for square in range(self.x + 1, rook.x):
                if situation[square][self.y] is not None:
                    free = False
        elif rook.x == 0:
            for square in range(rook.x, self.x):
                if situation[square][self.y] is not None:
                    free = False
        if free:
            return True
        return False

    def castle(self, situation: list[[]], rook: Rook) -> bool:
        """Checks if castle is possible"""
        if not self.has_moved and not rook.has_moved and not self.is_checked:
            return self._free_spaces(situation, rook)

    def legal_moves(self, situation: list[[]]) -> list:
        """Restricts the list of movements to only legal moves.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now.
        Returns the legal moves"""
        psb_moves = self.movement
        k_rook, q_rook = None, None
        if not self.has_moved:
            k_rook = situation[7][self.y]
            q_rook = situation[0][self.y]
        try:
            # checking if king side castle is possible
            if isinstance(k_rook, Rook) and self.castle(situation, k_rook):
                psb_moves.append([self.x + 2, self.y])
            # checking if queen side castle is possible
            if isinstance(q_rook, Rook) and self.castle(situation, q_rook):
                psb_moves.append([self.x - 2, self.y])
            # checking if the square is defended
            for move in psb_moves:
                if self.is_defended(move, situation) or (situation[move[0]][move[1]] is not None and
                                                         situation[move[0]][move[1]].color == self.color):
                    psb_moves.remove(move)
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
        # checking if the desired move is to castle
        if target[0] == self.x + 2 or target[0] == self.x - 2:
            # finding the rook
            rook_pos = 7 if target[0] == self.x + 2 else 0
            rook = situation[rook_pos][target[self.y]]
            # moving the rook
            rook_target = 5 if rook_pos == 7 else 3
            aux_situation = rook.update_situation([rook_target, self.y], situation)

            new_situation = self.update_situation(target, aux_situation)
        else:
            new_situation = self.update_situation(target, situation)
        return new_situation
