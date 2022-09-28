from .screen import Screen
from pyglet import graphics

class HomeScreen(Screen):
    def __init__(self, application, on_play):
        super().__init__(application)
        self.__on_play = on_play
         
    def draw(self):
        application = self.get_application()
        batch = graphics.Batch()

        # Obtém tamanho e posição da imagem background.
        background_x, background_y = self.get_pixels_by_percent(25, 0)
        background_width = self.width - background_x
        background_height = self.height

        # Obtém tamanho da logo.
        logo_width = self.get_pixels_by_percent(20, 0)[0]
        logo_height = logo_width // 1.5

        # Carrega a imagem da barra lateral.
        sidebar_filename = application.paths.get_image("home", "sidebar.png")
        sidebar_image = self.load_image(sidebar_filename, (background_x - 2, self.height))
    
        # Carrega a imagem de logo.
        logo_filename = application.paths.get_image("home", "logo.png")
        logo_image = self.load_image(logo_filename, (logo_width, logo_height))
        
        logo_sprite = self.create_sprite(
            logo_image, batch = batch,
            x = int(background_x / 2 - logo_width / 2),
            y = self.get_pixels_by_percent(0, 7)[1] + logo_width // 2
        )

        # Carrega a imagem de background.
        background_filename = application.paths.get_random_image("home", "background")
        background_image = self.load_image(background_filename, (background_width, background_height))

        # Aplica todos os desenhos na tela.
        sidebar_image.blit(0, 0)
        background_image.blit(background_x, background_y)
        batch.draw()
