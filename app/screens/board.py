from .screen import Screen
from pyglet import graphics
from pyglet.window import mouse

class BoardScreen(Screen):
    def __init__(self, application, game, player_2_input = None):
        super().__init__(application)

        self.player_2_input = player_2_input
        self.__game = game
        
        self.__build()
        
    def __build(self): pass

    def on_mouse_motion(self, *args):
        x, y = super().on_mouse_motion(*args)[0: 2]

    def on_mouse_release(self, *args):
        x, y, mouse_button = super().on_mouse_release(*args)[0: 3]
        if mouse_button != mouse.LEFT: return

    def on_draw(self, by_scheduler = False): pass
