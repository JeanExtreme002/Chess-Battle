from abc import ABC, abstractmethod

class Widget(ABC):
    """
    Classe abstrata para criar widgets na tela.
    """
    def __init__(self, screen, x, y, size, widget_group = None):
        self.__screen = screen
        
        self.__position = (x, y)
        self.__size = size

        if widget_group:
            widget_group.add(self)

    @abstractmethod
    def draw(self): pass

    @property
    def screen(self):
        return self.__screen

    @property
    def x(self):
        return self.__position[0]

    @property
    def y(self):
        return self.__position[1]

    @property
    def width(self):
        return self.__size[0]

    @property
    def height(self):
        return self.__size[1]
