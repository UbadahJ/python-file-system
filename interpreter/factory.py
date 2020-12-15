from typing import List

from interpreter.exception import InvalidStatement
from interpreter.statement import Statement
from models import Memory, File

_file_store: List[File] = []


class OpenFile(Statement):
    src: File

    def command(self) -> str:
        return 'open'

    def initialize(self) -> None:
        try:
            args = super().statement.split()[1]
            self.src = super().fs.current.open_file(*args.split(','))
        except AssertionError as e:
            raise InvalidStatement(self, *e.args)
        except:
            raise InvalidStatement(self, "Invalid arguments")

    def execute(self) -> None:
        self.src.lock.acquire()
        _file_store.append(self.src)
        self.src.lock.release()


class MemoryMap(Statement):
    map: Memory

    def command(self) -> str:
        return 'show_memory_map'

    def initialize(self) -> None:
        self.map = super().fs.memory_map()

    def execute(self) -> None:
        self.map.get_map()


class CloseFile(Statement):
    name: str

    def command(self) -> str:
        return 'close'

    def initialize(self) -> None:
        try:
            args = super().statement.split()
            self.name = args[1]
        except:
            raise InvalidStatement(self, "Invalid arguments")

        if self.name not in map(lambda x: x.name, _file_store):
            raise InvalidStatement(self, "No such file opened")

    def execute(self) -> None:
        global _file_store
        _file_store = [
            f
            for f in _file_store
            if f.name != self.name
        ]


class WriteToFile(Statement):
    src: File
    contents: str

    def command(self) -> str:
        return 'write_to_file'

    def initialize(self) -> None:
        name: str
        try:
            args = super().statement.split()[1]
            name, self.contents = args.split(',')
        except:
            raise InvalidStatement(self, "Invalid arguments")

        _f_map = {
            f.name: f
            for f in _file_store
        }
        if name not in _f_map:
            raise InvalidStatement(self, "No such file opened")

        self.src = _f_map[name]

    def execute(self) -> None:
        self.src.lock.acquire()
        self.src.write(self.contents)
        self.src.lock.release()

