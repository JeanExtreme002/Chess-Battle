from .screen import Screen
from .util.confirmation_box import ConfirmationBox
from pyglet import graphics
from pyglet.window import mouse, key

class BoardScreen(Screen):
    
    __LOCAL_MODE = 0
    __ONLINE_MODE = 1

    __WHITE_COLOR = (255, 255, 255)
    __BLACK_COLOR = (0, 0, 0)
    
    def __init__(self, application):
        super().__init__(application)

        self.__mode = self.LOCAL_MODE
        self.__game = None
        
        self.sound_player.stop_sound()
        self.__build()
        
    def __build(self):
        application = self.get_application()
        
        self.__batch = graphics.Batch()
        confirmation_box_batch = graphics.Batch()
        
        self.__square_shapes = []

        # Obtém o tamanho do tabuleiro, que deve ser divisível por 8.
        board_size = int(self.get_pixels_by_percent(0, 90)[1])

        while board_size % 8 != 0:
            board_size -= 1
        
        square_size = board_size / 8

        # Obtém a posição do tabuleiro.
        board_y = (self.height - board_size) // 2
        board_x = board_y

        # Obtém o tamanho e a posição do placar e seus elementos.
        score_board_area_x = board_size + board_x
        score_board_area_width = (self.width - score_board_area_x)
        
        score_board_height = self.height - (board_y * 2)
        score_board_width = score_board_height * 0.7
        score_board_x = score_board_area_x + score_board_area_width // 2 - score_board_width // 2
        score_board_y = board_y

        # Obtém o tamanho e a posição da caixa de mensagem.
        message_box_width = self.width * 0.45
        message_box_height = message_box_width * 0.7
        message_box_x = int(self.width / 2 - message_box_width / 2)
        message_box_y = int(self.height / 2 - message_box_height / 2)

        # Cria o plano de fundo.
        background_filename = application.paths.get_image("board", "background.png")
        self.__background_image = self.load_image(background_filename, (self.width, self.height))

        # Cria a imagem do placar.
        score_board_filename = application.paths.get_image("board", "score_board.png")
        score_board_image = self.load_image(score_board_filename, (score_board_width, score_board_height))

        self.__score_board_sprite = self.create_sprite(
            score_board_image, batch = self.__batch,
            x = score_board_x, y = score_board_y
        )  

        # Cria a borda do tabuleiro.
        self.__board_border = self.create_rectangle(
            board_x - 2, board_y - 2, board_size + 4, board_size + 4,
            batch = self.__batch, color = (0, 0, 0)
        )

        # Cria os quadrados do tabuleiro.
        for row in range(8):
            for column in range(8):
                x = board_x + square_size * column
                y = board_y + square_size * row

                if (column + row) % 2 == 0:
                    color = self.__WHITE_COLOR
                else: color = self.__BLACK_COLOR

                square = self.create_rectangle(
                    x, y, square_size, square_size,
                    batch = self.__batch, color = color
                )
                self.__square_shapes.append(square)
                
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

        # Instancia a posição e tamanho do tabuleiro, para serem utilizados posteriormente.
        self.__board_pos = board_x, (board_y)
        self.__board_size = board_size
        self.__square_size = square_size

    def __check_mouse_on_board(self, x, y):
        if not self.__is_mouse_on_board(x, y): return
        
        step = self.__square_size
        
        for index_x in range(8):
            for index_y in range(8):
                pos_x = self.__board_pos[0] + self.__square_size * index_x
                pos_y = self.__board_pos[1] + self.__square_size * index_y

                if pos_x <= x <= pos_x + step and pos_y <= y <= pos_y + step:
                    return index_y, index_x

    def __is_mouse_on_board(self, x, y):
        on_x = self.__board_pos[0] <= x <= self.__board_pos[0] + self.__board_size
        on_y = self.__board_pos[1] <= y <= self.__board_pos[1] + self.__board_size
        return on_x and on_y

    def __set_dialog_box_message(self, widget, *message):
        widget.set_message(
            self.width // 2, self.height // 2,
            *message, font_size = int(self.width * 0.012),
            line_spacing = int(self.width * 0.025)
        )
        
    @property
    def LOCAL_MODE(self):
        return self.__LOCAL_MODE

    @property
    def ONLINE_MODE(self):
        return self.__ONLINE_MODE

    def set_game(self, game, mode, input_func = None, output_func = None):
        self.__game = game
        self.__mode = mode
        self.__player_input = input_func
        self.__player_output = output_func

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            if not self.__confirmation_box.has_message():
                self.__set_dialog_box_message(self.__confirmation_box, "Realmente deseja abandonar o jogo?")     
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

        coords = self.__check_mouse_on_board(x, y)

    def on_draw(self, by_scheduler = False):
        self.__background_image.blit(0, 0)
        self.__batch.draw()
        self.__confirmation_box.draw()
