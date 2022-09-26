from .paths import paths
import json

class ApplicationSettings(object):

    __default = {
        "title": "Xadrez",
        "resizable": True,
        "size": (1280, 720),
    }
    
    def __init__(self, filename):
        self.__filename = paths.settings_filename
        self.__load_settings()

    def __load_settings(self):  
        try:
            file = open(self.__filename)
            # ...
            file.close()
        except:
            self.__create_default_file()

    def __create_default_file(self):
        with open(self.__filename, "w") as file:
            settings = json.dump(self.__default, file)
        # ...


settings = ApplicationSettings()
