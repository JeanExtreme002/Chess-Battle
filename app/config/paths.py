import random
import os

__all__ = ("paths",)

class Paths(object):

    sound_path = "sounds"
    image_path = "images"

    data_path = "data"
    database_path = os.path.join(data_path, "database")
    settings_filename = os.path.join(data_path, "settings.json")

    __image_extensions = (".png", ".jpg", ".jpeg")
    __sound_extensions = (".mp3",)

    def __init__(self):
        for key, value in self.__class__.__dict__.items():
            if key.endswith("path"): self.__initialize_directory(value)

    def __initialize_directory(self, path):
        if not os.path.exists(path): os.mkdir(path)

    def __setattr__(self, key, value):
        raise AttributeError("'{}' object has no attribute '{}'".format(
            self.__class__.__name__, key
        ))

    def __get_file(self, base, *path):
        return os.path.join(base, *path)

    def __get_file_list(self, base, extensions, *folders):
        path = os.path.join(base, *folders)

        for filename in os.listdir(path):
            if "." + filename.split(".")[-1] in extensions:
                yield os.path.join(path, filename)
    
    def get_image(self, *path):
        return self.__get_file(self.image_path, *path)

    def get_sound(self, *path):
        return self.__get_file(self.sound_path, *path)

    def get_image_list(self, *folders):
        for file in self.__get_file_list(self.image_path, self.__image_extensions, *folders):
            yield file

    def get_sound_list(self, *folders):
        for file in self.__get_file_list(self.sound_path, self.__sound_extensions, *folders):
            yield file

    def get_random_image(self, *folders):
       filenames = list(self.get_image_list(*folders))
       return random.choice(filenames)

    def get_random_sound(self, *folders):
       filenames = list(self.get_sound_list(*folders))
       return random.choice(filenames)

paths = Paths()
