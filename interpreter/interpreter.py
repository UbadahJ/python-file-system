from models import FileSystem


class Interpreter:
    fs: FileSystem
    src: str
    threads: int

    def __init__(self, fs: FileSystem, src: str, threads: int = 4):
        self.fs = fs
        self.src = src
        self.threads = threads


