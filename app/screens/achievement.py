from .screen import Screen
from pyglet.window import mouse, key

class AchievementScreen(Screen):
    """
    Classe para criar uma tela de histórico de partidas.
    """
    
    def __init__(self, application):
        super().__init__(application)
        self.__build()

        self.__titles = []
        self.__moving = False
        
    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar a tela.
        """
        application = self.get_application()
        
        self.__batch = self.create_batch()
        self.__text_batch = self.create_batch()

        # Calcula a posição e o tamanho das conquistas.
        self.__achievement_width = self.width * 0.7
        self.__achievement_height = self.__achievement_width * 0.15
        self.__achievement_x = self.width / 2 - self.__achievement_width / 2
        self.__achievement_vertical_margin = self.height * 0.1

        self.__start = self.__achievement_vertical_margin
        self.__end = self.__achievement_vertical_margin
        self.__velocity = self.__achievement_height * 0.2
    
        # Cria o plano de fundo.
        background_filename = application.paths.get_image("achievement", "background.png")
        self.__background_image = self.load_image(background_filename, (self.width, self.height))

        # Carrega a imagem de conquista.
        self.__achievement_filename = application.paths.get_image("achievement", "achievement.png")
        self.__achievement_image = self.load_image(self.__achievement_filename, (self.__achievement_width, self.__achievement_height))
        self.__achievements = []

    def __move(self, direction = 1):
        """
        Move a lista de conquistas verticalmente.
        """
        if direction > 0 and self.__end + self.__achievement_height <= (self.height - self.__achievement_vertical_margin): return
        if direction < 0 and self.__start >= self.__achievement_vertical_margin: return
        
        self.__end += self.__velocity * direction * -1
        self.__start += self.__velocity * direction * -1
    
        for achievement in self.__achievements:
            for widget in achievement:
                widget.y += self.__velocity * direction * 2

    def add_achievement(self, title, description, date):
        """
        Adiciona mais uma conquista para a lista.
        """
        if title in self.__titles: return

        self.__end += (self.__achievement_height * 1.4) if self.__titles else 0
        self.__titles.append(title)
        
        background = self.create_sprite(
            self.__achievement_image, x = self.__achievement_x,
            y = self.__end, batch = self.__batch
        )
        
        title = self.create_text(
            title, self.__achievement_x + self.__achievement_width * 0.2,
            self.__end + self.__achievement_height * 0.3,
            anchor_x = "left", anchor_y = "center",
            batch = self.__text_batch,
            font_name = "Comic Sans MS",
            font_size = self.width * 0.017,
            color = (255, 255, 255, 255)
        )  

        description = self.create_text(
            description, self.__achievement_x + self.__achievement_width * 0.2,
            self.__end + self.__achievement_height * 0.7,
            anchor_x = "left", anchor_y = "center",
            batch = self.__text_batch,
            font_size = self.width * 0.012,
            color = (235, 235, 235, 255)
        )

        date = self.create_text(
            date, self.__achievement_x + self.__achievement_width * 0.97,
            self.__end + self.__achievement_height * 0.3,
            anchor_x = "right", anchor_y = "center",
            batch = self.__text_batch,
            font_size = self.width * 0.01,
            color = (245, 245, 245, 255)
        )
        self.__achievements.append([background, title, description, date])

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
        # Caso o ESC seja apertado, significa que o usuário deseja sair desta tela.
        if symbol == key.ESCAPE:
            self.get_application().go_back()

        # Caso uma das setas verticais seja apertada, a lista será movida verticalmente.
        elif symbol == key.UP: self.__move(direction = -1)
        elif symbol == key.DOWN: self.__move(direction = 1)

        return True
