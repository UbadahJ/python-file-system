from abc import ABC, abstractmethod

from models import FileSystem


class Statement(ABC):
    fs: FileSystem
    statement: str

    def __init__(self, fs: FileSystem, statement: str):
        self.fs = fs
        self.statement = statement
        self.initialize()

    @property
    @abstractmethod
    def command(self) -> str: ...

    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def execute(self) -> None: ...
