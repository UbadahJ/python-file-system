from typing import List

from interpreter.exception import InvalidStatement
from interpreter.statement import Statement
from models import Memory, File

_file_store: List[File] = []


class OpenFile(Statement):
    src: File
    command: str = 'open'

    def initialize(self) -> None:
        try:
            args = self.statement.split()[1]
            self.src = self.fs.current.open_file(*args.split(','))
        except AssertionError as e:
            raise InvalidStatement(self, *e.args)
        except:
            raise InvalidStatement(self, "Invalid arguments")

    def execute(self) -> None:
        self.src.lock.acquire()
        self.pprint(f'Opening {self.src.name} as {type(self.src)}', is_log=True)
        _file_store.append(self.src)
        self.src.lock.release()


class MemoryMap(Statement):
    map: Memory
    command: str = 'show_memory_map'

    def initialize(self) -> None:
        self.map = self.fs.memory_map()

    def execute(self) -> None:
        self.pprint(self.map.get_formatted_string())


class CloseFile(Statement):
    name: str
    command: str = 'close'

    def initialize(self) -> None:
        try:
            args = self.statement.split()
            self.name = args[1]
        except:
            raise InvalidStatement(self, "Invalid arguments")

    def execute(self) -> None:
        global _file_store
        self.pprint(f'Closing {self.name}', is_log=True)
        if self.name not in map(lambda x: x.name, _file_store):
            raise InvalidStatement(self, "No such file opened")
        _file_store = [
            f
            for f in _file_store
            if f.name != self.name
        ]


class WriteToFile(Statement):
    name: str
    contents: str
    command: str = 'write_to_file'

    def initialize(self) -> None:
        try:
            args = self.statement.split(maxsplit=1)[1]
            self.name, self.contents = args.split(',', maxsplit=1)
        except:
            raise InvalidStatement(self, "Invalid arguments")

    def execute(self) -> None:
        _f_map = {
            f.name: f
            for f in _file_store
        }
        if self.name not in _f_map:
            raise InvalidStatement(self, "No such file opened")

        src = _f_map[self.name]

        src.lock.acquire()
        self.pprint(f'Writing to {src.name}', is_log=True)
        src.write(self.contents)
        src.lock.release()

