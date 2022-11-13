from .Player import Player
from .Piece import Piece
from .Board import Board
from .Color import Color
from .Data import GameData

class FinishedGameError(Exception):
    pass

class NoPromotionError(Exception):
    pass

class ChessGame:
    def __init__(self, replay_path: str):
        self.__game_data = GameData(replay_path)
        self.__white_player = Player(Color.White)
        self.__black_player = Player(Color.Black)

    @property
    def white_player(self):
        return self.__white_player

    @property
    def black_player(self):
        return self.__black_player

    @property
    def board(self):
        return self.__board

    def close(self):
        self.__game_data.close()

    def start_replay(self): # Falta implementar, para fazer o modo de jogo ser REPLAY, não permitindo o uso do método PLAY
        return NotImplemented

    def new_game(self):
        self.__current_player = self.__white_player
        self.__white_player.played = True
        self.__winner = None
        self.__board = Board()
        self.__game_data.open()

    def get_history(self) -> list:
        return self.__game_data.get_game_list()

    def __change_player(self):
        self.__white_player.played = not self.__white_player.played
        self.__black_player.played = not self.__black_player.played

        self.__current_player =  self.__white_player or self.__black_player

    def __defense_update(self):
        board = self.__board.pecas
        for p in (self.__white_player, self.__black_player):
            del p.defense

        for x in range(8):
            for y in range(8):
                peca = self.get_piece(x, y)
                if peca == None:
                    continue

                player = self.__white_player if peca.color == Color.White else self.__black_player
                for m in peca.legal_moves(board):
                    player.set_defended_pos(*m)

    def has_promotion(self):
        return bool(self.__board.check_promotion())

    def set_promotion(self, piece_name):
        self.__board.set_promotion(piece_name)

    def get_player(self) -> Player:
        return self.__current_player

    def get_piece(self, x:int, y:int) -> Piece: #0 ≤ x, y ≤ 7
        try:
            piece = self.__board.pecas[x][y]
        except KeyError:
            return None

        if piece is None:
            return None

        return piece

    def get_winner(self):
        return self.__winner

    def play(self, piece:Piece, to:tuple[int, int]) -> bool:
        if self.__winner:
            raise FinishedGameError("A partida já encerrou")

        if self.has_promotion():
            raise NoPromotionError("Promova o peão antes de jogar")
        
        if not (list(to) in piece.legal_moves(self.__board.pecas)):
            #Se o movimento não é legal...
            return False

        target_piece = self.__board.pecas[to[0]][to[1]]
        
        if target_piece and target_piece.name == "king":
            self.__winner = piece.color

        self.__board.pecas = piece.move(list(to), self.__board.pecas)
        self.__change_player()
        self.__defense_update()

        self.__game_data.save(self.__board.pecas)

        if self.__winner:
            self.__game_data.close(self.__winner)

        return True
