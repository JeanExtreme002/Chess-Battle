from .screen import Screen
from pyglet.window import mouse, key

class AchievementScreen(Screen):
    """
    Classe para criar uma tela de histórico de partidas.
    """
    
    def __init__(self, application):
        super().__init__(application)
        self.__build()
        
    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar a tela.
        """
        application = self.get_application()
        
        self.__batch = self.create_batch()
        self.__text_batch = self.create_batch()

        # Cria o plano de fundo.
        background_filename = application.paths.get_image("achievement", "background.png")
        self.__background_image = self.load_image(background_filename, (self.width, self.height))

    def on_draw_screen(self, by_scheduler = False):
        """
        Evento para desenhar a tela.
        """
        self.__background_image.blit(0, 0)
        self.__batch.draw()
        self.__text_batch.draw()

    def on_key_press(self, symbol, modifiers):
        """
        Evento de tecla pressionada.
        """
        # Caso o ESC seja apertado, significa que o usuário deseja sair desta tela.
        if symbol == key.ESCAPE:
            self.get_application().go_back()
     
        return True
