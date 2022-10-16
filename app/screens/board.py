from .screen import Screen
from .util.confirmation_box import ConfirmationBox
from pyglet.window import mouse, key

class BoardScreen(Screen):
    """
    Classe para criar a tela do tabuleiro.
    """
    
    __LOCAL_MODE = 0
    __ONLINE_MODE = 1

    __BORDER_COLOR = (0, 0, 0)
    __LIGHT_COLOR = (255, 248, 220)
    __DARK_COLOR = (100, 71, 50)
    
    def __init__(self, application):
        super().__init__(application)

        self.__mode = None
        self.__game = None
        self.__player_input = None
        self.__player_output = None

        self.__moving = False
        
        self.__selected_piece = None
        self.__selected_piece_index = None
        self.__selected_piece_position = None
        
        self.__piece_sprites = [[None,] * 8 for i in range(8)]
        self.__destroyed_piece_sprites = {"white": list(), "black": list()}

        self.__build()
        
    def __build(self):
        """
        Método para criar todas as imagens e objetos
        gráficos necessários para desenhar a tela.
        """
        application = self.get_application()
        
        self.__batch = self.create_batch()
        self.__piece_batch = self.create_batch()
        self.__selected_piece_batch = self.create_batch()
        
        confirmation_box_batch = self.create_batch()

        # Obtém o tamanho do tabuleiro, que deve ser divisível por oito.
        self.__board_size = int(self.height * 0.9)

        while self.__board_size % 8 != 0:
            self.__board_size -= 1
        
        self.__square_size = self.__board_size // 8
        self.__destroyed_piece_size = self.__square_size * 0.5

        # Obtém a posição do tabuleiro.
        self.__board_y = (self.height - self.__board_size) / 2
        self.__board_x = self.__board_y

        # Obtém o tamanho e a posição do placar e seus elementos.
        score_board_area_x = self.__board_size + self.__board_x
        score_board_area_width = (self.width - score_board_area_x)
        
        self.__score_board_height = self.height - (self.__board_y * 2)
        self.__score_board_width = self.__score_board_height * 0.7
        self.__score_board_x = score_board_area_x + score_board_area_width / 2 - self.__score_board_width / 2
        self.__score_board_y = self.__board_y

        # Obtém o tamanho e a posição da caixa de mensagem.
        message_box_width = self.width * 0.45
        message_box_height = message_box_width * 0.7
        message_box_x = self.width / 2 - message_box_width / 2
        message_box_y = self.height / 2 - message_box_height / 2

        # Inicializa as imagens de peças.
        self.__load_piece_images(self.__square_size)
        self.__load_destroyed_piece_images(self.__destroyed_piece_size)

        # Cria o plano de fundo.
        background_filename = application.paths.get_image("board", "background.png")
        self.__background_image = self.load_image(background_filename, (self.width, self.height))

        # Cria a imagem do placar.
        score_board_filename = application.paths.get_image("board", "score_board.png")
        score_board_image = self.load_image(score_board_filename, (self.__score_board_width, self.__score_board_height))

        self.__score_board_sprite = self.create_sprite(
            score_board_image, batch = self.__batch,
            x = self.__score_board_x, y = self.__score_board_y
        )  

        # Cria a borda do tabuleiro.
        self.__board_border = self.create_rectangle(
            self.__board_x - 2, self.__board_y - 2,
            self.__board_size + 4, self.__board_size + 4,
            batch = self.__batch, color = self.__BORDER_COLOR
        )

        # Cria os quadrados do tabuleiro e as peças.
        self.__square_shapes = []
        self.__piece_buttons = []
        
        for row in range(8):
            for column in range(8):
                x, y = self.__get_piece_image_pos(column, row)

                # Alterna a cor da casa, com base nas coordenadas.
                if (column + row) % 2 == 0:
                    color = self.__LIGHT_COLOR
                else: color = self.__DARK_COLOR

                square = self.create_rectangle(
                    x, y, self.__square_size, self.__square_size,
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

    def __add_destroyed_piece(self, piece):
        """
        Registra a dada peça destruída e cria sua imagem no placar.
        """
        color = "white" if piece.color.value == 0 else "black"
        image = self.__destroyed_piece_images[color][piece.name]

        sprite_list = self.__destroyed_piece_sprites[color]
        index = len(sprite_list)

        spacing_x = self.__destroyed_piece_size * 1.5
        spacing_y = self.__destroyed_piece_size * 1.1

        # Calcula a posição da peça destruída.
        if color == "black":
            x = self.__score_board_x + self.__score_board_width * 0.4 - self.__destroyed_piece_size
            x -= spacing_x if index >= 8 else 0
        else:
            x = self.__score_board_x + self.__score_board_width * 0.6
            x += spacing_x if index >= 8 else 0

        y = self.__score_board_y + self.__score_board_height * 0.3 + spacing_y * (index % 8)

        # Cria a imagem, adicionado-a à lista.
        sprite = self.create_sprite(
            image, batch = self.__piece_batch,
            x = x, y = y
        )
        sprite_list.append(sprite)

    def __delete_destroyed_pieces(self):
        """
        Apaga o registro das peças destruídas,
        junto com suas imagens criadas.
        """
        for color, sprite_list in self.__destroyed_piece_sprites.items():
            for sprite in sprite_list: sprite.delete()
            self.__destroyed_piece_sprites[color] = []

    def __get_coord_on_board(self, x, y):
        """
        Retorna a posição da casa do tabuleiro
        em que o cursor se encontra no momento.
        """
        if not self.__is_mouse_on_board(x, y): return
        
        step = self.__square_size

        # Percorre cada casa do tabuleiro.
        for index_x in range(8):
            for index_y in range(8):
                pos_x, pos_y = self.__get_piece_image_pos(index_x, index_y)

                # Verifica se o cursor está dentro dos limites da casa do tabuleiro em questão.
                if pos_x <= x <= pos_x + step and pos_y <= y <= pos_y + step:
                    return index_y, index_x

    def __get_piece_image_pos(self, x, y):
        """
        Retorna a posição na tela da imagem de peça, dadas
        as coordenadas da mesma no tabuleiro.
        """
        pos_x = self.__board_x + self.__square_size * x
        pos_y = self.__board_y + self.__square_size * y
        return pos_x, pos_y

    def __is_mouse_on_board(self, x, y):
        """
        Verifica se o cursor está dentro do campo do tabuleiro.
        """
        on_x = self.__board_x <= x <= self.__board_x + self.__board_size
        on_y = self.__board_y <= y <= self.__board_y + self.__board_size
        return on_x and on_y

    def __load_destroyed_piece_images(self, size):
        """
        Carrega as imagens das peças do jogo,
        salvando-as em um dicionário.
        """
        application = self.get_application()

        piece_names = ["king", "queen", "bishop", "knight", "pawn", "rook"]
        
        self.__destroyed_piece_images = {
            "black": dict(),
            "white": dict()
        }

        for color in self.__destroyed_piece_images.keys():
            for name in piece_names:
                piece_filename = application.paths.get_image("board", "pieces", "{}_{}.png".format(color, name))
                piece_image = self.load_image(piece_filename, (size, size), save = False)
                self.__destroyed_piece_images[color][name] = piece_image

    def __load_piece_images(self, size):
        """
        Carrega as imagens das peças do jogo,
        salvando-as em um dicionário.
        """
        application = self.get_application()

        piece_names = ["king", "queen", "bishop", "knight", "pawn", "rook"]
        
        self.__piece_images = {
            "black": dict(),
            "white": dict()
        }

        for color in self.__piece_images.keys():
            for name in piece_names:
                piece_filename = application.paths.get_image("board", "pieces", "{}_{}.png".format(color, name))
                piece_image = self.load_image(piece_filename, (size, size), save = False)
                self.__piece_images[color][name] = piece_image

    def __move_piece(self, row, column):
        """
        Move a peça selecionada para uma posição XY, se possível.
        """
        old_row, old_column = self.__selected_piece_index
        selected_piece = self.__game.get_piece(old_row, old_column)
        dest_piece = self.__game.get_piece(row, column)

        self.__stop_moving()

        # Se a jogada ocorreu com sucesso, o tabuleiro é completamente atualizado.
        if self.__game.play(selected_piece, (row, column)):
            
            # Se havia peça na posição de destino, o som a ser reproduzido
            # será o de ataque, além de que a peça será registrada como
            # destruída. Caso contrário, será de movimento.
            if dest_piece:
                self.__add_destroyed_piece(dest_piece)
                self.sound_player.play_attacking_sound()
            else:
                self.sound_player.play_movement_sound()

            # Atualiza o tabuleiro na tela.
            self.__update_piece_sprites()

    def __select_piece(self, row, column):
        """
        Define uma peça a ser selecionada, para que a mesma
        possa ser movida livremente com o cursor.
        """
        self.__moving = True

        sprite = self.__piece_sprites[row][column]
        sprite.batch = self.__selected_piece_batch
        
        self.__selected_piece = sprite
        self.__selected_piece_index = (row, column)
        self.__selected_piece_position = (sprite.x, sprite.y)

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

    def __stop_moving(self):
        """
        Interrompe o movimento da peça selecionada, fazendo-a
        voltar à sua posição original no tabuleiro.
        """
        self.__moving = False

        if self.__selected_piece:
            self.__selected_piece.batch = self.__piece_batch
            self.__selected_piece.x = self.__selected_piece_position[0]
            self.__selected_piece.y = self.__selected_piece_position[1]
        
        self.__selected_piece = None
        self.__selected_piece_index = None
        self.__selected_piece_position = None

    def __update_piece_sprites(self):
        """
        Atualiza o tabuleiro, criando toda as imagens das peças.
        """
        for row in range(8):
            for column in range(8):
                
                # Deleta a imagem da peça antiga.
                sprite = self.__piece_sprites[row][column]

                if sprite: sprite.delete()
                self.__piece_sprites[row][column] = None

                # Obtém o objeto de peça do jogo.
                piece = self.__game.get_piece(row, column)
                if not piece: continue

                # Obtém a imagem da peça a ser utilizada.
                color = "white" if piece.color.value == 0 else "black"
                image = self.__piece_images[color][piece.name]

                # Calcula a posição da peça no tabuleiro e cria a imagem.
                x, y = self.__get_piece_image_pos(column, row)

                sprite = self.create_sprite(
                    image, batch = self.__piece_batch,
                    x = x, y = y
                )
                self.__piece_sprites[row][column] = sprite
        
    @property
    def LOCAL_MODE(self):
        return self.__LOCAL_MODE

    @property
    def ONLINE_MODE(self):
        return self.__ONLINE_MODE

    def set_new_game(self, game, mode, input_func = None, output_func = None):
        """
        Define um novo jogo.
        """
        self.sound_player.play_start_sound()
        
        self.__game = game
        self.__mode = mode
        self.__player_input = input_func
        self.__player_output = output_func

        self.__delete_destroyed_pieces()
        self.__update_piece_sprites()

    def on_draw(self, by_scheduler = False):
        """
        Evento para desenhar a tela.
        """
        self.__background_image.blit(0, 0)
        self.__batch.draw()
        self.__piece_batch.draw()
        self.__selected_piece_batch.draw()
        self.__confirmation_box.draw()

    def on_key_press(self, symbol, modifiers):
        """
        Evento de tecla pressionada.
        """
        self.__stop_moving()

        # Caso o ESC seja apertado, significa que o usuário deseja sair
        # desta tela. Nesse caso, uma mensagem de confirmação deverá aparecer.
        if symbol == key.ESCAPE:
            if not self.__confirmation_box.has_message():
                self.__set_dialog_box_message(self.__confirmation_box, "Realmente deseja abandonar o jogo?")     
        return True

    def on_mouse_motion(self, *args):
        """
        Evento de movimentação do cursor.
        """
        x, y = super().on_mouse_motion(*args)[0: 2]
        
        if self.__confirmation_box.has_message():
            self.__confirmation_box.check(x, y)

        # Atualiza a posição da imagem da peça selecionada.
        if self.__moving:
            piece = self.__selected_piece
            piece.x = x - piece.width // 2
            piece.y = self.get_true_y_position(y - piece.height // 2, piece.height)

    def on_mouse_release(self, *args):
        """
        Evento de botão do mouse pressionado e liberado.
        """
        x, y, mouse_button = super().on_mouse_release(*args)[0: 3]
        if mouse_button != mouse.LEFT: return

        # Qualquer ação será realizada somente se não houver mensagens sendo mostrada na tela.
        if self.__confirmation_box.has_message():
            cancel, confirm = self.__confirmation_box.check(x, y)

            if not (confirm or cancel): return
            self.__confirmation_box.delete_message()

            # Sai da tela, caso confirmado.
            if confirm: self.get_application().go_back()

        # Obtém a casa do tabuleiro através da posição do cursor.
        coords = self.__get_coord_on_board(x, y)
        if not coords: return

        row, column = coords
    
        # Seleciona uma peça do tabuleiro.
        if not self.__moving:
            piece = self.__game.get_piece(row, column)
            player_color = self.__game.get_player().color

            # Verifica se a peça pertence ao jogador da rodada.
            if not piece or piece.color != player_color: return
            
            self.__select_piece(row, column)

        # Caso a coordenada seja igual à coordenada da peça selecionada,
        # o seu movimento será interrompido.  
        elif (row, column) == self.__selected_piece_index:
            self.__stop_moving()

        # Move a peça de uma casa à outra.
        else: self.__move_piece(row, column)
