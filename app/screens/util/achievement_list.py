from .widget import Widget

class AchievementList(Widget):
    """
    Classe para criar um popup com uma mensagem na tela.
    """
  
    def __init__(self, screen, size, image, font_size, widget_group = None):
        pass

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        pass

    def __move(self, direction = 1):
        """
        Move as conquistas verticalmente.
        """
        pass

    def draw(self):
        """
        Desenha o widget na tela.
        """
        pass

    def add_achievement(self, title, description, date):
        """
        Define uma mensagem a ser exibida.
        """
        pass
