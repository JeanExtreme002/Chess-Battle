from .paths import paths
from socket import gethostname, gethostbyname
import json

__all__ = ("settings",)

class ApplicationSettings(object):

    __settings = {
        "title": "Xadrez",
        "size": (1280, 720),
        "address": (gethostbyname(gethostname()), 5000)
    }
    
    def __init__(self):
        self.__filename = paths.settings_filename
        self.__load_settings()

    def __getattribute__(self, key):
        return super().__getattribute__(key) if key.startswith("_") else self.__settings[key]

    def __setattribute__(self, key, value):
        self.__settings[key] = value
        self.__save_settings()

    def __load_settings(self):  
        try:
            file = open(self.__filename)
            self.__settings.update(json.load(file))
            file.close()
        finally:
            self.__save_settings()

    def __save_settings(self):
        with open(self.__filename, "w") as file:
            json.dump(self.__settings, file)


settings = ApplicationSettings()
