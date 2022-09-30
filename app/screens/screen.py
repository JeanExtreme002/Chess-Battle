from abc import ABC, abstractmethod
from pyglet import image
from pyglet import gl
from pyglet import shapes
from pyglet import sprite
from pyglet import text

# Configuração para habilitar o redimensionamento de imagens.
gl.glEnable(gl.GL_TEXTURE_2D)
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)


class Screen(ABC):
    """
    Classe para gerar telas.
    """
    def __init__(self, application):
        self.__application = application
        self.__images = dict()
        
    @property
    def width(self):
        return self.__application.width

    @property
    def height(self):
        return self.__application.height

    def __get_true_y_position(self, y, height = 0):
        return self.height - y - height

    def create_text(self, string, x, y, **kwargs):
        return text.Label(string, x = x, y = y, **kwargs)

    def create_rectangle(self, x, y, width, height, **kwargs):
        y = self.__get_true_y_position(y, height)
        height *= -1

        shape = shapes.Rectangle(
            x = x, y = y,
            width = width,
            height = height,
            **kwargs
        )
        return shape

    def create_sprite(self, img, x, y, **kwargs):
        y = self.__get_true_y_position(y, img.height)
        return sprite.Sprite(img, x = x, y = y, **kwargs)

    def load_image(self, filename, size = None, save = True):

        # Carrega a imagem.
        if not filename in self.__images:
            img = image.load(filename)
            if save: self.__images[filename] = img
        else:
            img = self.__images[filename]

        # Redefine o seu tamanho, caso solicitado, alterando a sua escala.
        if size:
            img = img.get_texture() 
            img.width = size[0]
            img.height = size[1]

        return img

    def get_application(self):
        return self.__application

    def get_pixels_by_percent(self, x, y):
        width = self.width / 100 * x
        height = self.height / 100 * y
        return int(width), int(height)

    def on_mouse_motion(self, x, y, *args):
        return x, self.__get_true_y_position(y), *args

    def on_mouse_release(self, x, y, button, modifiers):
        return x, self.__get_true_y_position(y), button, modifiers

    @abstractmethod
    def on_draw(self, by_scheduler = False): pass
