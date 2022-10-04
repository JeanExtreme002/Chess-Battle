from socket import socket, AF_INET, SOCK_STREAM 

class Connection(object):
    __checking_string = "Check"
    
    def __init__(self, address, host = False):
        self.__socket = None
        self.__connection = None
        
        self.__address = address
        self.__hosting = host

    def __send_data(self, string):
        sender = self.__connection if self.__hosting else self.__socket
        sender.send(string.encode())

    def connect(self):
        self.__socket = socket(AF_INET, SOCK_STREAM)
        
        if self.__hosting:
            self.__socket.bind(self.__address)
            self.__socket.listen(1)
            self.__connection = self.__socket.accept()[0]
        else:
            self.__socket.connect(self.__address)

    def is_connected(self):
        try:
            self.__send_data(self.__checking_string)
            return True
        except: return False

    def recv(self):
        getter = self.__connection if self.__hosting else self.__socket
        return getter.recv(64).decode().replace(self.__checking_string, "")

    def send(self, origin, dest):
        self.__send_data("{}{}{}{}".format(*origin, *dest))

    def close(self):
        if self.__connection: self.__connection.close()
        if self.__socket: self.__socket.close()

        self.__connection = None
        self.__socket = None
        
