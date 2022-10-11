from .config import paths, settings
from .conn import Connection
from .screens import BoardScreen, HomeScreen
from .sound import SoundPlayer
from pyglet import app
from pyglet import clock
from pyglet import window
from threading import Thread
import os

class Application(window.Window):

    __FRAMES_PER_SECOND = 60
    
    def __init__(self):
        super().__init__(
            caption = settings.title,
            width = settings.size[0],
            height = settings.size[1],
            resizable = False
        )

        self.paths = paths
        
        self.__sound_player = SoundPlayer()

        self.__initialize_screens()
        clock.schedule_interval(self.on_draw, 1 / self.get_fps())

    def __initialize_screens(self):
        self.__home_screen = HomeScreen(self, self.__on_play)
        self.__board_screen = BoardScreen(self, None, None)
        self.__current_screen = self.__home_screen

    def __start_connection(self, host_mode): pass

    def __on_play(self, selection):     
        if selection >= 2:
            self.__current_screen.set_message("Modo online indisponível no momento", "(ಥ﹏ಥ)")
        else:
            self.__board_screen.set_mode(self.__board_screen.LOCAL_MODE)
            self.__current_screen = self.__board_screen

    def go_back(self):
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

    def run(self):
        app.run()
