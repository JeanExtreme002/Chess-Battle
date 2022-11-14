from .screen import Screen
from pyglet.window import mouse, key

class HistoryScreen(Screen):
    """
    Classe para criar uma tela de histórico de partidas.
    """
    
    def __init__(self, application):
        super().__init__(application)
        
        self.__replay_function = lambda game_id: None
        self.__game_list = []
        
        self.__index = 0
        self.__build()
        
    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar a tela.
        """
        application = self.get_application()
        
        self.__batch = self.create_batch()
        self.__text_batch = self.create_batch()

        # Obtém o tamanho e a posição do frame de partida.
        frame_width = self.width * 0.5
        frame_height = frame_width * 0.8
        frame_x = self.width / 2 - frame_width / 2
        frame_y = self.height / 2 - frame_height / 2

        # Obtém o tamanho e a posição da imagem do tabuleiro.
        self.__board_size = frame_height * 0.4
        self.__board_x = int(frame_x + frame_width * 0.87 - self.__board_size)
        self.__board_y = int(frame_y + frame_height * 0.85 - self.__board_size)

        # Obtém o tamanho e a posição das peças.
        piece_size = frame_height * 0.1
        piece_x = frame_x + frame_width * 0.13
        piece_y = self.__board_y + self.__board_size - piece_size

        # Obtém a posição do texto de resultado.
        result_x = piece_x + (self.__board_x - piece_x) / 2
        result_y = self.__board_y

        # Cria o plano de fundo.
        background_filename = application.paths.get_image("history", "background.png")
        self.__background_image = self.load_image(background_filename, (self.width, self.height))

        # Cria o frame de partida.
        frame_filename = application.paths.get_image("history", "frame.png")
        frame_image = self.load_image(frame_filename, (frame_width, frame_height))
        self.__frame = self.create_sprite(frame_image, frame_x, frame_y)

        # Cria texto para modo de jogo.
        self.__mode_text = self.create_text(
            str(), x = frame_x + frame_width / 2, y = frame_y + frame_height * 0.25,
            color = (30, 30, 30, 255), font_size = int(self.width * 0.026), font_name = "Comic Sans MS",
            anchor_x = "center", anchor_y = "center", batch = self.__text_batch
        )

        # Cria texto para data de jogo.
        self.__date_text = self.create_text(
            str(), x = frame_x + frame_width / 2, y = self.__board_y * 0.95,
            color = (30, 30, 30, 255), font_size = int(self.width * 0.012), font_name = "Comic Sans MS",
            anchor_x = "center", anchor_y = "bottom", batch = self.__text_batch
        )        

        # Cria texto para o resultado do jogo.
        self.__result_text = self.create_text(
            str(), x = result_x, y = result_y, font_name = "Arial Black",
            color = (30, 30, 30, 255), font_size = int(self.width * 0.024),
            anchor_x = "center", anchor_y = "top", batch = self.__text_batch
        )

        # Cria texto para a quantidade de peças no tabuleiro.
        self.__black_piece_text = self.create_text(
            str(), x = piece_x + piece_size * 1.1, y = piece_y + piece_size * 0.5,
            color = (30, 30, 30, 255), font_size = int(self.width * 0.02),
            anchor_x = "left", anchor_y = "center", batch = self.__text_batch
        )
        
        self.__white_piece_text = self.create_text(
            str(), x = piece_x + piece_size * 1.1, y = piece_y - piece_size * 1.5 + piece_size * 0.5,
            color = (30, 30, 30, 255), font_size = int(self.width * 0.02),
            anchor_x = "left", anchor_y = "center", batch = self.__text_batch
        )

        # Cria as imagens das peças.
        black_piece_filename = application.paths.get_image("history", "black_piece.png")
        black_piece_image = self.load_image(black_piece_filename, (piece_size, piece_size))

        white_piece_filename = application.paths.get_image("history", "white_piece.png")
        white_piece_image = self.load_image(white_piece_filename, (piece_size, piece_size))
        
        self.__black_piece = self.create_sprite(black_piece_image, piece_x, piece_y, batch = self.__batch)
        self.__white_piece = self.create_sprite(white_piece_image, piece_x, piece_y - piece_size * 1.5, batch = self.__batch)

        # Cria a borda para o tabuleiro.
        self.__board_border = self.create_rectangle(
            self.__board_x - 1, self.__board_y - 1,
            self.__board_size + 2, self.__board_size + 2,
            color = (0, 0, 0)
        )
        self.__board = None

    def __change_game(self):
        """
        Troca o jogo em exibição.
        """
        if not self.__game_list: return self.__set_empty_history()

        self.__game = self.__game_list[self.__index]
        self.__mode_text.text = "JOGO " + self.__game[0]
        self.__date_text.text = self.__game[5]

        # Define a mensagem de resultado do jogo.
        if self.__game[1].upper() == "WHITE":
            self.__result_text.text = "VITÓRIA"
            self.__result_text.color = (0, 180, 0, 255)
        else:
            self.__result_text.text = "DERROTA"
            self.__result_text.color = (180, 0, 0, 255)

        # Define a quantidade de peças no tabuleiro.
        self.__black_piece_text.text = str(self.__game[2])
        self.__white_piece_text.text = str(self.__game[3])

        # Define a imagem do tabuleiro.
        self.free_memory(save_original = False)
        self.__set_board_image()

    def __set_board_image(self):
        """
        Define a imagem de tabuleiro.
        """
        game_id = self.__game[4]
        
        board_filename = self.get_application().paths.get_replay_image("{}.png".format(game_id))
        board_image = self.load_image(board_filename, (self.__board_size, self.__board_size))

        if not self.__board: self.__board = self.create_sprite(board_image, self.__board_x, self.__board_y)
        else: self.__board.image = board_image

    def __set_empty_history(self):
        """
        Define o estado de histórico vazio.
        """
        self.__mode_text.text = "Histórico Vazio"
        self.__date_text.text = ""
        
        self.__black_piece_text.text = ""
        self.__white_piece_text.text = ""
        self.__result_text.text = ""
        
        self.__board = None
        self.__game = None

    def set_history(self, game_list):
        """
        Define os jogos disponíveis para replay.
        """
        self.__game_list = game_list
        self.__index = 0
        self.__change_game()

    def set_replay_function(self, function):
        """
        Define uma função de replay.
        """
        self.__replay_function = function

    def on_draw_screen(self, by_scheduler = False):
        """
        Evento para desenhar a tela.
        """
        self.__background_image.blit(0, 0)
        self.__frame.draw()
        
        self.__batch.draw()
        self.__text_batch.draw()
        
        if self.__game:
            self.__board_border.draw()
            self.__board.draw()

    def on_key_press(self, symbol, modifiers):
        """
        Evento de tecla pressionada.
        """
        if symbol == key.F12: return self.print_screen()
        
        # Caso o ESC seja apertado, significa que o usuário deseja sair desta tela.
        if symbol == key.ESCAPE:
            self.get_application().go_back()

        # Troca o jogo em exibição.
        elif symbol == key.DOWN:
            self.__index = (self.__index + 1) % len(self.__game_list)
            self.__change_game()
            
        elif symbol == key.UP:
            self.__index = (self.__index - 1) % len(self.__game_list)
            self.__change_game()

        # Inicia o replay do jogo, utilizando o ID do mesmo.
        elif symbol in [key.ENTER, key.SPACE]:
            self.__replay_function(self.__game[4])

        return True

    def on_mouse_motion(self, *args):
        """
        Evento de movimentação do cursor.
        """
        x, y = super().on_mouse_motion(*args)[0: 2]

    def on_mouse_release(self, *args):
        """
        Evento de botão do mouse pressionado e liberado.
        """
        x, y, mouse_button = super().on_mouse_release(*args)[0: 3]
        if mouse_button != mouse.LEFT: return
