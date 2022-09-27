from abc import ABC, abstractmethod
from pyglet import image
from pyglet import gl

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

    @abstractmethod
    def draw(self): pass
