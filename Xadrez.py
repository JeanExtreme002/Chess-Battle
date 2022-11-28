from app import Application, paths
from core import ChessGame
from locale import getlocale

import sys
import traceback

def main():
    """
    Função principal para executar o jogo.
    """
    chess_game = ChessGame(paths.replay_path)

    title = "Xadrez de Batalha" if "pt" in getlocale()[0] else "Battle Chess"
    winter_theme = len(sys.argv) > 1 and sys.argv[1].lower() == "winter_theme"

    application = Application(title, chess_game, winter_theme = winter_theme)
    application.run()

def save_errors_to_file(filename):
    """
    Salva o erro gerado em um arquivo.
    """
    with open(filename, "a+") as file:
        traceback.print_exc(file = file)
        file.write("\n" + "=" * 100 + "\n")

# Executa o código principal e, caso haja erro,
# o mesmo será salvo em um arquivo.
try:
    main()
except Exception:
    print("It looks like the game has crashed due to an error. Check it in the log file.")
    save_errors_to_file(filename = "log.txt")
