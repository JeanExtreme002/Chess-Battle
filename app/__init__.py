from .config import paths, settings
from .conn import Connection
from .screens import BoardScreen, HomeScreen, SettingsScreen
from .sound import SoundPlayer
from pyglet import app
from pyglet import clock
from pyglet import window
from threading import Thread
import os

class Application(window.Window):
    """
    Classe principal do aplicativo.
    """
    
    __FRAMES_PER_SECOND = 60
    
    def __init__(self, title, chess_game):
        super().__init__(
            caption = title,
            width = settings.size[0],
            height = settings.size[1],
            resizable = False
        )

        self.paths = paths

        self.__chess_game = chess_game
        self.__sound_player = SoundPlayer(settings.volume, settings.muted)

        self.__initialize_screens()
        self.__current_screen = self.__home_screen
        
        clock.schedule_interval(self.on_draw, 1 / self.get_fps())

    def __initialize_screens(self):
        """
        Inicializa todas as telas do jogo.
        """
        self.__home_screen = HomeScreen(self)
        self.__home_screen.set_play_function(self.__start_game)
        self.__home_screen.set_settings_function(self.__show_settings_screen)
        self.__home_screen.set_history_function(self.__show_history_screen)
        self.__home_screen.set_achivements_function(self.__show_achivements_screen)
        
        self.__board_screen = BoardScreen(self)
        self.__board_screen.set_board_coordinates(True)
        
        self.__settings_screen = SettingsScreen(self)

    def __show_achivements_screen(self):
        """
        Alterna para a tela de conquistas.
        """
        self.__current_screen.set_message("Conquistas indisponíveis no momento", "(ಥ﹏ಥ)")

    def __show_history_screen(self):
        """
        Alterna para a tela de histórico de partidas.
        """
        self.__current_screen.set_message("Histórico indisponível no momento", "(ಥ﹏ಥ)")

    def __show_settings_screen(self):
        """
        Alterna para a tela de configurações.
        """
        self.__current_screen = self.__settings_screen

    def __start_connection(self, host_mode):
        """
        Inicia uma conexão com outro jogador.
        """
        pass

    def __start_game(self, selection):
        """
        Inicia o jogo, dada uma seleção (local ou online).
        """
        if selection >= 2:
            self.__current_screen.set_message("Modo online indisponível no momento", "(ಥ﹏ಥ)")
        else:
            self.__board_screen.set_new_game(self.__chess_game, self.__board_screen.LOCAL_MODE)
            self.__current_screen = self.__board_screen

    def get_fps(self):
        """
        Retorna a taxa de frames por segundo do aplicativo.
        """
        return self.__FRAMES_PER_SECOND

    def get_ip_address(self):
        """
        Retorna o endereço IP do usuário.
        """
        return settings.address[0]

    def get_sound_player(self):
        """
        Retorna o reprodutor de som.
        """
        return self.__sound_player

    def go_back(self):
        """
        Volta uma tela para trás.
        """
        if isinstance(self.__current_screen, SettingsScreen):
            settings.volume = self.__sound_player.get_volume()
            settings.muted = self.__sound_player.is_muted()
            
        self.__current_screen = self.__home_screen

    def on_draw(self, interval = None):
        """
        Evento para desenhar a tela.
        """
        self.clear()
        self.__current_screen.on_draw(not interval is None)

    def on_key_press(self, *args):
        """
        Evento de tecla pressionada.
        """
        self.__current_screen.on_key_press(*args)

    def on_mouse_motion(self, *args):
        """
        Evento de movimentação do cursor.
        """
        self.__current_screen.on_mouse_motion(*args)

    def on_mouse_release(self, *args):
        """
        Evento de botão do mouse pressionado e liberado.
        """
        self.__current_screen.on_mouse_release(*args)

    def resize(self, width, height):
        """
        Altera o tamanho da tela do aplicativo.
        """
        settings.size = [width, height]
        self.width = width
        self.height = height
        self.__initialize_screens()

    def run(self):
        """
        Inicia a execução do aplicativo.
        """
        app.run()

    def set_ip_address(self, address):
        """
        Define um endereço IP para o usuário.
        """
        settings.address[0] = address
