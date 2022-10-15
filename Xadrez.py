from app import Application, paths
from core import ChessGame

chess_game = ChessGame(paths.database_path)

application = Application("Xadrez", chess_game)
application.run()
