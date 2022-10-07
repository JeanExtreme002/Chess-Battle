from .widget import Widget
from pyglet.graphics import OrderedGroup

class MessageBox(Widget):
    def __init__(self, screen, batch, x, y, size, image):
        super().__init__(screen, batch, x, y, size)

        self.__texts = []
        
        self.__image = image
        self.__build()

    def __build(self):
        # Cria a sombra para destacar a caixa de texto.
        self.__shadow_group = OrderedGroup(0)
        
        self.__shadow = self.screen.create_rectangle(
            0, 0, self.screen.width, self.screen.height,
            batch = self.batch, group = self.__shadow_group,
            color = (0, 0, 0)
        )
        self.__shadow.opacity = 150

        # Cria a imagem de background da caixa de texto.
        self.__loaded_image = self.screen.load_image(self.__image, (self.width, self.height))
        
        self.__box_group = OrderedGroup(1)
        
        self.__sprite = self.screen.create_sprite(
            self.__loaded_image, batch = self.batch,
            group = self.__box_group, x = self.x, y = self.y
        )

        # Cria um grupo para os textos.
        self.__text_group = OrderedGroup(2)

    def delete_message(self):
        for text in self.__texts:
            text.delete()
        self.__texts = []

    def draw(self, with_messages_only = True):
        if with_messages_only and not self.__texts: return
        self.batch.draw()

    def has_message(self):
        return len(self.__texts) > 0

    def set_message(self, x, y, *lines, color = (0, 0, 0, 255), font_size = 16, anchor = ("center", "center"), line_spacing = 1):
        self.delete_message()
        line_index = 0
        
        for line in lines:
            text = self.screen.create_text(
                line, x = x, y = y + line_spacing * line_index,
                batch = self.batch, group = self.__text_group,
                color = color, font_size = font_size,
                anchor_x = anchor[0], anchor_y = anchor[1]
            )
            self.__texts.append(text)
            line_index += 1
