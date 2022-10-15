from Piece import Piece
from Pawn import Pawn
from Rook import Rook
from enum import Enum
from Queen import Queen
from Knight import Knight
from Bishop import Bishop
from King import King


class Board():
    
    def __init__(self):
        self.pecas = [[0]*8 for i in range(8)]
        for i in range(8):       
            wp = Pawn(0,i,1)
            self.pecas[1][i] = wp
        for i in range(8):       
            bp = Pawn(1,i,1)
            self.pecas[6][i] = bp
        wr0 = Rook(0,0,0)
        wr1 = Rook(0,0,7)
        br0 = Rook(1,7,0)
        br1 = Rook(1,7,7)
        wn0 = Knight(0,0,1)
        wn1 = Knight(0,0,6)
        bn0 = Knight(1,7,1)
        bn1 = Knight(1,7,6)
        wb0 = Bishop(0,0,2)
        wb1 = Bishop(0,0,5)
        bb0 = Bishop(1,7,2)
        bb1 = Bishop(1,7,5)
        wk = King(0,0,3)
        bk = King(1,7,4)
        wq = Queen(0,0,4)
        bq = Queen(1,7,3)
        self.add_piece(wr0)
        self.add_piece(wr1)
        self.add_piece(br0)
        self.add_piece(br1)
        self.add_piece(wn0)
        self.add_piece(wn1)
        self.add_piece(bn0)
        self.add_piece(bn1)
        self.add_piece(wb0)
        self.add_piece(wb1)
        self.add_piece(bb0)
        self.add_piece(bb1)
        self.add_piece(bq)
        self.add_piece(wq)
        self.add_piece(bk)
        self.add_piece(wk)
    def add_piece(self,piece):
        self.pecas[piece.x][piece.y]= piece.r_id
    def imprimir(self):
        # for i in self.pecas:
        #     print(i.r_id)
        for i in range(8):
            for j in range(8):
                if(type(self.pecas[i][j])==int):
                    print(self.pecas[i][j],end="")
                else:
                    print(self.pecas[i][j].r_id,end="")
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

tabuleiro = Board()
tabuleiro.imprimir()