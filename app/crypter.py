from abc import ABC, abstractmethod
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

class Crypter(ABC):
    """
    Classe para criptografar e descriptografar strings.
    """
    def __init__(self, password = str()):
        key = self.generate_key(password)
        key = self.__get_key(key)
        
        self.__fernet = Fernet(key)

    def __get_key(self, password):
        """
        Gera uma chave de criptografia.
        """ 
        digest = hashes.Hash(hashes.SHA256(), backend = default_backend())
        digest.update(password.encode())
        return base64.urlsafe_b64encode(digest.finalize())

    def decrypt(self, string):
        """
        Descriptografa uma string.
        """
        if not string: return str()

        data = bytes(string, encoding = "UTF-8")
        return self.__fernet.decrypt(data).decode()
    
    def encrypt(self, string):
        """
        Criptografa a string, retornando uma string em bytes.
        """
        if not string: return str()

        data = bytes(string, encoding = "UTF-8")
        return self.__fernet.encrypt(data).decode()

    def generate_key(self, password):
        """
        Recebe uma senha e retorna uma chave parcial.
        """
        return password
