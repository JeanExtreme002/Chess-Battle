from app import Application, paths
from core import ChessGame

chess_game = ChessGame(paths.replay_path)

application = Application("Xadrez de Batalha", chess_game)
application.run()
