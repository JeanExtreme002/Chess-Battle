from .config import paths, settings
from .screens import HomeScreen
from pyglet import window
from pyglet import app
import os

class Application(window.Window):
    
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

    def __initialize_screens(self):
        self.__home_screen = HomeScreen(self, self.__on_play)

    def __on_play(self, selection):
        print("Inciando jogo. Selecionada a opção:", selection)

    def on_draw(self):
        self.clear()
        self.__current_screen.on_draw()

    def on_mouse_motion(self, *args):
        self.__current_screen.on_mouse_motion(*args)

    def on_mouse_release(self, *args):
        self.__current_screen.on_mouse_release(*args)

    def run(self):
        app.run()
