import logging

from models import FileSystem
from models.auth import Authentication
from services.authservice import AuthService
from ui.gui import FileManager

logging.basicConfig(level=logging.DEBUG)
fs: FileSystem = FileSystem.load()

if __name__ == '__main__':
    AuthService.init(Authentication('root'))
    FileManager(fs)
