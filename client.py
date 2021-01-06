import logging

from client.ui.gui import ClientConfig
from models import FileSystem

logging.basicConfig(level=logging.DEBUG)
fs: FileSystem

if __name__ == '__main__':
    ClientConfig()
