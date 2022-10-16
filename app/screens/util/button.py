from .widget import Widget

class Button(Widget):
    """
    Classe para criar botões na tela.
    """
    def __init__(self, screen, batch, x, y, size, images, group = None):
        super().__init__(screen, batch, x, y, size)
        
        self.__activated = False
        self.__previous_status = False
        self.__group = group
        
        self.__sprite = None
        self.change_image(images)

    def __load_images(self):
        """
        Carrega as imagens do botão.
        """
        image_1 = self.screen.load_image(self.__images[0], (self.width, self.height))
        image_2 = self.screen.load_image(self.__images[1], (self.width, self.height))
        
        self.__loaded_images = [image_1, image_2]

    def __create_sprite(self):
        """
        Cria a imagem do botão.
        """
        self.__sprite = self.screen.create_sprite(
            self.__loaded_images[int(self.__activated)],
            batch = self.batch, x = self.x, y = self.y,
            group = self.__group
        )

    def __delete_sprite(self):
        """
        Deleta a imagem do botão.
        """
        if self.__sprite is not None: self.__sprite.delete()

    def change_image(self, images):
        """
        Troca as imagens do botão.
        """
        self.__images = images
        self.__load_images()
        self.__delete_sprite()
        self.__create_sprite()

    def check(self, *cursor_pos):
        """
        Verifica se o cursor se encontra na posição do botão.
        """
        in_x = self.x <= cursor_pos[0] <= (self.x + self.width)
        in_y = self.y <= cursor_pos[1] <= (self.y + self.height)
        
        self.__activated = (in_x and in_y)

        # Se sim, a imagem do botão será alterada para a imagem de botão ativo.
        if self.__previous_status != self.__activated:
            self.__previous_status = self.__activated
            self.__delete_sprite()
            self.__create_sprite()

        return self.__activated
