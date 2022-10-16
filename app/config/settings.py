from .paths import paths
from socket import gethostname, gethostbyname
import base64, json, uuid

__all__ = ("settings",)

class Crypt(object):
    """
    Classe estática para criptografar
    e descriptografar textos.
    """
    @staticmethod
    def __crypt(string, key):
        new_string = ""

        for char in string:
            new_string += chr(ord(char) + key)
        return new_string
    
    @staticmethod
    def encrypt(string, key):
        """
        Criptografa o texto, a partir de uma chave numérica.
        """
        string = Crypt.__crypt(string, key).encode()
        return base64.b64encode(string).decode()

    @staticmethod
    def decrypt(string, key):
        """
        Descriptografa o texto, a partir de uma chave numérica.
        """
        string = base64.b64decode(string.encode())
        return Crypt.__crypt(string.decode(), -1 * key)


class ApplicationSettings(object):
    """
    Classe para carregar e salvar
    configurações do aplicativo.
    """
    __settings = {
        "size": (1280, 720),
        "volume": 100,
        "muted": False,
        "address": (gethostbyname(gethostname()), 5000)
    }

    __SECRET_KEY = int(uuid.getnode()) % 10000
    
    def __init__(self):
        self.__filename = paths.settings_filename
        self.__load_settings()

    def __getattribute__(self, key):
        return super().__getattribute__(key) if key.startswith("_") else self.__settings[key]

    def __setattr__(self, key, value):
        if key.startswith("_"):
            return super().__setattr__(key, value)

        self.__settings[key] = value
        self.__save_settings()

    def __load_settings(self):
        """
        Carrega as configurações de um arquivo.
        """
        try:
            file = open(self.__filename, encoding = "UTF-8")
            self.__settings.update(json.loads(Crypt.decrypt(file.read(), self.__SECRET_KEY)))
            file.close()

        except Exception as error:
            pass
        
        finally:
            self.__save_settings()

    def __save_settings(self):
        """
        Salva as configurações em um arquivo.
        """
        with open(self.__filename, "w", encoding = "UTF-8") as file:
            string = json.dumps(self.__settings)
            file.write(Crypt.encrypt(string, self.__SECRET_KEY))
        
settings = ApplicationSettings()
