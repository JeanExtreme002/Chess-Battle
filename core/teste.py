from Piece import Piece
from Pawn import Pawn
from Rook import Rook
from enum import Enum
from Queen import Queen
from Color import Color


class Board():

    def __init__(self):
        self.pecas = [[None] * 8 for i in range(8)]

    def add_piece(self, piece):
        self.pecas[piece.x][piece.y] = piece.r_id

    def imprimir(self):
        # for i in self.pecas:
        #     print(i.r_id)
        for i in range(8):
            print(self.pecas[i])

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
joao = Pawn(Color.White, 0, 0)
jean = Pawn(Color.Black, 0, 1)
nanda = Queen(Color.Black, 2, 0)
tabuleiro.add_piece(joao)
tabuleiro.add_piece(jean)
tabuleiro.add_piece(nanda)
tabuleiro.imprimir()