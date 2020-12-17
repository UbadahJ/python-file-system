from typing import List, Optional, Dict

from interpreter.exception import StatementError
from interpreter.statement import Statement, FileStatement
from models import File
from models.file import Readable, Hybrid

_file_store: List[File] = []


def _open_file(statement: Statement, name: str) -> File:
    _f_map: Dict[str, File] = {
        f.name: f
        for f in _file_store
    }
    if name not in _f_map:
        raise StatementError(statement, "No such file opened")

    return _f_map[name]


class CreateFolder(Statement):
    command: str = 'mkdir'

    def initialize(self) -> None:
        if len(self.args) != 1:
            raise StatementError(self, "Invalid name")

    def execute(self) -> None:
        self.fs.lock.acquire()
        self.pprint(f'Creating folder {self.args[0]}')
        self.fs.create_directory(self.args[0])
        self.fs.lock.release()


class DeleteFolder(Statement):
    command: str = 'rmdir'

    def initialize(self) -> None:
        if len(self.args) != 1:
            raise StatementError(self, "Invalid name")

    def execute(self) -> None:
        self.fs.lock.acquire()
        self.pprint(f'Deleting folder {self.args[0]}')
        self.fs.delete(self.args[0])
        self.fs.lock.release()


class ChangeFolder(Statement):
    command: str = 'chdir'

    def initialize(self) -> None:
        if len(self.args) != 1:
            raise StatementError(self, "Invalid name")

    def execute(self) -> None:
        self.fs.lock.acquire()
        self.pprint(f'Changed folder from {self.fs.current.name} to {self.args[0]}')
        self.fs.change_directory(self.args[0])
        self.fs.lock.release()


class Move(Statement):
    command: str = 'move'

    def initialize(self) -> None:
        if len(self.args) != 2:
            raise StatementError(self, "Invalid arguments")

    def execute(self) -> None:
        self.fs.lock.acquire()
        self.pprint(f'Moving {self.args[0]} to {self.args[1]}')
        self.fs.move(self.args[0], self.args[1])
        self.fs.lock.release()


class CreateFile(FileStatement):
    command: str = 'create'

    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        super().execute()
        self.fs.current.create_file(self.args[0])


class DeleteFile(FileStatement):
    command: str = 'delete'

    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        super().execute()
        if self.args[0] in [
            f.name
            for f in _file_store
        ]: raise StatementError(self, "File is opened")

        self.pprint(f'Deleting file {self.args[0]}')
        self.fs.current.delete_file(self.args[0])


class OpenFile(FileStatement):
    name: str
    mode: str
    command: str = 'open'

    def initialize(self) -> None:
        try:
            self.name, self.mode = self.args
        except AssertionError as e:
            raise StatementError(self, *e.args)
        except:
            raise StatementError(self, "Invalid arguments")

    def execute(self) -> None:
        super().execute()
        src = self.fs.current.open_file(self.name, self.mode)
        src.lock.acquire()
        self.pprint(f'Opening {src.name} as {type(src)}', is_log=True)
        _file_store.append(src)
        src.lock.release()


class CloseFile(FileStatement):
    name: str
    command: str = 'close'

    def initialize(self) -> None:
        try:
            self.name = self.args[0]
        except:
            raise StatementError(self, "Invalid arguments")

    def execute(self) -> None:
        super().execute()
        global _file_store
        self.pprint(f'Closing {self.name}', is_log=True)
        if self.name not in map(lambda x: x.name, _file_store):
            raise StatementError(self, "No such file opened")
        _file_store = [
            f
            for f in _file_store
            if f.name != self.name
        ]


class ReadFile(FileStatement):
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
        super().execute()
        src: File = _open_file(self, self.name)
        src.lock.acquire()
        self.pprint(f'Reading from {src.name}', is_log=True)
        if not isinstance(src, Readable) and not isinstance(src, Hybrid):
            raise StatementError(self, "File opened in write-only mode")

        self.pprint(src.read(self.start, self.size))
        src.lock.release()


class WriteToFile(FileStatement):
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
        super().execute()
        src: File = _open_file(self, self.name)
        src.lock.acquire()
        self.pprint(f'Writing to {src.name}', is_log=True)
        if isinstance(src, Readable):
            raise StatementError(self, "File opened in read-only mode")

        if self.start is not None:
            src.write(self.contents, start=self.start)
        else:
            src.write(self.contents)

        src.lock.release()


class TruncateFile(FileStatement):
    name: str
    end: int
    command: str = 'truncate'

    def initialize(self) -> None:
        try:
            self.name, self.end = self.args[0], int(self.args[1].strip())
        except:
            raise StatementError(self, "Invalid arguments")

    def execute(self) -> None:
        super().execute()
        src: File = _open_file(self, self.name)
        src.lock.acquire()
        self.pprint(f'Truncating {src.name}', is_log=True)
        src.truncate(self.end)
        src.lock.release()


class MemoryMap(FileStatement):
    command: str = 'show_memory_map'

    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        super().execute()
        _m = self.fs.memory_map().get_formatted_string()
        l = len(_m.split('\n')[0])
        self.pprint('-' * l)
        self.pprint(_m)
        self.pprint('-' * l)
