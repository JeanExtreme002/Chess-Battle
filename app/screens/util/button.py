from .widget import Widget

class Button(Widget):
    def __init__(self, screen, batch, x, y, size, images, group = None):
        super().__init__(screen, batch, x, y, size)
        
        self.__activated = False
        self.__previous_status = False
        self.__images = images
        self.__group = group

        self.__load_images()
        self.__create_sprite()

    def __load_images(self):
        image_1 = self.screen.load_image(self.__images[0], (self.width, self.height))
        image_2 = self.screen.load_image(self.__images[1], (self.width, self.height))
        
        self.__loaded_images = [image_1, image_2]

    def __create_sprite(self):
        self.__sprite = self.screen.create_sprite(
            self.__loaded_images[int(self.__activated)],
            batch = self.batch, x = self.x, y = self.y,
            group = self.__group
        )

    def __delete_sprite(self):
        self.__sprite.delete()

    def check(self, *cursor_pos):
        in_x = self.x <= cursor_pos[0] <= (self.x + self.width)
        in_y = self.y <= cursor_pos[1] <= (self.y + self.height)
        
        self.__activated = (in_x and in_y)

        if self.__previous_status != self.__activated:
            self.__previous_status = self.__activated
            self.__delete_sprite()
            self.__create_sprite()

        return self.__activated
