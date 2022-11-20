from .widget import Widget

class HighlightedWidget(Widget):
    """
    Classe para criar caixas de input.
    """
    def __init__(self, screen, x, y, size, color = (0, 0, 0), opacity = 150, fill = "expand", widget_group = None):
        super().__init__(screen, x, y, size, widget_group = widget_group)
        self.__color = color
        self.__opacity = opacity
        self.__fill = fill
        self.__build()
        
    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        x = 0 if self.__fill == "expand" else self.x - self.__fill
        y = 0 if self.__fill == "expand" else self.y - self.__fill
        
        width = self.screen.width if self.__fill == "expand" else self.width + self.__fill * 2
        height = self.screen.height if self.__fill == "expand" else self.height + self.__fill * 2

        self._highlight = self.screen.create_rectangle(
            x, y, width, height, color = self.__color
        )
        self._highlight.opacity = self.__opacity

    def draw(self):
        """
        Desenha o widget na tela.
        """
        self._highlight.draw()

    def get_opacity(self) -> int:
        """
        Retorna a opacidade do widget.
        """
        return self._highlight.opacity

    def set_opacity(self, value: int):
        """
        Define a opacidade do widget.
        """
        self._highlight.opacity = value
