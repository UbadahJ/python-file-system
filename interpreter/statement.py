from abc import ABC, abstractmethod
from io import TextIOBase
from typing import Optional

from models import FileSystem


class Statement(ABC):
    fs: FileSystem
    statement: str
    log: bool
    out: Optional[TextIOBase] = None

    def __init__(self, fs: FileSystem, statement: str, out: Optional[TextIOBase] = None, log=False):
        self.fs = fs
        self.statement = statement
        self.out = out
        self.log = log
        self.initialize()

    @property
    @abstractmethod
    def command(self) -> str: ...

    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def execute(self) -> None: ...

    def pprint(self, *args, is_log=False, sep=' ', end='\n'):
        if self.out is not None:
            if is_log and not self.log:
                return

            print(*args, sep=sep, end=end, file=self.out)
