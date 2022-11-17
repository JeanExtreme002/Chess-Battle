from ..crypter import Crypter
import sys, uuid

class FileCrypter(Crypter):
    """
    Classe para criptografar e descriptografar
    dados de arquivos locais.
    """

    def generate_key(self, password):
        """
        Recebe uma senha e retorna uma chave parcial.
        """
        salt = sys.platform + str(uuid.getnode())
        return password + salt
