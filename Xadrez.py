from app import Application, paths
from core import ChessGame
from locale import getlocale

import sys

chess_game = ChessGame(paths.replay_path)

title = "Xadrez de Batalha" if "pt" in getlocale()[0] else "Battle Chess"
winter_theme = len(sys.argv) > 1 and sys.argv[1].lower() == "winter_theme"

application = Application(title, chess_game, winter_theme = winter_theme)
application.run()
