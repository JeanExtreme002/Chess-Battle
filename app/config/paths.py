import random
import os

__all__ = ("paths",)

class Paths(object):

    sound_path = "sounds"
    sound_effects_path = os.path.join(sound_path, "effects")
    music_path = os.path.join(sound_path, "music")

    image_path = "images"

    data_path = "data"
    database_path = os.path.join(data_path, "database")
    settings_filename = os.path.join(data_path, "settings.json")

    def __init__(self):
        for key, value in self.__class__.__dict__.items():
            if key.endswith("path"): self.__initialize_directory(value)

    def __initialize_directory(self, path):
        if not os.path.exists(path): os.mkdir(path)

    def __setattr__(self, key, value):
        raise AttributeError("'{}' object has no attribute '{}'".format(
            self.__class__.__name__, key
        ))

    def __get_random_file(self, path, *extensions):
        filenames = []
        
        for filename in os.listdir(path):
            if not "." in filename: continue
            
            if "." + filename.split(".")[-1] in extensions:
                filenames.append(filename)
                
        return os.path.join(path, random.choice(filenames))

    def get_image(self, *paths):
        return os.path.join(self.image_path, *paths)

    def get_random_image(self, *folders):
       path = os.path.join(self.image_path, *folders)
       return self.__get_random_file(path, ".png", ".jpg", ".jpeg")

paths = Paths()
