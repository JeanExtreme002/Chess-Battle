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

    __FRAMES_PER_SECOND = 60
    
    def __init__(self, title):
        super().__init__(
            caption = title,
            width = settings.size[0],
            height = settings.size[1],
            resizable = False
        )

        self.paths = paths
        
        self.__sound_player = SoundPlayer(settings.volume, settings.muted)

        self.__initialize_screens()
        self.__current_screen = self.__home_screen
        clock.schedule_interval(self.on_draw, 1 / self.get_fps())

    def __initialize_screens(self):
        self.__home_screen = HomeScreen(self)
        self.__home_screen.set_play_function(self.__start_game)
        self.__home_screen.set_settings_function(self.__show_settings_screen)
        self.__home_screen.set_history_function(self.__show_history_screen)
        self.__home_screen.set_achivements_function(self.__show_achivements_screen)
        
        self.__board_screen = BoardScreen(self)
        self.__settings_screen = SettingsScreen(self)

    def __start_connection(self, host_mode): pass

    def __show_settings_screen(self):
        self.__current_screen = self.__settings_screen

    def __show_history_screen(self):
        self.__current_screen.set_message("Histórico indisponível no momento", "(ಥ﹏ಥ)")

    def __show_achivements_screen(self):
        self.__current_screen.set_message("Troféus indisponíveis no momento", "(ಥ﹏ಥ)")

    def __start_game(self, selection):     
        if selection >= 2:
            self.__current_screen.set_message("Modo online indisponível no momento", "(ಥ﹏ಥ)")
        else:
            self.__board_screen.set_game(None, self.__board_screen.LOCAL_MODE)
            self.__current_screen = self.__board_screen

    def go_back(self):
        
        if isinstance(self.__current_screen, SettingsScreen):
            settings.volume = self.__sound_player.get_volume()
            settings.muted = self.__sound_player.is_muted()
            
        self.__current_screen = self.__home_screen

    def get_fps(self):
        return self.__FRAMES_PER_SECOND

    def get_sound_player(self):
        return self.__sound_player

    def on_draw(self, interval = None):
        self.clear()
        self.__current_screen.on_draw(not interval is None)

    def on_key_press(self, *args):
        self.__current_screen.on_key_press(*args)

    def on_mouse_motion(self, *args):
        self.__current_screen.on_mouse_motion(*args)

    def on_mouse_release(self, *args):
        self.__current_screen.on_mouse_release(*args)

    def resize(self, width, height):
        settings.size = [width, height]
        self.width = width
        self.height = height
        self.__initialize_screens()

    def run(self):
        app.run()
