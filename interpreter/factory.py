from typing import List, Optional

from interpreter.exception import StatementError
from interpreter.statement import Statement
from models import File
from models.file import Readable, Hybrid

_file_store: List[File] = []


class CreateFile(Statement):
    command: str = 'create'

    def initialize(self) -> None:
        self.fs.current.create_file(self.args[0])

    def execute(self) -> None:
        pass


class DeleteFile(Statement):
    command: str = 'delete'

    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        if self.args[0] in [
            f.name
            for f in _file_store
        ]: raise StatementError(self, "File is opened")

        self.fs.current.delete_file(self.args[0])


class OpenFile(Statement):
    src: File
    command: str = 'open'

    def initialize(self) -> None:
        try:
            self.src = self.fs.current.open_file(*self.args)
        except AssertionError as e:
            raise StatementError(self, *e.args)
        except:
            raise StatementError(self, "Invalid arguments")

    def execute(self) -> None:
        self.src.lock.acquire()
        self.pprint(f'Opening {self.src.name} as {type(self.src)}', is_log=True)
        _file_store.append(self.src)
        self.src.lock.release()


class CloseFile(Statement):
    name: str
    command: str = 'close'

    def initialize(self) -> None:
        try:
            self.name = self.args[0]
        except:
            raise StatementError(self, "Invalid arguments")

    def execute(self) -> None:
        global _file_store
        self.pprint(f'Closing {self.name}', is_log=True)
        if self.name not in map(lambda x: x.name, _file_store):
            raise StatementError(self, "No such file opened")
        _file_store = [
            f
            for f in _file_store
            if f.name != self.name
        ]


class ReadFile(Statement):
    name: str
    start: int = 0
    size: int = -1
    command: str = 'read_from_file'

    def initialize(self) -> None:
        try:
            self.name = self.args[0]
            if len(self.args) > 1:
                self.start = int(self.args[1])
            if len(self.args) > 2:
                self.size = int(self.args[2])
        except:
            raise StatementError(self, "Invalid arguments")

    def execute(self) -> None:
        _f_map = {
            f.name: f
            for f in _file_store
        }
        if self.name not in _f_map:
            raise StatementError(self, "No such file opened")

        src = _f_map[self.name]

        src.lock.acquire()
        self.pprint(f'Reading from {src.name}', is_log=True)
        if not isinstance(src, Readable) and not isinstance(src, Hybrid):
            raise StatementError(self, "File opened in write-only mode")

        self.pprint(src.read(self.start, self.size))
        src.lock.release()


class WriteToFile(Statement):
    name: str
    contents: str
    start: Optional[int] = None
    command: str = 'write_to_file'

    def initialize(self) -> None:
        try:
            self.name, self.contents = self.args[0], self.args[1].strip('"').strip()
            if len(self.args) > 2:
                self.start = int(self.args[2])
        except:
            raise StatementError(self, "Invalid arguments")

    def execute(self) -> None:
        _f_map = {
            f.name: f
            for f in _file_store
        }
        if self.name not in _f_map:
            raise StatementError(self, "No such file opened")

        src = _f_map[self.name]

        src.lock.acquire()
        self.pprint(f'Writing to {src.name}', is_log=True)
        if isinstance(src, Readable):
            raise StatementError(self, "File opened in read-only mode")

        if self.start is not None:
            src.write(self.contents, start=self.start)
        else:
            src.write(self.contents)

        src.lock.release()


class TruncateFile(Statement):
    name: str
    end: int
    command: str = 'truncate'

    def initialize(self) -> None:
        try:
            self.name, self.end = self.args[0], int(self.args[1].strip())
        except:
            raise StatementError(self, "Invalid arguments")

    def execute(self) -> None:
        _f_map = {
            f.name: f
            for f in _file_store
        }
        if self.name not in _f_map:
            raise StatementError(self, "No such file opened")

        src: File = _f_map[self.name]

        src.lock.acquire()
        self.pprint(f'Writing to {src.name}', is_log=True)
        src.truncate(self.end)
        src.lock.release()


class MemoryMap(Statement):
    command: str = 'show_memory_map'

    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        _m = self.fs.memory_map().get_formatted_string()
        l = len(_m.split('\n')[0])
        self.pprint('-' * l)
        self.pprint(_m)
        self.pprint('-' * l)
