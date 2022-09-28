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
        logo_width = self.get_pixels_by_percent(10, 0)[0]
        logo_height = logo_width

        # Desenha background da barra lateral.
        shape = self.create_rectangle(0, 0, background_x - 2, self.height, color = (30, 30, 80), batch = batch)
    
        # Carrega a imagem de logo e desenha.
        logo_filename = application.paths.get_image("home_logo.png")
        logo_image = self.load_image(logo_filename, (logo_width, logo_height))
        
        logo_sprite = self.create_sprite(
            logo_image, batch = batch,
            x = int(background_x / 2 - logo_width / 2),
            y = self.get_pixels_by_percent(0, 10)[1] + logo_width / 2
        )

        # Carrega a imagem de background.
        background_filename = application.paths.get_random_image("background")
        background_image = self.load_image(background_filename, (background_width, background_height))

        # Aplica todos os desenhos na tela.
        background_image.blit(background_x, background_y)
        batch.draw()
