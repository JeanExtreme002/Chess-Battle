from socket import gethostname, gethostbyname

__all__ = ("default_settings",)

default_settings = {
    "size": (1280, 720),
    "volume": 100,
    "muted": False,
    "address": [gethostbyname(gethostname()), 5000]
}
