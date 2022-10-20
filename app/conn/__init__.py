from socket import socket, AF_INET, SOCK_STREAM 

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

    def __send_data(self, string):
        """
        Envia os dados para o receptor.
        """
        sender = self.__connection if self.__hosting else self.__socket
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

    def is_connected(self):
        """
        Verifica se está conectado.
        """
        if not self.__connection and not self.__socket: return False
        
        try:
            self.__send_data(self.__checking_string)
            return True
        except: return False

    def recv(self):
        """
        Retorna as coordenadas de origem e destino.
        """
        getter = self.__connection if self.__hosting else self.__socket
        string = getter.recv(64).decode().replace(self.__checking_string, "")

        return string[:2], string[2:]

    def send(self, origin, dest):
        """
        Envia as coordenadas de origem e destino.
        """
        self.__send_data("{}{}{}{}".format(*origin, *dest))

