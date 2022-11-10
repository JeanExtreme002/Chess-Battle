import socket
import sys

__all__ = ("default_settings",)

def get_ip_address(remote_server = "8.8.8.8"):
    """
    Retorna o endereço IP privado.
    """
    address = "127.0.0.1"
    
    if "win" in sys.platform:
        hostname = socket.gethostname()
        address = socket.gethostbyname(hostname)

    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    try:
        connection.connect((remote_server, 80))
        address = connection.getsockname()[0]
    finally:
        connection.close()
        return address

default_settings = {
    "size": (1280, 720),
    "volume": 100,
    "muted": False,
    "address": [get_ip_address(), 5000]
}
