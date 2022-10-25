from .widget import Widget
from .highlighted_widget import HighlightedWidget

class Achievement(HighlightedWidget):
    """
    Classe para criar um popup com uma mensagem na tela.
    """
    def __init__(self, screen, size, image, widget_group = None):
        super().__init__(
            screen, self.screen.width - size[0], self.screen.height - size[1],
            size, fill = size[1] * 0.2, opacity = 200, widget_group = widget_group
        )

        self.__frame_counter = 0

        self.__image = image
        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        self.__image_batch = self.screen.create_batch()
        self.__title_batch = self.screen.create_batch()
        self.__description_batch = self.screen.create_batch()

    def draw(self):
        """
        Desenha o widget na tela.
        """
        super().draw()
        
        self.__title_batch.draw()
        self.__description_batch.draw()

    def set_achivement(self, title, *description, colors = ((255, 255, 255, 255), (230, 230, 230, 255)), font_size = 16, line_spacing = 1):
        """
        Define uma mensagem a ser exibida.
        """
        pass
