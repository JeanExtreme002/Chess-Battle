from .screen import Screen
from .util import Button, ConfirmationPopup, IPAddressEntry, WidgetGroup
from pyglet.window import mouse, key

class SettingsScreen(Screen):
    """
    Classe para criar uma tela de configurações.
    """
    
    __resolutions = [
        (640, 360),
        (960, 540),
        (1280, 720),
        (1366, 768)
    ]
    
    def __init__(self, application):
        super().__init__(application)

        self.__selected_ip_entry = False
        
        self.__build()
        self.__load_current_settings()
        
    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar a tela.
        """
        application = self.get_application()
        
        self.__text_batch = self.create_batch()
        self.__widget_group = WidgetGroup()

        # Obtém o tamanho e a posição dos labels.
        label_width = self.width * 0.25
        label_height = label_width * 0.41
        label_x = self.width / 2 - label_width / 2
        first_label_y = self.height * 0.1

        # Obtém o tamanho e a posição do botão de ativar/desativar sons.
        sound_button_height = label_height * 0.5
        sound_button_width = sound_button_height
        sound_button_x = label_x + label_width * 1.1
        sound_button_y = first_label_y + (label_height + label_height * 0.2) + sound_button_height * 0.5

        # Obtém o tamanho e a posição da caixa de texto de endereço IP.
        ip_entry_width = self.width * 0.23
        ip_entry_height = ip_entry_width * 0.15
        ip_entry_x = self.width / 2 - ip_entry_width / 2
        ip_entry_y = self.height * 0.6 - ip_entry_height

        # Obtém o tamanho e a posição do botão de aplicar alterações.
        apply_button_width = self.width * 0.2
        apply_button_height = apply_button_width * 0.39
        apply_button_x = self.width / 2 - apply_button_width / 2
        apply_button_y = self.height * 0.8 - apply_button_height
        
        # Obtém o tamanho e a posição do popup.
        popup_width = self.width * 0.45
        popup_height = popup_width * 0.7
        popup_x = self.width / 2 - popup_width / 2
        popup_y = self.height / 2 - popup_height / 2

        # Cria o plano de fundo.
        background_filename = application.paths.get_image("settings", "background.png")
        self.__background_image = self.load_image(background_filename, (self.width, self.height))

        # Cria as imagens de label.
        label_filename = application.paths.get_image("settings", "label.png")
        activated_label_filename = application.paths.get_image("settings", "activated_label.png")

        self.__labels = []

        for index in range(2):
            label = Button(
                self, label_x, first_label_y + (label_height + label_height * 0.1) * index,
                (label_width, label_height), (label_filename, activated_label_filename),
                widget_group = self.__widget_group
            )
            
            text = self.create_text(
                str(), label_x + label_width / 2,
                first_label_y + label_height / 1.7 + (label_height + label_height * 0.1) * index,
                color = (255, 255, 255, 255), font_size = int(self.width * 0.017),
                anchor_x = "center", anchor_y = "center", batch = self.__text_batch
            )
            self.__labels.append((label, text))

        # Cria botão para ativar e desativar os sons do jogo.
        self.__mute_button_filename = application.paths.get_image("settings", "buttons", "mute.png")
        self.__activated_mute_button_filename = application.paths.get_image("settings", "buttons", "activated_mute.png")
        self.__dismute_button_filename = application.paths.get_image("settings", "buttons", "dismute.png")
        self.__activated_dismute_button_filename = application.paths.get_image("settings", "buttons", "activated_dismute.png")
        
        self.__sound_button = Button(
            self, sound_button_x, sound_button_y, (sound_button_width, sound_button_height),
            (self.__mute_button_filename, self.__activated_mute_button_filename),
            widget_group = self.__widget_group
        )

        # Cria caixa de texto para inserir um endereço IP.
        self.__ip_entry = IPAddressEntry(
            self, ip_entry_x, ip_entry_y,
            (ip_entry_width, ip_entry_height),
            border = 2, default_text = "Endereço IP",
            widget_group = self.__widget_group
        )

        # Cria botão para aplicar as configurações.
        apply_button_filename = application.paths.get_image("settings", "buttons", "apply.png")
        activated_apply_button_filename = application.paths.get_image("settings", "buttons", "activated_apply.png")
        
        self.__apply_button = Button(
            self, apply_button_x, apply_button_y,
            (apply_button_width, apply_button_height),
            (apply_button_filename, activated_apply_button_filename),
            widget_group = self.__widget_group
        )
                
        # Cria um popup de confirmação.
        popup_filename = application.paths.get_image("general", "popup", "popup.png")

        cancel_button_filename = application.paths.get_image("general", "popup", "buttons", "cancel.png")
        activated_cancel_button_filename = application.paths.get_image("general", "popup", "buttons", "activated_cancel.png")
        
        confirm_button_filename = application.paths.get_image("general", "popup", "buttons", "confirm.png")
        activated_confirm_button_filename = application.paths.get_image("general", "popup", "buttons", "activated_confirm.png")

        self.__confirmation_popup = ConfirmationPopup(
            self, popup_x, popup_y,
            (popup_width, popup_height), popup_filename,
            button_images = (
                (cancel_button_filename, activated_cancel_button_filename),
                (confirm_button_filename, activated_confirm_button_filename)
            )
        )

    def __apply_changes(self):
        """
        Aplica as alterações realizadas.
        """
        self.sound_player.set_volume(self.__volume)
        self.sound_player.set_mute(self.__muted)

        self.get_application().set_ip_address(self.__ip_entry.get_text())
        self.get_application().resize(*self.__resolutions[self.__resolution_index])
        self.get_application().save_settings()
        
        self.__changed = False

        # Conquista de usuário.
        self.get_application().add_achievement("Do jeitinho que eu gosto.", "Alterou as configurações do jogo.")

    def __change_ip_address(self, symbol):
        """
        Altera o endereço IP na caixa de entrada.
        """
        if symbol == key.BACKSPACE:
            self.__ip_entry.delete_char()
            self.__changed = True
                
        elif self.__ip_entry.add_char(chr(symbol)):
            self.__changed = True

    def __change_resolution(self):
        """
        Altera a resolução da tela.
        """
        self.__resolution_index += 1
        self.__resolution_index %= len(self.__resolutions)
        self.__changed = True
        self.__update_labels()

    def __change_sound_status(self):
        """
        Ativa ou desativa o som.
        """
        self.__muted = not self.__muted
        self.__changed = True
        self.__update_labels()

    def __change_sound_volume(self):
        """
        Altera o volume do som.
        """
        self.__volume += 10
        self.__volume %= 110
        self.__changed = True
        self.__update_labels()

    def __load_current_settings(self):
        """
        Carrega as configurações do aplicativo para serem
        usadas e mostradas na tela de configurações.
        """
        application = self.get_application()
        
        try:
            current_resolution = (application.width, application.height)
            self.__resolution_index = self.__resolutions.index(current_resolution)
        except IndexError:
            self.__resolution_index = len(self.__resolutions) // 2

        self.__volume = self.sound_player.get_volume()
        self.__muted = self.sound_player.is_muted()

        self.__ip_entry.clear()

        for char in self.get_application().get_ip_address():
            self.__ip_entry.add_char(char)
        
        self.__changed = False
        self.__update_labels()

    def __set_dialog_box_message(self, widget, *message):
        """
        Define uma mensagem a ser mostrada em
        um widget de caixa de mensagem.
        """
        widget.set_message(
            self.width // 2, self.height // 2,
            *message, font_size = int(self.width * 0.012),
            line_spacing = int(self.width * 0.025)
        )

    def __update_labels(self):
        """
        Método para atulizar os estados das labels e botões na tela.
        """
        self.__labels[0][1].text = "{}x{}".format(*self.__resolutions[self.__resolution_index])
        self.__labels[1][1].text = "Volume: {}%".format(int(self.__volume))

        if self.__muted: images = [self.__dismute_button_filename, self.__activated_dismute_button_filename]
        else: images = [self.__mute_button_filename, self.__activated_mute_button_filename]
        
        self.__sound_button.change_image(images)

    def on_draw_screen(self, by_scheduler = False):
        """
        Evento para desenhar a tela.
        """
        self.__background_image.blit(0, 0)
        self.__widget_group.draw()
        self.__text_batch.draw()
        self.__confirmation_popup.draw()
        
        if by_scheduler: self.__ip_entry.next()

    def on_key_press(self, symbol, modifiers):
        """
        Evento de tecla pressionada.
        """
        # Caso o ESC seja apertado, significa que o usuário deseja sair desta tela.
        if symbol == key.ESCAPE:

            # Se não houver alterado nenhuma configuração, pode sair da tela sem problema.
            if not self.__changed:
                self.get_application().go_back()

            # Se alterou algo, será pedido uma confirmação para sair.
            elif not self.__confirmation_popup.has_message():
                self.__set_dialog_box_message(self.__confirmation_popup, "Deseja sair sem salvar as alterações?")

        # Insere o caractere na caixa de texto do endereço IP, se o mesmo foi selecionado.
        if self.__selected_ip_entry: self.__change_ip_address(symbol)

        return True

    def on_mouse_motion(self, *args):
        """
        Evento de movimentação do cursor.
        """
        x, y = super().on_mouse_motion(*args)[0: 2]

        if self.__confirmation_popup.has_message():
            self.__confirmation_popup.check(x, y)

        self.__apply_button.check(x, y)
        self.__sound_button.check(x, y)
        self.__ip_entry.check(x, y)

        for label, text in self.__labels:
            if label.check(x, y):
                text.color = (230, 230, 230, 255)
            else:
                text.color = (255, 255, 255, 255)

    def on_mouse_release(self, *args):
        """
        Evento de botão do mouse pressionado e liberado.
        """
        x, y, mouse_button = super().on_mouse_release(*args)[0: 3]
        if mouse_button != mouse.LEFT: return

        # Qualquer ação será realizada somente se não houver mensagem sendo mostrada na tela.
        if self.__confirmation_popup.has_message():
            cancel, confirm = self.__confirmation_popup.check(x, y)
            
            if not (confirm or cancel): return
            self.__confirmation_popup.delete_message()

            # Sai da tela, redefinindo as configurações, caso confirmado.
            if confirm:
                self.__load_current_settings()
                self.get_application().go_back()

        self.__selected_ip_entry = self.__ip_entry.check(x, y)
        self.__ip_entry.set_pipe(self.__selected_ip_entry)

        # Verifica se o usuário deseja alterar a resolução.
        if self.__labels[0][0].check(x, y):
            self.__change_resolution()

        # Verifica se o usuário deseja alterar o volume do som.
        elif self.__labels[1][0].check(x, y):
            self.__change_sound_volume()

        # Verifica se o usuário deseja ativar ou desativar o som.
        elif self.__sound_button.check(x, y):
            self.__change_sound_status()

        # Aplica as alterações e sai da tela.
        elif self.__apply_button.check(x, y):
            self.__apply_changes()
            self.get_application().go_back()
