from .screen import Screen
from .util.button import Button
from .util.confirmation_box import ConfirmationBox
from .util.slide import Slide
from .util.message_box import MessageBox
from pyglet import graphics
from pyglet.window import mouse, key

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
        confirmation_box_batch = graphics.Batch()

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

        # Obtém o tamanho e posição dos botões maiores, que serão dispostos verticalmente.
        large_button_width = int(sidebar_width * 0.60)
        large_button_height = int(large_button_width * 0.39)
        large_button_spacing = large_button_height * 0.2
        
        large_button_x = int(sidebar_width * 0.5 - large_button_width * 0.5)
        first_large_button_y = int(self.height * 0.35)

        # Obtém o tamanho e posição dos botões menores, que serão dispostos horizontalmente.
        small_button_width = (large_button_width * 0.8) // 3
        small_button_height = int(small_button_width * 0.75)
        small_button_spacing = large_button_width * 0.1

        first_small_button_x = large_button_x
        small_button_y = int(sidebar_height * 0.9 - small_button_height)

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
        play_button_1_filename = application.paths.get_image("home", "buttons", "play_local.png")
        activated_play_button_1_filename = application.paths.get_image("home", "buttons", "activated_play_local.png")
        
        play_button_2_filename = application.paths.get_image("home", "buttons", "play_as_host.png")
        activated_play_button_2_filename = application.paths.get_image("home", "buttons", "activated_play_as_host.png")
        
        play_button_3_filename = application.paths.get_image("home", "buttons", "play_as_client.png")
        activated_play_button_3_filename = application.paths.get_image("home", "buttons", "activated_play_as_client.png")

        # Carrega a imagem dos botões de histórico, conquistas e configurações.
        history_button_filename = application.paths.get_image("home", "buttons", "history.png")
        activated_history_button_filename = application.paths.get_image("home", "buttons", "activated_history.png")

        achivements_button_filename = application.paths.get_image("home", "buttons", "achivements.png")
        activated_achivements_button_filename = application.paths.get_image("home", "buttons", "activated_achivements.png")

        settings_button_filename = application.paths.get_image("home", "buttons", "settings.png")
        activated_settings_button_filename = application.paths.get_image("home", "buttons", "activated_settings.png")

        # Cria os botões de jogar.
        play_button_1 = Button(
            self, batch, large_button_x,
            first_large_button_y + (large_button_height + large_button_spacing) * 0,
            (large_button_width, large_button_height),
            (play_button_1_filename, activated_play_button_1_filename)
        )

        play_button_2 = Button(
            self, batch, large_button_x,
            first_large_button_y + (large_button_height + large_button_spacing) * 1,
            (large_button_width, large_button_height),
            (play_button_2_filename, activated_play_button_2_filename)
        )

        play_button_3 = Button(
            self, batch, large_button_x,
            first_large_button_y + (large_button_height + large_button_spacing) * 2,
            (large_button_width, large_button_height),
            (play_button_3_filename, activated_play_button_3_filename)
        )

        # Cria os botões de histórico, conquistas e configurações.
        history_button = Button(
            self, batch, first_small_button_x + (small_button_width + small_button_spacing) * 0,
            small_button_y, (small_button_width, small_button_height),
            (history_button_filename, activated_history_button_filename)
        )

        achivements_button = Button(
            self, batch, first_small_button_x + (small_button_width + small_button_spacing) * 1,
            small_button_y, (small_button_width, small_button_height),
            (achivements_button_filename, activated_achivements_button_filename)
        )

        settings_button = Button(
            self, batch, first_small_button_x + (small_button_width + small_button_spacing) * 2,
            small_button_y, (small_button_width, small_button_height),
            (settings_button_filename, activated_settings_button_filename)
        )

        # Carrega a imagem de background.
        background_filenames = application.paths.get_image_list("home", "background", shuffle = True)
        
        background = Slide(
            self, batch, background_x, background_y,
            (background_width, background_height),
            background_filenames
        )

        # Cria uma caixa de mensagens e uma caixa de confirmação.
        message_box_filename = application.paths.get_image("general", "message_box.png")

        cancel_button_filename = application.paths.get_image("general", "buttons", "cancel.png")
        activated_cancel_button_filename = application.paths.get_image("general", "buttons", "activated_cancel.png")
        
        confirm_button_filename = application.paths.get_image("general", "buttons", "confirm.png")
        activated_confirm_button_filename = application.paths.get_image("general", "buttons", "activated_confirm.png")

        message_box = MessageBox(
            self, message_box_batch, message_box_x, message_box_y,
            (message_box_width, message_box_height), message_box_filename
        )

        confirmation_box = ConfirmationBox(
            self, confirmation_box_batch, message_box_x, message_box_y,
            (message_box_width, message_box_height), message_box_filename,
            button_images = (
                (cancel_button_filename, activated_cancel_button_filename),
                (confirm_button_filename, activated_confirm_button_filename)
            )
        )

        # Instancia as imagens desenhadas no batch (para o garbage collector não apagá-las antes de desenhar)
        # e a posição do background, que será necessária para desenhar posteriormente.
        self.__sidebar_image = sidebar_image
        self.__background = background
        
        self.__logo_sprite = logo_sprite
        self.__message_box = message_box
        self.__confirmation_box = confirmation_box
        
        self.__play_button_1 = play_button_1
        self.__play_button_2 = play_button_2
        self.__play_button_3 = play_button_3

        self.__history_button = history_button
        self.__achivements_button = achivements_button
        self.__settings_button = settings_button
        
        self.__batch = batch

    def __check_buttons(self, x, y):
        # A princípio pode parecer exagerado definir múltiplas condicionais,
        # ao invés de simplesmente retornar em uma única linha o retorno de cada função,
        # no entanto, cada verificação abaixo, repetidas várias vezes, acaba sendo muito
        # custoso. Só é necessário verificar uma vez. Dessa forma, o programa fica mais
        # otimizado e a animação da tela, consequentemente, fica mais fluída.
        if self.__play_button_1.check(x, y): return True, False, False, False, False, False
        elif self.__play_button_2.check(x, y): return False, True, False, False, False, False
        elif self.__play_button_3.check(x, y): return False, False, True, False, False, False
        elif self.__history_button.check(x, y): return False, False, False, True, False, False
        elif self.__achivements_button.check(x, y): return False, False, False, False, True, False
        elif self.__settings_button.check(x, y): return False, False, False, False, False, True
        return False, False, False, False, False, False

    def __set_dialog_box_message(self, widget, *message):
        widget.set_message(
            self.width // 2, self.height // 2,
            *message, font_size = int(self.width * 0.012),
            line_spacing = int(self.width * 0.025)
        )

    def set_message(self, *message):
        self.__set_dialog_box_message(self.__message_box, *message)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            message = self.__message_box.has_message()
            message = message or self.__confirmation_box.has_message()
            
            if not message:
                self.__set_dialog_box_message(self.__confirmation_box, "Você realmente deseja sair?")
        return True

    def on_mouse_motion(self, *args):
        x, y = super().on_mouse_motion(*args)[0: 2]
        self.__check_buttons(x, y)

        if self.__confirmation_box.has_message():
            self.__confirmation_box.check(x, y)

    def on_mouse_release(self, *args):
        x, y, mouse_button = super().on_mouse_release(*args)[0: 3]
        if mouse_button != mouse.LEFT: return
            
        play_button_1, play_button_2, play_button_3, history, achivements, settings = self.__check_buttons(x, y)

        # Qualquer ação será realizada somente se não houver mensagens sendo mostrada na tela.
        if self.__message_box.has_message():
            return self.__message_box.delete_message()

        if self.__confirmation_box.has_message():
            cancel, confirm = self.__confirmation_box.check(x, y)

            if confirm: self.get_application().close()
            elif cancel: self.__confirmation_box.delete_message()
            return

        # Verifica se algum botão de jogar foi apertado.
        if play_button_1: self.__on_play(1)
        elif play_button_2: self.__on_play(2)
        elif play_button_3: self.__on_play(3)
         
    def on_draw(self, by_scheduler = False):
        if by_scheduler: self.__background.next()
        self.__sidebar_image.blit(0, 0)
        self.__batch.draw()

        self.__confirmation_box.draw()
        self.__message_box.draw()
