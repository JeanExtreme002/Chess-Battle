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
        background_x, background_y = self.get_pixels_by_percent(30, 0)
        background_width = self.width - background_x
        background_height = self.height

        # Obtém o tamanho da barra lateral.
        sidebar_width = background_x - 2
        sidebar_height = self.height

        # Obtém tamanho e posição da logo.
        logo_width = int(sidebar_width * 0.70)
        logo_height = int(logo_width * 0.65)
        
        logo_x = int(sidebar_width * 0.5 - logo_width * 0.5)
        logo_y = int(self.height * 0.25)

        # Obtém o tamanho e posição dos botões de jogar.
        play_button_width = int(sidebar_width * 0.60)
        play_button_height = int(play_button_width * 0.75)
        
        play_button_x = int(sidebar_width * 0.5 - play_button_width * 0.5)
        play_button_spacing = play_button_height * 0.2
        first_play_button_y = int(self.height * 0.45)

        # Carrega a imagem da barra lateral.
        sidebar_filename = application.paths.get_image("home", "sidebar.png")
        sidebar_image = self.load_image(sidebar_filename, (sidebar_width, sidebar_height))
    
        # Carrega a imagem de logo.
        logo_filename = application.paths.get_image("home", "logo.png")
        logo_image = self.load_image(logo_filename, (logo_width, logo_height))
        logo_sprite = self.create_sprite(logo_image, batch = batch, x = logo_x, y = logo_y)

        # Carrega a imagem dos botões de jogar.
        button_1_filename = application.paths.get_image("home", "buttons", "play_local.png")
        button_1_image = self.load_image(button_1_filename, (play_button_width, play_button_height))
        
        button_2_filename = application.paths.get_image("home", "buttons", "play_as_host.png")
        button_2_image = self.load_image(button_2_filename, (play_button_width, play_button_height))

        button_3_filename = application.paths.get_image("home", "buttons", "play_as_client.png")
        button_3_image = self.load_image(button_3_filename, (play_button_width, play_button_height))

        button_1_sprite = self.create_sprite(
            button_1_image, batch = batch,
            x = play_button_x, y = first_play_button_y
        )
        
        button_2_sprite = self.create_sprite(
            button_2_image, batch = batch,
            x = play_button_x, y = first_play_button_y + (play_button_height * 0.5 + play_button_spacing) * 1
        )
        
        button_3_sprite = self.create_sprite(
            button_3_image, batch = batch,
            x = play_button_x, y = first_play_button_y + (play_button_height * 0.5 + play_button_spacing) * 2
        )

        # Carrega a imagem de background.
        background_filename = application.paths.get_random_image("home", "background")
        background_image = self.load_image(background_filename, (background_width, background_height))

        # Aplica todos os desenhos na tela.
        background_image.blit(background_x, background_y)
        sidebar_image.blit(0, 0)
        batch.draw()
