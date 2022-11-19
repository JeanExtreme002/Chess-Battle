from app import Application, paths
from core import ChessGame
from locale import getlocale

chess_game = ChessGame(paths.replay_path)

title = "Xadrez de Batalha" if "pt" in getlocale()[0] else "Battle Chess"

application = Application(title, chess_game)
application.run()
