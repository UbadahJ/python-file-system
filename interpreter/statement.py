from abc import ABC, abstractmethod
from typing import Optional, List, TextIO

from models import FileSystem


class Statement(ABC):
    fs: FileSystem
    statement: str
    args: Optional[List[str]] = None
    log: bool = False
    out: Optional[TextIO] = None

    def __init__(self, fs: FileSystem, statement: str, out: Optional[TextIO] = None, log=False):
        self.fs = fs
        self.statement = statement
        self.out = out
        self.log = log
        try:
            self.args = statement.split(maxsplit=1)[1].split(',')
        except:
            pass
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
