import logging

from client.models.remotesystem import RemoteFileSystem
from models import FileSystem
from ui.gui import FileManager

logging.basicConfig(level=logging.DEBUG)
fs: FileSystem

if __name__ == '__main__':
    fs = RemoteFileSystem('192.168.18.7', 5500)
    FileManager(fs)
