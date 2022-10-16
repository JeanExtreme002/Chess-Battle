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
            wp = Pawn(Color.White,i,1)
            self.pecas[1][i] = wp

        for i in range(8):       
            bp = Pawn(Color.Black,i,6)
            self.pecas[6][i] = bp

        wr0 = Rook(Color.White,0,0)
        wr1 = Rook(Color.White,0,7)
        br0 = Rook(Color.Black,7,0)
        br1 = Rook(Color.Black,7,7)

        wn0 = Knight(Color.White,0,1)
        wn1 = Knight(Color.White,0,6)
        bn0 = Knight(Color.Black,7,1)
        bn1 = Knight(Color.Black,7,6)

        wb0 = Bishop(Color.White,0,2)
        wb1 = Bishop(Color.White,0,5)
        bb0 = Bishop(Color.Black,7,2)
        bb1 = Bishop(Color.Black,7,5)

        wk = King(Color.White,0,3)
        bk = King(Color.Black,7,4)

        wq = Queen(Color.White,0,4)
        bq = Queen(Color.Black,7,3)

        for p in (wr0, wr1, br0, br1, wn0, wn1, bn0, bn1, wb0, wb1, bb0, bb1, bq, wq, bk, wk):
            self.add_piece(p)

    def add_piece(self, piece):
        self.pecas[piece.x][piece.y] = piece

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
