from models import FileSystem
from ui.gui import Gui

fs: FileSystem = FileSystem.load()

if __name__ == '__main__':
    Gui(fs)