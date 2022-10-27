from .conn import Connection
from .data import achievements, paths, settings
from .screens import AchievementScreen, BoardScreen, HistoryScreen, HomeScreen, SettingsScreen, StartupScreen
from .sound import SoundPlayer
from pyglet import app
from pyglet import canvas
from pyglet import clock
from pyglet import window
from threading import Thread
import os, time

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
        self.__center_window()
        self.paths = paths

        self.__address = settings.address
        self.__connection = None

        self.__chess_game = chess_game
        self.__initialize()

    def __center_window(self):
        """
        Centraliza a janela da aplicação.
        """
        user_screen = canvas.Display().get_screens()[0]
        
        x = int(user_screen.width / 2 - self.width / 2)
        y = int(user_screen.height / 2 - self.height / 2)
        
        self.set_location(x, y)

    def __check_achivements(self):
        """
        Verifica se o usuário pode liberar determinadas
        conquistas obtidas ao iniciar o jogo.
        """
        self.add_achievement("Uma nova jornada começa...", "Iniciou o jogo pela primeira vez.")

        localtime = time.localtime()
        
        if localtime.tm_mday == 20 and localtime.tm_mon == 7:
            self.add_achievement("É dia de xadrez!!", "Iniciou o jogo no dia internacional do xadrez.") 

    def __destroy_screens(self):
        """
        Destrói as telas criadas, liberando o espaço em memória.
        """
        self.__home_screen.free_memory()
        self.__board_screen.free_memory()
        self.__settings_screen.free_memory()
        self.__history_screen.free_memory()
        self.__achievement_screen.free_memory()

    def __initialize(self):
        """
        Inicializa a aplicação.
        """
        self.__initializing = True
        
        # Mostra uma tela de inicialização, enquanto o aplicativo inicializa.
        self.__current_screen = StartupScreen(self)
        clock.schedule_interval(self.on_draw, 1 / self.get_fps())

        # Inicializa o reprodutor de sons.
        self.__sound_player = SoundPlayer(settings.volume, settings.muted)

        # Inicializa as telas do jogo.
        clock.schedule_once(lambda interval: self.__initialize_screens(), 1 / self.get_fps() * 5)

    def __initialize_screens(self):
        """
        Inicializa todas as telas do jogo.
        """
        self.__home_screen = HomeScreen(self)
        self.__home_screen.set_play_function(self.__start_game)
        self.__home_screen.set_settings_function(self.__show_settings_screen)
        self.__home_screen.set_history_function(self.__show_history_screen)
        self.__home_screen.set_achievement_function(self.__show_achievement_screen)
        
        self.__board_screen = BoardScreen(self)
        self.__board_screen.set_board_coordinates(True)
        
        self.__settings_screen = SettingsScreen(self)
        self.__history_screen = HistoryScreen(self)
        self.__achievement_screen = AchievementScreen(self)

        if self.__initializing:
            self.__current_screen.free_memory()
            self.__initializing = False
            
        self.__current_screen = self.__home_screen
        self.__check_achivements()

    def __finish_online_match_by_error(self):
        """
        Encerra a partida online informando que houve um erro.
        """
        self.go_back()
        self.__current_screen.set_popup_message("Conexão perdida.")

        return False

    def __get_movement(self):
        """
        Retorna a jogada realizada pelo outro jogador, se houver.
        """
        if self.__connection.is_connected():
            return self.__connection.recv()

        return self.__finish_online_match_by_error()

    def __send_movement(self, origin, dest):
        """
        Envia a jogada realizada para o outro jogador.
        """
        if self.__connection.is_connected():
            self.__connection.send(origin, dest)
            return True

        return self.__finish_online_match_by_error()
            
    def __show_achievement_screen(self):
        """
        Alterna para a tela de conquistas.
        """
        self.__current_screen = self.__achievement_screen

    def __show_history_screen(self):
        """
        Alterna para a tela de histórico de partidas.
        """
        self.__current_screen = self.__history_screen

    def __show_settings_screen(self):
        """
        Alterna para a tela de configurações.
        """
        self.__current_screen = self.__settings_screen

    def __start_connection(self, host_mode):
        """
        Inicia uma conexão com outro jogador.
        """
        self.__connection = Connection(settings.address, host_mode)
        self.__connection.connect(timeout_in_seconds = 0.3, attempts = 10)
        
        return self.__connection.is_connected()
        
    def __start_game(self, selection):
        """
        Inicia o jogo, dada uma seleção (local ou online).
        """

        # Inicia o jogo localmente.
        if selection == 1: return self.__start_local_game()

        # Inicia o jogo online.
        self.__current_screen.set_popup_message("Procurando por um jogador na rede...", "Por favor, aguarde.")
        clock.schedule_once(lambda interval: self.__start_online_game(selection), 1 / self.get_fps() * 3)

    def __start_local_game(self):
        """
        Inicia o jogo no modo local.
        """
        self.__board_screen.set_new_game(self.__chess_game, self.__board_screen.LOCAL_MODE)
        self.__current_screen = self.__board_screen

    def __start_online_game(self, selection):
        """
        Inicia o jogo no modo online.
        """
        # Tentar estabelecer uma conexão.
        if not self.__start_connection(selection == 2):
            return self.__current_screen.set_popup_message("Infelizmente, não foi possível conectar.", "Por favor, verique a sua conexão.")

        self.__current_screen.set_popup_message(None)
        
        self.__board_screen.set_new_game(
            self.__chess_game, self.__board_screen.ONLINE_MODE,
            self.__send_movement, self.__get_movement, selection == 2
        )
        self.__current_screen = self.__board_screen

    def add_achievement(self, title, description):
        """
        Adiciona uma nova conquista de usuário.
        """
        if achievements.add_achievement(title, description):
            self.__current_screen.set_achievement(title)
  
    def get_fps(self):
        """
        Retorna a taxa de frames por segundo do aplicativo.
        """
        return self.__FRAMES_PER_SECOND

    def get_ip_address(self):
        """
        Retorna o endereço IP do usuário.
        """
        return self.__address[0]

    def get_sound_player(self):
        """
        Retorna o reprodutor de som.
        """
        return self.__sound_player

    def go_back(self):
        """
        Volta uma tela para trás.
        """
        if self.__connection:
            self.__connection.close()
            self.__connection = None
            
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

    def on_mouse_drag(self, *args):
        """
        Evento de botão do mouse pressionado.
        """
        self.__current_screen.on_mouse_drag(*args)

    def on_mouse_motion(self, *args):
        """
        Evento de movimentação do cursor.
        """
        self.__current_screen.on_mouse_motion(*args)

    def on_mouse_release(self, *args):
        """
        Evento de botão do mouse liberado.
        """
        self.__current_screen.on_mouse_release(*args)

    def resize(self, width, height):
        """
        Altera o tamanho da tela do aplicativo.
        """
        if width == self.width and height == self.height: return
        
        self.width = width
        self.height = height
        
        self.__center_window()
        self.__destroy_screens()
        self.__initialize_screens()

    def run(self):
        """
        Inicia a execução do aplicativo.
        """
        app.run()    

    def save_settings(self):
        """
        Salva todas as configurações atuais do aplicativo serão salvas.
        """
        settings.address = self.__address
        settings.size = [self.width, self.height]
        settings.volume = self.__sound_player.get_volume()
        settings.muted = self.__sound_player.is_muted()

    def set_ip_address(self, address):
        """
        Define um endereço IP para o usuário.
        """
        self.__address[0] = address
