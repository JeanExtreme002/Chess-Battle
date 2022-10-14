from .screen import Screen
from .util.button import Button
from .util.confirmation_box import ConfirmationBox
from pyglet import graphics
from pyglet.window import mouse, key

class SettingsScreen(Screen):

    __resolutions = [
        (640, 360),
        (960, 540),
        (1280, 720),
        (1366, 768)
    ]
    
    def __init__(self, application):
        super().__init__(application)
        
        self.__build()
        self.__load_current_settings()
        
    def __build(self):
        application = self.get_application()
        
        self.__batch = graphics.Batch()
        self.__text_batch = graphics.Batch()
        confirmation_box_batch = graphics.Batch()

        # Obtém o tamanho e a posição dos labels.
        label_width = self.width * 0.25
        label_height = label_width * 0.41
        label_x = self.width / 2 - label_width / 2
        first_label_y = self.height * 0.1

        # Obtém o tamanho e a posição do botão de aplicar alterações.
        button_width = self.width * 0.2
        button_height = button_width * 0.39
        button_x = self.width / 2 - button_width / 2
        button_y = self.height * 0.8 - label_height
        
        # Obtém o tamanho e a posição da caixa de mensagem.
        message_box_width = self.width * 0.45
        message_box_height = message_box_width * 0.7
        message_box_x = self.width / 2 - message_box_width / 2
        message_box_y = self.height / 2 - message_box_height / 2

        # Cria o plano de fundo.
        background_filename = application.paths.get_image("settings", "background.png")
        self.__background_image = self.load_image(background_filename, (self.width, self.height))

        # Cria as imagens de label.
        label_filename = application.paths.get_image("settings", "label.png")
        activated_label_filename = application.paths.get_image("settings", "activated_label.png")

        self.__labels = []

        for index in range(2):
            label = Button(
                self, self.__batch, label_x, first_label_y + (label_height + label_height * 0.1) * index,
                (label_width, label_height), (label_filename, activated_label_filename)
            )
            
            text = self.create_text(
                str(), label_x + label_width / 2,
                first_label_y + label_height / 1.7 + (label_height + label_height * 0.1) * index,
                color = (255, 255, 255, 255), font_size = int(self.width * 0.017), anchor_x = "center", anchor_y = "center",
                batch = self.__text_batch
            )
            self.__labels.append((label, text))

        # Cria botão para aplicar as configurações
        button_filename = application.paths.get_image("settings", "apply_button.png")
        activated_button_filename = application.paths.get_image("settings", "activated_apply_button.png")
        
        self.__apply_button = Button(
            self, self.__batch, button_x, button_y,
            (button_width, button_height),
            (button_filename, activated_button_filename)
        )
                
        # Cria uma caixa de mensagens e uma caixa de confirmação.
        message_box_filename = application.paths.get_image("general", "message_box.png")

        cancel_button_filename = application.paths.get_image("general", "buttons", "cancel.png")
        activated_cancel_button_filename = application.paths.get_image("general", "buttons", "activated_cancel.png")
        
        confirm_button_filename = application.paths.get_image("general", "buttons", "confirm.png")
        activated_confirm_button_filename = application.paths.get_image("general", "buttons", "activated_confirm.png")

        self.__confirmation_box = ConfirmationBox(
            self, confirmation_box_batch, message_box_x, message_box_y,
            (message_box_width, message_box_height), message_box_filename,
            button_images = (
                (cancel_button_filename, activated_cancel_button_filename),
                (confirm_button_filename, activated_confirm_button_filename)
            )
        )

    def __load_current_settings(self):
        application = self.get_application()
        
        try:
            current_resolution = (application.width, application.height)
            self.__resolution_index = self.__resolutions.index(current_resolution)
        except IndexError:
            self.__resolution_index = len(self.__resolutions) // 2

        self.__volume = self.sound_player.get_volume()
        self.__changed = False
        self.__update_label_texts()

    def __set_dialog_box_message(self, widget, *message):
        widget.set_message(
            self.width // 2, self.height // 2,
            *message, font_size = int(self.width * 0.012),
            line_spacing = int(self.width * 0.025)
        )

    def __update_label_texts(self):
        self.__labels[0][1].text = "{}x{}".format(*self.__resolutions[self.__resolution_index])
        self.__labels[1][1].text = "Volume: {}%".format(int(self.__volume))

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            if not self.__changed:
                self.get_application().go_back()
            elif not self.__confirmation_box.has_message():
                self.__set_dialog_box_message(self.__confirmation_box, "Deseja sair sem salvar as alterações?")     
        return True

    def on_mouse_motion(self, *args):
        x, y = super().on_mouse_motion(*args)[0: 2]
        
        if self.__confirmation_box.has_message():
            self.__confirmation_box.check(x, y)

        self.__apply_button.check(x, y)

        for label, text in self.__labels:
            if label.check(x, y):
                text.color = (230, 230, 230, 255)
            else:
                text.color = (255, 255, 255, 255)

    def on_mouse_release(self, *args):
        x, y, mouse_button = super().on_mouse_release(*args)[0: 3]
        if mouse_button != mouse.LEFT: return

        # Qualquer ação será realizada somente se não houver mensagens sendo mostrada na tela.
        if self.__confirmation_box.has_message():
            cancel, confirm = self.__confirmation_box.check(x, y)

            if not (confirm or cancel): return
            self.__confirmation_box.delete_message()
            
            if confirm:
                self.__load_current_settings()
                self.get_application().go_back()

        if self.__labels[0][0].check(x, y):
            self.__resolution_index += 1
            self.__resolution_index %= len(self.__resolutions)
            self.__changed = True
            self.__update_label_texts()
            
        elif self.__labels[1][0].check(x, y):
            self.__volume += 10
            self.__volume %= 110
            self.__changed = True
            self.__update_label_texts()

        elif self.__apply_button.check(x, y):
            self.sound_player.set_volume(self.__volume)
            self.__changed = False
            self.get_application().resize(*self.__resolutions[self.__resolution_index])
            self.get_application().go_back()

    def on_draw(self, by_scheduler = False):
        self.__background_image.blit(0, 0)
        self.__batch.draw()
        self.__text_batch.draw()
        self.__confirmation_box.draw()
