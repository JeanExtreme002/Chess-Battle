from .Piece import Piece
from .Pawn import Pawn
from .Rook import Rook
from enum import Enum
from .Queen import Queen
from .Knight import Knight
from .Bishop import Bishop
from .King import King
from .Color import Color

class Board():
    def __init__(self):
        self.pecas = [[None]*8 for i in range(8)]

        for i in range(8):
            self.add_piece(Pawn(Color.White, i, 1))   

        for i in range(8):
            self.add_piece(Pawn(Color.Black, i, 6))

        wr0 = Rook(Color.White, 0, 0)
        wr1 = Rook(Color.White, 7, 0)
        br0 = Rook(Color.Black, 0, 7)
        br1 = Rook(Color.Black, 7, 7)

        wn0 = Knight(Color.White, 1, 0)
        wn1 = Knight(Color.White, 6, 0)
        bn0 = Knight(Color.Black, 1, 7)
        bn1 = Knight(Color.Black, 6, 7)

        wb0 = Bishop(Color.White, 2, 0)
        wb1 = Bishop(Color.White, 5, 0)
        bb0 = Bishop(Color.Black, 2, 7)
        bb1 = Bishop(Color.Black, 5, 7)

        wk = King(Color.White, 3, 0)
        bk = King(Color.Black, 4, 7)

        wq = Queen(Color.White, 4, 0)
        bq = Queen(Color.Black, 3, 7)

        for p in (wr0, wr1, br0, br1, wn0, wn1, bn0, bn1, wb0, wb1, bb0, bb1, bq, wq, bk, wk):
            self.add_piece(p)

    def add_piece(self, piece):
        self.pecas[piece.y][piece.x] = piece

    def imprimir(self):
        # for i in self.pecas:
        #     print(i.r_id)
        for i in range(8):
            for j in range(8):
                if type(self.pecas[i][j]) == int:
                    print(f"{self.pecas[i][j]:02d}", end=" ")
                elif self.pecas[i][j] == None:
                    print("00", end=" ")
                else:
                    print(f"{self.pecas[i][j].r_id:02d}", end=" ")
            print()

    def write_pos(self):
        for i in range(8):
            print(self.pecas[i])

class Data():
    game_number = 0

    @property
    def currentgame(self):
        file = ""
        return

if __name__ == '__main__':
    tabuleiro = Board()
    tabuleiro.imprimir()
