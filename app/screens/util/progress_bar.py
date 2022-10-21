from .widget import Widget
from pyglet.graphics import OrderedGroup

class ProgressBar(Widget):
    """
    Classe para criar um popup com uma mensagem na tela.
    """
    def __init__(self, screen, batch, x, y, size, text = "", background = (255, 255, 255), color = (255, 0, 0), border_size = 2):
        super().__init__(screen, batch, x, y, size)
        self.__text = text
        self.__border_size = border_size
        
        self.__background = background
        self.__color = color

        self.__progress = 0
        
        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        # Cria a sombra para destacar a caixa de texto.
        self.__shadow_group = OrderedGroup(0)
        
        self.__shadow = self.screen.create_rectangle(
            0, 0, self.screen.width, self.screen.height,
            batch = self.batch, group = self.__shadow_group,
            color = (0, 0, 0)
        )
        self.__shadow.opacity = 150

        # Cria uma borda e a barra "móvel".
        self.__background_group = OrderedGroup(1)
        
        self.__border = self.screen.create_rectangle(
            self.x - self.__border_size, self.y - self.__border_size,
            self.screen.width + self.__border_size * 2,
            self.screen.height + self.__border_size * 2,
            batch = self.batch, group = self.__background_group,
            color = (0, 0, 0)
        )

        self.__background = self.screen.create_rectangle(
            self.x, self.y, self.width, self.screen.height,
            batch = self.batch, group = self.__background_group,
            color = self.__background
        )

        self.__progress_bar = self.screen.create_rectangle(
            self.x, self.y, self.width * self.__progress, self.screen.height,
            batch = self.batch, group = self.__background_group,
            color = self.__color
        )

    def draw(self, with_progress_only = True):
        """
        Desenha o widget, com a possível condição de que haja progresso.
        """
        if with_progress_only and self.__progress == 0: return
        self.batch.draw()

    def get_progress(self):
        """
        Retorna o progresso da barra.
        """
        return self.__progress

    def set_progress(self, progress):
        """
        Define o progresso da barra (0 <= progress <= 1).
        """
        self.__progress = progress
        self.__progress_bar.width = self.width * self.__progress
