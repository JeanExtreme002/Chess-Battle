from .screen import Screen
from .util.confirmation_box import ConfirmationBox
from pyglet import graphics
from pyglet.window import mouse, key

class SettingsScreen(Screen):
    
    def __init__(self, application):
        super().__init__(application)
        self.__build()
        
    def __build(self):
        application = self.get_application()
        
        self.__batch = graphics.Batch()
        confirmation_box_batch = graphics.Batch()

        # Obtém o tamanho e a posição dos labels.
        label_width = self.width * 0.35
        label_height = label_width * 0.41
        label_x = int(self.width / 2 - label_width / 2)
        first_label_y = self.height * 0.1

        # Obtém o tamanho e a posição da caixa de mensagem.
        message_box_width = self.width * 0.45
        message_box_height = message_box_width * 0.7
        message_box_x = int(self.width / 2 - message_box_width / 2)
        message_box_y = int(self.height / 2 - message_box_height / 2)

        # Cria o plano de fundo.
        background_filename = application.paths.get_image("settings", "background.png")
        self.__background_image = self.load_image(background_filename, (self.width, self.height))

        # Cria a imagens de label.
        label_filename = application.paths.get_image("settings", "label.png")
        label_image = self.load_image(label_filename, (label_width, label_height))

        self.__labels = []

        for index in range(2):
            label = self.create_sprite(
                label_image, batch = self.__batch,
                x = label_x, y = first_label_y + (label_height + label_height * 0.1) * index
            )
            self.__labels.append(label)
                
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

    def __set_dialog_box_message(self, widget, *message):
        widget.set_message(
            self.width // 2, self.height // 2,
            *message, font_size = int(self.width * 0.012),
            line_spacing = int(self.width * 0.025)
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            if not self.__confirmation_box.has_message():
                self.__set_dialog_box_message(self.__confirmation_box, "Deseja sair sem salvar as alterações?")     
        return True

    def on_mouse_motion(self, *args):
        x, y = super().on_mouse_motion(*args)[0: 2]
        
        if self.__confirmation_box.has_message():
            self.__confirmation_box.check(x, y)

    def on_mouse_release(self, *args):
        x, y, mouse_button = super().on_mouse_release(*args)[0: 3]
        if mouse_button != mouse.LEFT: return

        # Qualquer ação será realizada somente se não houver mensagens sendo mostrada na tela.
        if self.__confirmation_box.has_message():
            cancel, confirm = self.__confirmation_box.check(x, y)

            if not (confirm or cancel): return
            self.__confirmation_box.delete_message()
            
            if confirm: self.get_application().go_back()

    def on_draw(self, by_scheduler = False):
        self.__background_image.blit(0, 0)
        self.__batch.draw()
        self.__confirmation_box.draw()
