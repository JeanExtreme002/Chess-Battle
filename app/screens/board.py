from .screen import Screen
from pyglet import graphics
from pyglet.window import mouse

class BoardScreen(Screen):
    
    __LOCAL_MODE = 0
    __ONLINE_MODE = 1

    __WHITE_COLOR = (255, 255, 255)
    __BLACK_COLOR = (0, 0, 0)
    
    def __init__(self, application, player_input, player_output):
        super().__init__(application)

        self.player_input = player_input
        self.player_output = player_output

        self.__mode = self.LOCAL_MODE
        self.__game = None
        self.__build()

        self.sound_player.play_music()
        
    def __build(self):
        application = self.get_application()
        self.__batch = graphics.Batch()
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
        
        score_board_height = self.height - board_y
        score_board_width = score_board_height * 0.8
        score_board_x = score_board_area_x + score_board_area_width // 2 - score_board_width // 2
        score_board_y = board_y

        player_indicator_size = score_board_area_width * 0.08
        player_indicator_x = score_board_area_x + score_board_area_width // 2 - player_indicator_size // 2
        player_indicator_y = board_y + score_board_height * 0.05

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

        # Cria imagem para indicar a posição dos jogadores no placar.
        player_indicator_filename = application.paths.get_image("board", "players.png")
        player_indicator_image = self.load_image(player_indicator_filename, (player_indicator_size, player_indicator_size))

        self.__player_indicator_sprite = self.create_sprite(
            player_indicator_image, batch = self.__batch,
            x = player_indicator_x, y = player_indicator_y
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

    @property
    def LOCAL_MODE(self):
        return self.__LOCAL_MODE

    @property
    def ONLINE_MODE(self):
        return self.__ONLINE_MODE

    def set_mode(self, mode):
        self.__mode = mode

    def set_game(self, game):
        self.__game = game

    def on_mouse_motion(self, *args):
        x, y = super().on_mouse_motion(*args)[0: 2]

    def on_mouse_release(self, *args):
        x, y, mouse_button = super().on_mouse_release(*args)[0: 3]
        if mouse_button != mouse.LEFT: return

    def on_draw(self, by_scheduler = False):
        self.__background_image.blit(0, 0)
        self.__batch.draw()
