class Slide(object):
    def __init__(self, screen, batch, x, y, size, images):
        super().__init__(screen, batch, x, y, size)

        self.__images = images
        self.__load_images()

    def __load_images(self):
        self.__loaded_images = []
        
        for filename in self.__images:
            image = self.screen.load_image(filename, (self.width, self.height))
            self.__loaded_images.append(image)

    def __create_sprite(self):
        self.__sprite = self.__screen.create_sprite(
            self.__loaded_images[int(self.__activated)],
            batch = self.__batch,
            x = self.__position[0],
            y = self.__position[1]
        )
