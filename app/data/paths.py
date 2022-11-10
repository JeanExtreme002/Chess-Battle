import random
import os

__all__ = ("Paths",)

class Paths(object):
    """
    Classe responsável por gerenciar
    diretórios e nomes de arquivos.
    """
    sound_path = "sounds"
    image_path = "images"

    data_path = "data"
    database_path = os.path.join(data_path, "database")

    achievements_filename = os.path.join(data_path, "0001.userdata")
    settings_filename = os.path.join(data_path, "0002.userdata")

    __image_extensions = (".png", ".jpg", ".jpeg")
    __sound_extensions = (".mp3", ".wav")

    def __init__(self):
        for key, value in self.__class__.__dict__.items():
            if key.endswith("path"): self.__initialize_directory(value)

    def __setattr__(self, key, value):
        raise AttributeError("'{}' object has no attribute '{}'".format(
            self.__class__.__name__, key
        ))

    def __get_file(self, base, *path):
        """
        Retorna o nome do arquivo com os separadores corretos.
        """
        return os.path.join(base, *path)

    def __get_file_list(self, base, extensions, *folders):
        """
        Retorna lista de todos os arquivos presentes em
        um diretório, filtrando os arquivos pela sua extensão.
        """
        path = os.path.join(base, *folders)
        filenames = []
        
        for filename in os.listdir(path):
            if "." + filename.split(".")[-1] in extensions:
                filenames.append(os.path.join(path, filename))
        return filenames

    def __initialize_directory(self, path):
        """
        Cria um diretório se ele não existir.
        """
        if not os.path.exists(path): os.mkdir(path)
    
    def get_image(self, *path):
        """
        Retorna o nome do arquivo de imagem com os separadores corretos.
        """
        return self.__get_file(self.image_path, *path)

    def get_image_list(self, *folders, shuffle = False):
        """
        Retorna lista de todos os arquivos de imagem
        presentes em um dado diretório.
        """
        images = self.__get_file_list(self.image_path, self.__image_extensions, *folders)

        if shuffle: random.shuffle(images)
        return images

    def get_random_image(self, *folders):
        """
        Retorna um arquivo de imagem aleatório, de um dado diretório.
        """
        filenames = list(self.get_image_list(*folders))
        return random.choice(filenames)

    def get_random_sound(self, *folders):
        """
        Retorna um arquivo de som aleatório, de um dado diretório.
        """
        filenames = list(self.get_sound_list(*folders))
        return random.choice(filenames)

    def get_sound(self, *path):
        """
        Retorna o nome do arquivo de som com os separadores corretos.
        """
        return self.__get_file(self.sound_path, *path)

    def get_sound_list(self, *folders, shuffle = False):
        """
        Retorna lista de todos os arquivos de som
        presentes em um dado diretório.
        """
        sounds = self.__get_file_list(self.sound_path, self.__sound_extensions, *folders)
            
        if shuffle: random.shuffle(sounds)
        return sounds
