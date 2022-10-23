from .file_crypter import FileCrypter
from .paths import Paths
from .settings import ApplicationSettings

__all__ = ("paths", "settings")

paths = Paths()

file_crypter = FileCrypter()

settings_filename = paths.settings_filename
settings = ApplicationSettings(settings_filename, file_crypter)

