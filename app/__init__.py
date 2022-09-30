from .config import paths, settings
from .screens import HomeScreen
from pyglet import app
from pyglet import clock
from pyglet import window
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

        self.__initialize_screens()
        self.__current_screen = self.__home_screen
        clock.schedule_interval(self.on_draw, 1 / self.get_fps())

    def __initialize_screens(self):
        self.__home_screen = HomeScreen(self, self.__on_play)

    def __on_play(self, selection):
        print("Inciando jogo. Selecionada a opção:", selection)

    def get_fps(self):
        return self.__FRAMES_PER_SECOND

    def on_draw(self, interval = None):
        self.clear()
        self.__current_screen.on_draw(not interval is None)

    def on_mouse_motion(self, *args):
        self.__current_screen.on_mouse_motion(*args)

    def on_mouse_release(self, *args):
        self.__current_screen.on_mouse_release(*args)

    def run(self):
        app.run()
