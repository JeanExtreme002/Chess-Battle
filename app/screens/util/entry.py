from .widget import Widget

class Entry(Widget):
    """
    Classe para criar caixas de input.
    """
    def __init__(self, screen, x, y, size, border = 0, default_text = "", widget_group = None):
        super().__init__(screen, x, y, size, widget_group = widget_group)
        self.__border_size = border
        self.__default_text = default_text
        
        self.__selected = False
        self.__pipe_on = False
        
        self.__pipe_interval = int(screen.get_application().get_fps() * 0.8)
        self.__frames = 0
        
        self.__input_string = str()
        self.__build()
        
        self.update_text()
        
    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        self.__background_batch = self.screen.create_batch()
        self.__text_batch = self.screen.create_batch()
        
        self.__border = self.screen.create_rectangle(
            self.x - self.__border_size, self.y - self.__border_size,
            self.width + self.__border_size * 2,
            self.height + self.__border_size * 2,
            batch = self.__background_batch,
            color = (0, 0, 0)
        )

        self.__background = self.screen.create_rectangle(
            self.x, self.y, self.width, self.height,
            batch = self.__background_batch,
            color = (255, 255, 255)
        )

        self.__text = self.screen.create_text(
            self.__input_string, self.x + 5, self.y + self.height // 2,
            anchor_x = "left", anchor_y = "center",
            batch = self.__text_batch,
            font_size = self.height * 0.4,
            color = (0, 0, 0, 255)
        )

    def add_char(self, char):
        """
        Adiciona um caractere ao final da caixa de texto.
        """
        self.__input_string += char
        self.update_text()
        return True

    def check(self, *cursor_pos):
        """
        Verifica se o cursor se encontra na posição da caixa de texto.
        """
        in_x = self.x <= cursor_pos[0] <= (self.x + self.width)
        in_y = self.y <= cursor_pos[1] <= (self.y + self.height)
        
        if in_x and in_y:
            self.__background.color = (240, 240, 240)
            return True
        
        self.__background.color = (250, 250, 250)
        return False

    def clear(self):
        """
        Limpa a caixa de texto.
        """
        self.__input_string = ""
        self.update_text()

    def delete_char(self):
        """
        Apaga o último caractere da caixa de texto.
        """
        if not self.__input_string: return
        
        self.__input_string = self.__input_string[:-1]
        self.update_text()

    def draw(self):
        """
        Desenha o widget na tela.
        """
        self.__background_batch.draw()
        self.__text_batch.draw()

    def get_text(self):
        """
        Retorna o texto da caixa de texto.
        """
        return self.__input_string

    def next(self):
        """
        Avança para o próximo estado da animação.
        """
        self.__frames = (self.__frames + 1) % self.__pipe_interval
        if self.__frames == 0: self.__pipe_on = not self.__pipe_on
        
        self.update_text()

    def set_pipe(self, boolean):
        """
        Ativa ou desativa o pipe.
        """
        self.__selected = boolean

    def update_text(self):
        """
        Atualiza o objeto gráfico de texto.
        """
        if not self.__input_string:
            self.__text.text = self.__default_text
            self.__text.color = (60, 60, 60, 255)
            
        else:
            self.__text.text = self.__input_string + ("|" if self.__pipe_on and self.__selected else "")
            self.__text.color = (0, 0, 0, 255)
