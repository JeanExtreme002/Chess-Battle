from typing import Union
from enum import Enum

class ChessPiece:
    '''Classe feita apenas para compatibilidade das "type hints". Ela será removida assim que a classe Piece estiver pronta.'''
    pass

class ChessGame:
    def __init__(self, database_path: str):
        pass

    def new_game(self, timeout: bool, first_player:Union[bool, int, Enum]):
        pass

    def load_game(self, match:int, round:int):
        pass

    def get_history(self) -> list:
        pass

    def get_player(self) -> Union[Enum, bool, int]:
        pass

    def get_time(self) -> str:
        pass

    def get_piece(self, x:int, y:int) -> Union[Enum, ChessPiece]:
        pass

    def get_status(self) -> Enum:
        pass

    def play(self, from_:tuple[int, int], to:tuple[int, int]) -> bool:
        pass
