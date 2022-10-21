from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

class ConnectionCrypter(object):
    """
    Classe para encriptografar e descriptografar
    os dados trafegados pela conexão.
    """
    def __init__(self, address):
        self.__fernet = Fernet(self.__get_key(address))

    def __get_key(self, address):
        """
        Gera uma chave de criptografia.
        """
        password = str()

        for index in range(0, len(address[0]), 2):
            password += address[0][index: index + 2]
            
            if index // 2 < len(str(address[1])):
                 password += str(address[1])[index // 2]
    
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
