from .widget import Widget

class HighlightedWidget(Widget):
    """
    Classe para criar caixas de input.
    """
    def __init__(self, screen, x, y, size, color = (0, 0, 0), opacity = 150, widget_group = None):
        super().__init__(screen, x, y, size, widget_group = widget_group)
        self.__color = color
        self.__opacity = opacity
        self.__build()
        
    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        self.__background_batch = self.screen.create_batch()

        self.__background = self.screen.create_rectangle(
            0, 0, self.screen.width, self.screen.height,
            batch = self.__background_batch,
            color = self.__color
        )
        self.__background.opacity = self.__opacity

    def draw(self):
        """
        Desenha o widget na tela.
        """
        self.__background_batch.draw()
