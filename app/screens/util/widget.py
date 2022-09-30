class Widget(object):
    def __init__(self, screen, batch, x, y, size):
        self.__screen = screen
        self.__batch = batch

        self.__position = (x, y)
        self.__size = size

    @property
    def screen(self):
        return self.__screen

    @property
    def batch(self):
        return self.__batch

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
