from .connection_crypter import ConnectionCrypter
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

    def __coordinates_to_string(self, origin, dest):
        """
        Recebe duas tuplas XY, indicando origem e destino,
        e retorna uma string dessas coordenadas.
        """
        return "{}{}{}{}".format(*origin, *dest)

 
    def __send_data(self, string, encrypt = True):
        """
        Envia os dados para o receptor.
        """
        sender = self.__connection if self.is_host() else self.__socket
        if encrypt: string = self.__crypter.encrypt(string)
        
        sender.send(string.encode())
        return True

    def __string_to_coordinates(self, string):
        """
        Recebe uma string e retorna duas tuplas XY,
        indicando origem e destino.
        """
        if len(string) == 4:
            origin = (int(string[0]), int(string[1]))
            dest = (int(string[2]), int(string[3]))
            return origin, dest

    def close(self):
        """
        Encerra a conexão.
        """
        if self.__connection: self.__connection.close()
        if self.__socket: self.__socket.close()

        self.__connection = None
        self.__socket = None

    def connect(self, timeout_in_seconds = 5, attempts = 1):
        """
        Estabelece uma conexão.
        """
        if attempts == 0: return
        
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.settimeout(timeout_in_seconds)

        # Tenta estabelecer uma conexão, criando um servidor
        # ou se conectando à um servidor existente.
        try:
            if self.is_host():
                self.__socket.bind(self.__address)
                self.__socket.listen(1)

                self.__connection = self.__socket.accept()[0]
            else:
                self.__socket.connect(self.__address)

        # Caso o tempo para conectar tenha excedido, uma nova
        # tentativa de conexão será realizada.
        except timeout:
            self.close()
            self.connect(timeout_in_seconds, attempts - 1)

        # Se outro tipo de exceção ocorreu, uma nova tentativa
        # de conexão será realizada somente se o modo de abertura
        # de conexão não for host. Caso o contrário, significaria
        # que pode existir algum problema no endereço informado.
        # Neste caso, é inútil realizar novas tentativas.
        except:
            self.close()
            
            if not self.is_host():
                self.connect(timeout_in_seconds, attempts - 1)
            
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

    def is_host(self):
        """
        Verifica se é um host ou client.
        """
        return self.__hosting

    def recv(self):
        """
        Retorna as coordenadas de origem e destino.
        """
        getter = self.__connection if self.is_host() else self.__socket

        try:
            string = getter.recv(256).decode()
            string = string.replace(self.__checking_string, "")
            string = self.__crypter.decrypt(string)
            return self.__string_to_coordinates(string)
            
        except (ConnectionAbortedError, ConnectionResetError):
            self.close()
            
        except timeout: pass

    def send(self, origin, dest):
        """
        Envia as coordenadas de origem e destino.
        """
        try:
            string = self.__coordinates_to_string(origin, dest)
            return self.__send_data(string)

        except ConnectionResetError:
            self.close()
        
        except timeout: pass

        return False 

