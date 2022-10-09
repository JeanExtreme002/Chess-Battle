from .screen import Screen
from .util.button import Button
from .util.slide import Slide
from .util.message_box import MessageBox
from pyglet import graphics
from pyglet.window import mouse

class HomeScreen(Screen):
    def __init__(self, application, on_play):
        super().__init__(application)
        self.__on_play = on_play
        self.__message = None
        self.__build()

    def __build(self):
        application = self.get_application()
        batch = graphics.Batch()
        
        message_box_batch = graphics.Batch()

        # Obtém tamanho e posição da imagem background.
        background_x, background_y = self.get_pixels_by_percent(30, 0)
        background_width = self.width - background_x
        background_height = self.height

        # Obtém o tamanho da barra lateral.
        sidebar_width = background_x - 2
        sidebar_height = self.height

        # Obtém tamanho e posição da logo.
        logo_width = int(sidebar_width * 0.70)
        logo_height = int(logo_width * 0.77)
        
        logo_x = int(sidebar_width * 0.5 - logo_width * 0.5)
        logo_y = int(self.height * 0.02)

        # Obtém o tamanho e posição dos botões de jogar.
        play_button_width = int(sidebar_width * 0.60)
        play_button_height = int(play_button_width * 0.39)
        
        play_button_x = int(sidebar_width * 0.5 - play_button_width * 0.5)
        play_button_spacing = play_button_height * 0.2
        first_play_button_y = int(self.height * 0.35)

        # Obtém o tamanho e posição do botão de configuração.
        settings_button_width = int(sidebar_width * 0.18)
        settings_button_height = int(settings_button_width * 0.75)

        settings_button_x = int(sidebar_width - (sidebar_width - play_button_width) / 2 - settings_button_width)
        settings_button_y = int(sidebar_height * 0.9 - settings_button_height)

        # Obtém o tamanho e a posição da caixa de mensagem.
        message_box_width = self.width * 0.45
        message_box_height = message_box_width * 0.7
        message_box_x = int(self.width / 2 - message_box_width / 2)
        message_box_y = int(self.height / 2 - message_box_height / 2)
        
        # Carrega a imagem da barra lateral.
        sidebar_filename = application.paths.get_image("home", "sidebar.png")
        sidebar_image = self.load_image(sidebar_filename, (sidebar_width, sidebar_height))
    
        # Carrega a imagem de logo.
        logo_filename = application.paths.get_image("home", "logo.png")
        logo_image = self.load_image(logo_filename, (logo_width, logo_height))
        logo_sprite = self.create_sprite(logo_image, batch = batch, x = logo_x, y = logo_y)

        # Carrega a imagem dos botões de jogar.
        button_1_filename = application.paths.get_image("home", "buttons", "play_local.png")
        activated_button_1_filename = application.paths.get_image("home", "buttons", "activated_play_local.png")
        
        button_2_filename = application.paths.get_image("home", "buttons", "play_as_host.png")
        activated_button_2_filename = application.paths.get_image("home", "buttons", "activated_play_as_host.png")
        
        button_3_filename = application.paths.get_image("home", "buttons", "play_as_client.png")
        activated_button_3_filename = application.paths.get_image("home", "buttons", "activated_play_as_client.png")

        settings_button_filename = application.paths.get_image("home", "buttons", "settings.png")
        activated_settings_button_filename = application.paths.get_image("home", "buttons", "activated_settings.png")

        button_1 = Button(
            self, batch, play_button_x,
            first_play_button_y,
            (play_button_width, play_button_height),
            (button_1_filename, activated_button_1_filename)
        )

        button_2 = Button(
            self, batch, play_button_x,
            first_play_button_y + (play_button_height + play_button_spacing) * 1,
            (play_button_width, play_button_height),
            (button_2_filename, activated_button_2_filename)
        )

        button_3 = Button(
            self, batch, play_button_x,
            first_play_button_y + (play_button_height + play_button_spacing) * 2,
            (play_button_width, play_button_height),
            (button_3_filename, activated_button_3_filename)
        )

        settings_button = Button(
            self, batch, settings_button_x, settings_button_y,
            (settings_button_width, settings_button_height),
            (settings_button_filename, activated_settings_button_filename)
        )

        # Carrega a imagem de background.
        background_filenames = application.paths.get_image_list("home", "background", shuffle = True)
        
        background = Slide(
            self, batch, background_x, background_y,
            (background_width, background_height),
            background_filenames
        )

        # Cria uma caixa de mensagens para inserir futuras mensagens.
        message_box_filename = application.paths.get_image("home", "message_box.png")

        message_box = MessageBox(
            self, message_box_batch, message_box_x, message_box_y,
            (message_box_width, message_box_height), message_box_filename
        )

        # Instancia as imagens desenhadas no batch (para o garbage collector não apagá-las antes de desenhar)
        # e a posição do background, que será necessária para desenhar posteriormente.
        self.__sidebar_image = sidebar_image
        self.__background = background
        
        self.__logo_sprite = logo_sprite
        self.__message_box = message_box
        
        self.__button_1 = button_1
        self.__button_2 = button_2
        self.__button_3 = button_3
        self.__settings_button = settings_button
        
        self.__batch = batch

    def __check_buttons(self, x, y):
        if self.__button_1.check(x, y): return True, False, False, False
        elif self.__button_2.check(x, y): return False, True, False, False
        elif self.__button_3.check(x, y): return False, False, True, False
        elif self.__settings_button.check(x, y): return False, False, False, True
        return False, False, False, False

    def set_message(self, *message):
        self.__message_box.set_message(
            self.width // 2, self.height // 2,
            *message, font_size = int(self.width * 0.012),
            line_spacing = int(self.width * 0.025)
        )

    def on_mouse_motion(self, *args):
        x, y = super().on_mouse_motion(*args)[0: 2]
        self.__check_buttons(x, y)

    def on_mouse_release(self, *args):
        x, y, mouse_button = super().on_mouse_release(*args)[0: 3]
        if mouse_button != mouse.LEFT: return
            
        button_1, button_2, button_3 = self.__check_buttons(x, y)

        if self.__message_box.has_message():
            return self.__message_box.delete_message()
        
        if button_1: self.__on_play(1)
        elif button_2: self.__on_play(2)
        elif button_3: self.__on_play(3)
         
    def on_draw(self, by_scheduler = False):
        if by_scheduler: self.__background.next()
        self.__sidebar_image.blit(0, 0)
        self.__batch.draw()
        self.__message_box.draw()
