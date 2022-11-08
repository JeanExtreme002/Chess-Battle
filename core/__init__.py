from .Player import Player
from .Piece import Piece
from .Board import Board
from .Color import Color

class ChessGame:
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.__white_player = Player(Color.White)
        self.__black_player = Player(Color.Black)
        self.new_game()

    @property
    def white_player(self):
        return self.__white_player

    @property
    def black_player(self):
        return self.__black_player

    @property
    def board(self):
        return self.__board

    def new_game(self):
        self.__current_player = self.__white_player
        self.__white_player.played = True
        self.__board = Board()

    def load_game(self, match:int, round:int): #Esperando database ficar pronto (ou quase isso)...
        return NotImplemented

    def get_history(self) -> list: #Mesma coisa do de cima...
        return NotImplemented

    def __change_player(self):
        self.__white_player.played = not self.__white_player.played
        self.__black_player.played = not self.__black_player.played

        self.__current_player =  self.__white_player or self.__black_player

    def get_player(self) -> Player:
        return self.__current_player

    def get_time(self) -> str: #Esperando implementarem o tempo...
        return NotImplemented

    def get_piece(self, x:int, y:int) -> Piece: #0 ≤ x, y ≤ 7
        try:
            piece = self.__board.pecas[x][y]
        except KeyError:
            return None

        if piece is None:
            return None

        return piece

    def get_status(self) -> str:
        pass

    def play(self, piece:Piece, to:tuple[int, int]) -> bool:
        if not (list(to) in piece.legal_moves(self.__board.pecas)):
            #Se o movimento não é legal...
            return False

        self.__board.pecas = piece.move(list(to), self.__board.pecas)
        self.__change_player()

        return True
