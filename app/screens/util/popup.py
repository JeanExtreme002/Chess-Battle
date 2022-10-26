from .highlighted_widget import HighlightedWidget

class Popup(HighlightedWidget):
    """
    Classe para criar um popup com uma mensagem na tela.
    """
    def __init__(self, screen, x, y, size, image, widget_group = None):
        super().__init__(screen, x, y, size, widget_group = widget_group)

        self.__texts = []
        
        self.__image = image
        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        # Cria a imagem de background da caixa de texto.
        self.__loaded_image = self.screen.load_image(self.__image, (self.width, self.height))
        
        self.__background_batch = self.screen.create_batch()
        
        self.__background = self.screen.create_sprite(
            self.__loaded_image, batch = self.__background_batch,
            x = self.x, y = self.y
        )

        # Cria um grupo para os textos.
        self.__text_batch = self.screen.create_batch()

    def delete_message(self):
        """
        Apaga a mensagem.
        """
        for text in self.__texts:
            text.delete()
        self.__texts = []

    def draw(self, with_message_only = True):
        """
        Desenha o widget na tela, com a possível condição de que haja mensagem.
        """
        if with_message_only and not self.__texts: return False

        super().draw()
        
        self.__background_batch.draw()
        self.__text_batch.draw()

        return True

    def has_message(self):
        """
        Verifica se existe mensagem a ser exibida.
        """
        return len(self.__texts) > 0

    def set_message(self, x, y, *lines, color = (0, 0, 0, 255), font_size = 16, anchor = ("center", "center"), line_spacing = 1):
        """
        Define uma mensagem a ser exibida.
        """
        self.delete_message()
        line_index = 0
        
        for line in lines:
            text = self.screen.create_text(
                line, x = int(x), y = int(y + line_spacing * line_index),
                batch = self.__text_batch, color = color, font_size = int(font_size),
                anchor_x = anchor[0], anchor_y = anchor[1]
            )
            self.__texts.append(text)
            line_index += 1
