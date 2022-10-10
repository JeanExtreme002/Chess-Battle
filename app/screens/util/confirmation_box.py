from .message_box import MessageBox
from .button import Button
from pyglet.graphics import OrderedGroup

class ConfirmationBox(MessageBox):
    def __init__(self, screen, batch, x, y, size, image, button_images):
        super().__init__(screen, batch, x, y, size, image)

        self.__button_images = button_images
        self.__build()

    def __build(self):
        self.__button_group = OrderedGroup(3)
        button_width = self.width * 0.1
        button_height = button_width * 0.75

        self.__cancel_button = Button(
            self.screen, self.batch, self.x + self.width * 0.2,
            self.y + self.height - button_height - self.width * 0.15,
            (button_width, button_height),
            (self.__button_images[0][0], self.__button_images[0][1]),
            group = self.__button_group
        )

        self.__confirm_button = Button(
            self.screen, self.batch, self.x + self.width * 0.8 - button_width,
            self.y + self.height - button_height - self.width * 0.15,
            (button_width, button_height),
            (self.__button_images[1][0], self.__button_images[1][1]),
            group = self.__button_group
        )

    def check(self, x, y):
        if self.__cancel_button.check(x, y): return True, False
        elif self.__confirm_button.check(x, y): return False, True
        return False, False
