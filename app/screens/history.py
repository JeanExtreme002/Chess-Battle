from .screen import Screen
from pyglet.window import mouse, key

class HistoryScreen(Screen):
    """
    Classe para criar uma tela de histórico de partidas.
    """
    
    def __init__(self, application):
        super().__init__(application)
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

        # Cria o plano de fundo.
        background_filename = application.paths.get_image("history", "background.png")
        self.__background_image = self.load_image(background_filename, (self.width, self.height))

        # Cria o frame de partida.
        frame_filename = application.paths.get_image("history", "frame.png")
        frame_image = self.load_image(frame_filename, (frame_width, frame_height))
        self.__frame = self.create_sprite(frame_image, frame_x, frame_y, batch = self.__batch)

        # Cria texto para modo de jogo.
        self.__mode_text = self.create_text(
            str(), x = frame_x + frame_width / 2, y = frame_y + frame_height * 0.25,
            color = (30, 30, 30, 255), font_size = int(self.width * 0.02), font_name = "Comic Sans MS",
            anchor_x = "center", anchor_y = "center", batch = self.__text_batch
        )

    def __change_history(self):
        """
        Troca o jogo em exibição.
        """
        game = self.__game_list[self.__index]
        self.__mode_text.text = "JOGO " + game[0]

    def set_history(self, game_list):
        """
        Define os jogos disponíveis para replay.
        """
        self.__game_list = game_list
        self.__index = 0
        self.__change_history()

    def on_draw_screen(self, by_scheduler = False):
        """
        Evento para desenhar a tela.
        """
        self.__background_image.blit(0, 0)
        self.__batch.draw()
        self.__text_batch.draw()

    def on_key_press(self, symbol, modifiers):
        """
        Evento de tecla pressionada.
        """
        if symbol == key.F12: return self.print_screen()
        
        # Caso o ESC seja apertado, significa que o usuário deseja sair desta tela.
        if symbol == key.ESCAPE:
            self.get_application().go_back()
     
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
