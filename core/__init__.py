from .Player import Player
from typing import Union
from .Piece import Piece
from enum import Enum
from .teste import Board

class ChessGame:
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.__white_player = Player("white")
        self.__black_player = Player("black")
        self.__black_player.played = True
        self.__board = Board()

    @property
    def white_player(self):
        return self.__white_player

    @property
    def black_player(self):
        return self.__black_player

    @property
    def board(self):
        return self.__board
    
    #def new_game(self, first_player=None, timeout=None):
    #    if first_player == None:
    #        first_player = self.__white_player
    #    self.__white_player.played = True #Assumimos que o método get_player será chamado após o 1º jogador fazer um movimento

    def load_game(self, match:int, round:int): #Esperando database ficar pronto (ou quase isso)...
        return NotImplemented

    def get_history(self) -> list: #Mesma coisa do de cima...
        return NotImplemented

    def get_player(self) -> Player:
        self.__white_player.played = not self.__white_player.played
        self.__black_player.played = not self.__black_player.played

        return self.__white_player or self.__black_player

    def get_time(self) -> str: #Esperando implementarem o tempo...
        return NotImplemented

    def get_piece(self, x:int, y:int) -> Piece: #1 ≤ x, y ≤ 8
        x -= 1
        y -= 1
        piece = self.__board.pecas[x][y]

        if piece == 0:
            return

        if (self.__black_player.played and (not piece.r_id%2)) or (self.__white_player.played and piece.r_id%2):
            return

        return piece

    def get_status(self) -> Enum:
        pass

    def play(self, from_:tuple[int, int], to:tuple[int, int]) -> bool:
        pass
