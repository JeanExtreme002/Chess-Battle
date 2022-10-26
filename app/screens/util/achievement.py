from .highlighted_widget import HighlightedWidget

class Achievement(HighlightedWidget):
    """
    Classe para criar um popup com uma mensagem na tela.
    """
  
    def __init__(self, screen, size, image, font_size, widget_group = None):
        super().__init__(
            screen, screen.width - size[0], screen.height + size[1], size,
            fill = 0, opacity = 200, widget_group = widget_group
        )

        self.__speed = size[1] / (screen.get_application().get_fps() * 0.5)
        self.__show_time = screen.get_application().get_fps() * 2.5

        self.__running = False
        
        self.__frame_counter = 0
        self.__status = 0

        self.__font_size = font_size
        
        self.__image = image
        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        self.__batch = self.screen.create_batch()
        

        image_size = self.height * 0.9
        
        image = self.screen.load_image(self.__image, (image_size, image_size))
        
        self.__image = self.screen.create_sprite(
            image, batch = self.__batch,
            x = self.x + (self.height - image_size) * 0.5,
            y = self.y + self.height * 0.5 - image_size * 0.5
        )

        self.__title = self.screen.create_text(
            str(), self.x + self.height,
            self.y + self.height * 0.5,
            anchor_x = "left", anchor_y = "center",
            batch = self.__batch,
            font_name = "Comic Sans MS",
            font_size = self.__font_size,
            color = (255, 255, 255, 255)
        )  

    def __hide(self):
        """
        Esconde o widget, movendo-o para cima, na janela.
        """
        if self.__frame_counter <= 0: self.__reset()
        else: self.__move(direction = -1)

    def __move(self, direction = 1):
        """
        Move os objetos gráficos verticalmente.
        """
        self.__frame_counter -= self.__speed

        self.__image.y += self.__speed * direction * 2
        self.__title.y += self.__speed * direction * 2
        self._highlight.y += self.__speed * direction * 2

    def __show(self):
        """
        Mostra o widget, movendo-o para cima, na janela.
        """
        if self.__frame_counter <= -self.__show_time:
            self.__frame_counter = self.height
            self.__status = -1
            return

        if self.__frame_counter <= 0: self.__frame_counter -= 1
        else: self.__move(direction = 1)

    def __reset(self):
        """
        Reseta as configurações do widget para seu estado original.
        """
        self.__status, self.__frame_counter = 0, 0

        self.__image.x, self.__image.y = self.__old_image_pos
        self.__title.x, self.__title.y = self.__old_title_pos
        
        self._highlight.x, self._highlight.y = self.__old_highlight_pos
        self.__running = False

    def draw(self):
        """
        Desenha o widget na tela.
        """
        if self.__status == 0: return
        
        super().draw()
        self.__batch.draw()

    def next(self):
        """
        Avança para o próximo estado da animação.
        """
        if self.__status == 1: self.__show()
        if self.__status == -1: self.__hide()

    def set_achievement(self, title):
        """
        Define uma mensagem a ser exibida.
        """

        if self.__running: self.__reset()
        
        self.__old_image_pos = (self.__image.x, self.__image.y)
        self.__old_title_pos = (self.__title.x, self.__title.y)
        
        self.__old_highlight_pos = (self._highlight.x, self._highlight.y)
        
        self.__title.text = title
        self.__frame_counter = self.height
        
        self.__running = True
        self.__status = 1
