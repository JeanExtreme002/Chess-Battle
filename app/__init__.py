import pyglet

class Application(pyglet.window.Window):
    
    def __init__(self):
        super().__init__()

        self.__current_screen = None

    def on_draw(self):
        self.clear()
        print("Desenhando...")

    def run(self):
        pyglet.app.run()
