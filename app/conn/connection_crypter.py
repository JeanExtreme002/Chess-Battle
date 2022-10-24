from ..crypter import Crypter
import time

class ConnectionCrypter(Crypter):
    """
    Classe para encriptografar e descriptografar
    os dados trafegados pela conexão.
    """
    def __init__(self, address, connection):
        self.__connection = connection
        super().__init__(address)

    def generate_key(self, address):
        """
        Recebe uma senha e retorna uma chave parcial.
        """
        password = str()

        for index in range(0, len(address[0]), 2):
            password += address[0][index: index + 2]
            
            if index // 2 < len(str(address[1])):
                 password += str(address[1])[index // 2]

        salt = str(time.time())

        self.__connection.send(salt.encode())
        salt += self.__connection.recv(128).decode()

        return password + salt
