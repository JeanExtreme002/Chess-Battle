import io
import os

class GameData():
    
    __PIECE_NAMES = ["pawn", "king", "knight", "queen", "bishop", "piece", "rook"]
    
    def __init__(self, directory):
        self.__directory = directory
        self.__file = None
        self.__closed = True

    def __get_game_id(self):
        return len([filename for filename in os.listdir(self.__directory) if filename.endswith(".replay")])

    def __get_piece_id(self, piece):
        if not piece: return "00"
        
        piece_id = str(self.__PIECE_NAMES.index(piece.name) + 1) # ID de peça
        piece_id += str(piece.color.value)                       # ID de cor
        
        return piece_id

    def close(self, winner = None):
        if self.__closed: return
        
        self.__file.close()
        self.__file = None
        
        self.__closed = True

        # Renomeia o arquivo temporário.
        if not self.__read_mode and not winner is None:
            new_filename = "{}_{}x{}_{}.replay".format(winner.value, *self.__score, self.__get_game_id()) # WINNER_NxM_GAMEID.replay
            new_filename = os.path.join(self.__directory, new_filename)
            os.rename(self.__filename, new_filename)

        # Se a partida encerrou sem vencedores, o jogo não é salvo.
        if not self.__read_mode and winner is None:
            os.remove(self.__filename)

    def get_game_list(self):
        games = []

        for filename in os.listdir(self.__directory):
            if filename.endswith(".replay") and filename.count("_") == 2:
                data = filename.rstrip(".replay").split("_")
                winner = "WHITE" if data[0] == "0" else "BLACK"
                score = data[1].split("x")
                game_id = data[2]
                
                games.append([winner, score[0], score[1], game_id])
        return games

    def open(self, game_id = None):
        if self.__file: raise io.UnsupportedOperation("file is already open")
        
        if game_id:
            for filename in os.listdir(self.__directory):
                if filename.endswith(".replay") and "_{}".format(game_id) in filename:
                    filename = os.path.join(self.__directory, filename)
                    break
        else: filename = os.path.join(self.__directory, str(os.getpid()) + ".temp".format(game_id))
                    
        self.__read_mode = bool(not game_id is None)
        self.__filename = filename
        self.__closed = False

        self.__file = open(self.__filename, "r" if self.__read_mode else "w")
    
    def save(self, board: list):
        if self.__read_mode or self.__closed: raise io.UnsupportedOperation("not writable")

        self.__score = [0, 0]
        
        for row in board:
            for piece in row:
                self.__file.write(self.__get_piece_id(piece))
                if piece: self.__score[piece.color.value] += 1
                
        self.__file.write("\n")
        
        

