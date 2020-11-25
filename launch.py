from models import FileSystem
from ui.gui import Gui
import logging

logging.basicConfig(level=logging.DEBUG)
fs: FileSystem = FileSystem.load()

if __name__ == '__main__':
    Gui(fs)