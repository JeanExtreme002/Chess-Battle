from .Player import Player
from .Piece import Piece
from .Board import Board
from .Color import Color
from .Data import GameData
from copy import deepcopy

class FinishedGameError(Exception):
    pass

class NoPromotionError(Exception):
    pass

class GameModeError(Exception):
    pass

class ChessGame:
    def __init__(self, replay_path: str):
        self.__game_data = GameData(replay_path)
        self.__white_player = Player(Color.White)
        self.__black_player = Player(Color.Black)
        self.__status = "normal"
        self.__check_legal_moves = {}
        self.__replaying = False

    @property
    def white_player(self):
        if self.__replaying:
            raise GameModeError("Você não pode usar esse atributo no modo replay")
        return self.__white_player

    @property
    def black_player(self):
        if self.__replaying:
            raise GameModeError("Você não pode usar esse atributo no modo replay")
        return self.__black_player

    @property
    def board(self):
        return self.__board

    @property
    def id(self):
        return self.__game_data.id

    def close(self):
        self.__replaying = False
        self.__game_data.close()

    def back(self):
        if not self.__replaying:
            raise GameModeError("Você deve iniciar o modo replay para usar esse método")
        
        self.__game_data.back()
        self.__board.pecas = self.__game_data.read()

    def next(self):
        if not self.__replaying:
            raise GameModeError("Você deve iniciar o modo replay para usar esse método")
        
        self.__game_data.back()
        self.__board.pecas = self.__game_data.read()

    def start_replay(self, game_id):
        self.close()
        self.__replaying = True
        
        self.__game_data.open(game_id)
        self.__board.pecas = self.__game_data.read()

    def new_game(self, name = "game"):
        self.close()
        
        self.__current_player = self.__white_player
        self.__white_player.played = True
        self.__winner = None
        self.__board = Board()
        self.__status = "normal"
        self.__game_data.open(game_name = name)
        self.__white_player.king = self.__board.pecas[0][3]
        self.__black_player.king = self.__board.pecas[7][3]     

    def get_history(self) -> list:
        return self.__game_data.get_game_list()

    def __change_player(self):
        self.__white_player.played = not self.__white_player.played
        self.__black_player.played = not self.__black_player.played

        self.__current_player =  self.__white_player or self.__black_player

    def __gen_defense_table(self, player, board=None) -> list[[]]:
        if board is None:
            board = self.__board.pecas

        new_defense_table = [[False for _ in range(8)] for _ in range(8)]

        for x in range(8):
            for y in range(8):
                peca = self.get_piece(x, y)
                if peca == None or peca.color != player.color:
                    continue

                for m in peca.legal_moves(board):
                    new_defense_table[m[0]][m[1]] = True

        return new_defense_table

    def __defense_update(self):
        for p in (self.__white_player, self.__black_player):
            p.defense = self.__gen_defense_table(p)

    def __check_legal_moves_update(self):
        play_color = self.__current_player.color
        pkpx, pkpy = self.__current_player.king.x, self.__current_player.king.y
        new_clm = {}

        for x in range(8):
            for y in range(8):
                peca = self.get_piece(x, y)
                if peca == None or peca.color != play_color:
                    continue

                for mov in peca.legal_moves(self.__board.pecas):
                    if self.__simule_check_out(peca.coords, mov):
                        new_clm[peca.coords] = new_clm.get(peca.coords, []) + [mov]

        self.__check_legal_moves = new_clm

    def __check_verify(self):
        adv_player = self.__white_player if self.__current_player == self.__black_player else self.__black_player
        king_pos = self.__current_player.king.x, self.__current_player.king.y
        if adv_player.defense[king_pos[1]][king_pos[0]]:
            self.__status = "xeque"
        else:
            self.__status = "normal"

    def __simule_check_out(self, from_, to) -> bool:
        adv_player = self.__white_player if self.__current_player == self.__black_player else self.__black_player

        xi, yi = from_
        xf, yf = to
        board = deepcopy(self.__board.pecas)
        piece = board[yi][xi]
        board[yf][xf] = piece
        piece.x = xf
        piece.y = yf
        board[yi][xi] = None
        defended = self.__gen_defense_table(adv_player, board)

        return not defended[self.__current_player.king.y][self.__current_player.king.x]

    def has_promotion(self):
        if self.__replaying:
            raise GameModeError("Você não pode usar esse método no modo replay")
        return bool(self.__board.check_promotion()) and not self.get_winner()

    def set_promotion(self, piece_name):
        if self.__replaying:
            raise GameModeError("Você não pode usar esse método no modo replay")
        
        if not self.__has_promotion():
            NoPromotionError("Não há promoções disponíveis no momento")
            
        self.__board.set_promotion(piece_name)
        self.__change_player()

    def get_player(self) -> Player:
        if self.__replaying:
            raise GameModeError("Você não pode usar esse método no modo replay")
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
        if self.__replaying:
            raise GameModeError("Você não pode usar esse método no modo replay")
        return self.__winner

    def play(self, piece:Piece, to:tuple[int, int]) -> bool:
        if self.__replaying:
            raise GameModeError("Você não pode usar esse método no modo replay")
        
        if self.__winner:
            raise FinishedGameError("A partida já encerrou")

        if self.has_promotion():
            raise NoPromotionError("Promova o peão antes de jogar")
        
        if not (list(to) in piece.legal_moves(self.__board.pecas)):
            #Se o movimento não é legal...
            return False

        if self.__status == "xeque":
            self.__check_legal_moves_update()
            try:
                mov = self.__check_legal_moves[piece.coords]
                if not (to in mov):
                    raise KeyError

                self.__status = "normal"

            except KeyError:
                cor_msg = 'branco' if self.__current_player.color == Color.White else "preto"
                print(f"Tire o rei {cor_msg} do xeque!")
                return False

        target_piece = self.__board.pecas[to[0]][to[1]]
        
        if target_piece and target_piece.name == "king":
            self.__winner = piece.color

        self.__board.pecas = piece.move(list(to), self.__board.pecas)

        if not self.has_promotion():
            self.__game_data.save(self.__board.pecas)
            self.__change_player()

        if self.__winner:
            self.__game_data.close(self.__winner)

        self.__defense_update()
        self.__check_verify()

        return True
