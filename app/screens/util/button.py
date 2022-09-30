class Button(object):
    def __init__(self, screen, batch, x, y, size, images):
        self.__screen = screen
        self.__batch = batch
        self.__images = images

        self.__activated = False
        self.__previous_status = False

        self.__position = (x, y)
        self.set_size(size)

    def __load_images(self):
        image_1 = self.__screen.load_image(self.__images[0], self.__size)
        image_2 = self.__screen.load_image(self.__images[1], self.__size)
        
        self.__loaded_images = [image_1, image_2]

    def __create_sprite(self):
        self.__sprite = self.__screen.create_sprite(
            self.__loaded_images[int(self.__activated)],
            batch = self.__batch,
            x = self.__position[0],
            y = self.__position[1]
        )

    @property
    def x(self):
        return self.__position[0]

    @property
    def y(self):
        return self.__position[1]

    @property
    def width(self):
        return self.__size[0]

    @property
    def height(self):
        return self.__size[1]

    def check(self, *cursor_pos):
        in_x = self.x <= cursor_pos[0] <= (self.x + self.width)
        in_y = self.y <= cursor_pos[1] <= (self.y + self.height)
        
        self.__activated = (in_x and in_y)

        if self.__previous_status != self.__activated:
            self.__previous_status = self.__activated
            self.__create_sprite()

        return self.__activated

    def set_size(self, size):
        self.__size = size
        self.__load_images()
        self.__create_sprite()
