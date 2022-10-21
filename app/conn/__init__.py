from .crypt import ConnectionCrypter
from socket import socket, timeout, AF_INET, SOCK_STREAM 

class Connection(object):
    """
    Classe para criar uma conexão com outro jogador.
    """
    __checking_string = "Check"
    
    def __init__(self, address, host = False):
        self.__socket = None
        self.__connection = None
        
        self.__address = tuple(address)
        self.__hosting = host

        self.__crypter = ConnectionCrypter(address)

    def __send_data(self, string, encrypt = True):
        """
        Envia os dados para o receptor.
        """
        sender = self.__connection if self.__hosting else self.__socket
        if encrypt: string = self.__crypter.encrypt(string)
        
        sender.send(string.encode())

    def close(self):
        """
        Encerra a conexão.
        """
        if self.__connection: self.__connection.close()
        if self.__socket: self.__socket.close()

        self.__connection = None
        self.__socket = None

    def connect(self, timeout = 5):
        """
        Estabelece uma conexão.
        """
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.settimeout(timeout)

        try:
            if self.__hosting:
                self.__socket.bind(self.__address)
                self.__socket.listen(1)

                self.__connection = self.__socket.accept()[0]
            else:
                self.__socket.connect(self.__address)
        except: self.close()
            
    def is_connected(self, attempts = 1):
        """
        Verifica se está conectado.
        """
        if not self.__connection and not self.__socket: return False

        for i in range(attempts):
            try:
                self.__send_data(self.__checking_string, encrypt = False)
                return True
            except: pass
        return False

    def recv(self):
        """
        Retorna as coordenadas de origem e destino.
        """
        getter = self.__connection if self.__hosting else self.__socket

        try:
            string = getter.recv(256).decode()
            string = string.replace(self.__checking_string, "")
            string = self.__crypter.decrypt(string)
            
        except ConnectionResetError:
            self.close()
            return False
            
        except timeout:
            return

        if len(string) == 4:
            origin = (int(string[0]), int(string[1]))
            dest = (int(string[2]), int(string[3]))
            return origin, dest

    def send(self, origin, dest):
        """
        Envia as coordenadas de origem e destino.
        """
        try:
            self.__send_data("{}{}{}{}".format(*origin, *dest))
            return True

        except ConnectionResetError:
            self.close()
            return False
        
        except timeout:
            return False 

