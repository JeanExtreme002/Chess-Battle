from Player import Player
from typing import Union
from Piece import Piece
from enum import Enum

class ChessGame:
    def __init__(self, white_player: Player, black_player: Player, database_path: str):
        self.database_path = database_path
        self.white_player = white_player
        self.black_player = black_player

    def new_game(self, first_player:Enum, timeout=None):
        pass

    def load_game(self, match:int, round:int):
        pass

    def get_history(self) -> list:
        pass

    def get_player(self) -> Enum:
        pass

    def get_time(self) -> str:
        pass

    def get_piece(self, x:int, y:int) -> Union[Enum, Piece]:
        pass

    def get_status(self) -> Enum:
        pass

    def play(self, from_:tuple[int, int], to:tuple[int, int]) -> bool:
        pass
