from Piece import Piece
from Pawn import Pawn
from Rook import Rook
from enum import Enum


class Tipo_peca(Enum):
    Black = 1
    White = 0
    Dark = [i for i in range(0, 64, 2)]
    Light = [i for i in range(1, 64, 2)]

class Board():
    
    def __init__(self):
        self.pecas = []
    def add_piece(self,piece):
        self.pecas.append(piece)
    def imprimir(self):
        for i in self.pecas:
            print(i.r_id)
    def write_pos(self):
        for i in self.pecas:

            pass
tabuleiro = Board()
joao = Pawn(0,0,0,1)
jean = Pawn(1,0,1,2)
vitor = Rook(0,1,1,3)
tabuleiro.add_piece(joao)
tabuleiro.add_piece(jean)
tabuleiro.add_piece(vitor)
tabuleiro.imprimir()