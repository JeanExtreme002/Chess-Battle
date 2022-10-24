from .widget import Widget
from .highlighted_widget import HighlightedWidget

class MediaControl(HighlightedWidget):
    """
    Classe para criar um popup com uma mensagem na tela.
    """
    def __init__(self, screen, x, y, size, images, widget_group = None):
        super().__init__(screen, x, y, size, fill = height * 0.1, widget_group = widget_group)
        
        self.__image = images
        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        pass

    def check(self):
        """
        Verifica se o cursor se encontra na posição do botão.
        """
        pass

    def draw(self):
        """
        Desenha o widget na tela.
        """
        pass
