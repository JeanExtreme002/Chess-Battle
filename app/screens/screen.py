from .util import Achievement
from abc import ABC, abstractmethod
from pyglet import image
from pyglet import gl
from pyglet import graphics
from pyglet import shapes
from pyglet import sprite
from pyglet import text

# Configuração para habilitar o redimensionamento de imagens.
gl.glEnable(gl.GL_TEXTURE_2D)
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)


class Screen(ABC):
    """
    Classe abstrata para criar telas.
    """

    _images = dict()
    _achievement_widget = None
    
    def __init__(self, application):
        self.__application = application
        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar a tela.
        """
        application = self.get_application()
        achievement_filename = application.paths.get_image("general", "trophy.png")
        
        Screen._achievement_widget = Achievement(
            self, (application.width * 0.4, application.height * 0.13),
            image = achievement_filename, font_size = application.height * 0.15 * 0.2
        )
        
    @property
    def width(self):
        return self.__application.width

    @property
    def height(self):
        return self.__application.height

    @property
    def sound_player(self):
        return self.__application.get_sound_player()

    def create_batch(self, *args, **kwargs):
        """
        Cria um batch.
        """
        return graphics.Batch(*args, **kwargs)

    def create_rectangle(self, x, y, width, height, **kwargs):
        """
        Cria um retângulo, com a posição Y invertida.
        """
        y = self.get_true_y_position(y)
        height *= -1

        shape = shapes.Rectangle(
            x = x, y = y,
            width = width,
            height = height,
            **kwargs
        )
        return shape

    def create_sprite(self, img, x, y, **kwargs):
        """
        Cria uma imagem, com a posição Y invertida.
        """
        y = self.get_true_y_position(y, img.height)
        return sprite.Sprite(img, x = x, y = y, **kwargs)

    def create_text(self, string, x, y, **kwargs):
        """
        Cria um texto, com a posição Y invertida.
        """
        y = self.get_true_y_position(y)
        return text.Label(string, x = x, y = y, **kwargs)

    def free_memory(self, save_original = True):
        """
        Método para apagar todas as imagens utilizadas pela tela.
        """
        found_image_filenames = []

        # Busca por imagens que não estão sendo utilizadas por outras telas,
        # para que sejam posteriormente removidas do dicionário.
        for filename, resolutions in Screen._images.items():
            if self in resolutions["original"]["users"]:
                resolutions["original"]["users"].remove(self)

            if len(resolutions["original"]["users"]) == 0:
                found_image_filenames.append([filename, list(resolutions.keys())])

        # Percorre a lista de imagens encontradas para remoção, apagando-as do dicionário.
        for filename, resolutions in found_image_filenames:

            # Apaga todo o dicionário referente ao arquivo de imagem,
            # caso o usuário não deseje salvar a imagem original.
            if not save_original:
                Screen._images.pop(filename)
                continue

            # Remove todas as diferentes resoluções de imagem derivadas da imagem original.
            for size in resolutions:
                if size != "original": Screen._images[filename].pop(size)

    def get_application(self):
        """
        Retorna o objeto Application.
        """
        return self.__application

    def get_true_y_position(self, y, height = 0):
        """
        Calcula a posição Y invertida.
        """
        return self.height - y - height

    def load_image(self, filename, size = "original"):
        """
        Carrega uma imagem.
        """
        # Obtém a imagem original, sem modificações, se ela não tiver sido salva.
        if not filename in Screen._images:
            Screen._images[filename] = dict()
            Screen._images[filename]["original"] = dict()
            Screen._images[filename]["original"]["image"] = image.load(filename)
            Screen._images[filename]["original"]["users"] = set()
        
        # Caso a imagem na resolução solicitada não tenha sido salva, uma cópia
        # da imagem original será criada, redimensionando a mesma.
        if not size in Screen._images[filename]:
            img = Screen._images[filename]["original"]["image"]
            img = img.get_region(0, 0, img.width, img.height)

            img = img.get_texture()
            img.width = size[0]
            img.height = size[1]
            
            Screen._images[filename][size] = dict()
            Screen._images[filename][size]["image"] = img

        Screen._images[filename]["original"]["users"].add(self)

        # Retorna a imagem com a resolução deseja.
        return Screen._images[filename][size]["image"]

    def on_draw(self, by_scheduler = False):
        """
        Evento para desenhar a tela.
        """
        if by_scheduler: Screen._achievement_widget.next()
        
        self.on_draw_screen(by_scheduler)
        Screen._achievement_widget.draw()

    @abstractmethod
    def on_draw_screen(self, by_scheduler = False):
        """
        Método chamado pelo evento on_draw para desenhar a tela.
        """
        pass

    def on_key_press(self, symbol, modifiers):
        """
        Evento de tecla pressionada.
        """
        return True

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        """
        Evento de botão do mouse pressionado.
        """
        return x, self.get_true_y_position(y), button, modifiers

    def on_mouse_motion(self, x, y, *args):
        """
        Evento de movimentação do cursor.
        """
        return x, self.get_true_y_position(y), *args

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Evento de botão do mouse liberado.
        """
        return x, self.get_true_y_position(y), button, modifiers

    def set_achievement(self, title):
        """
        Mostra uma conquista obtida na tela.
        """
        Screen._achievement_widget.set_achievement(title)
