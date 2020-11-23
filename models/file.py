from io import UnsupportedOperation
from typing import Union, Any

from models.node import Node


class File(Node):
    contents: Union[bytes, str]

    def __init__(self, name: str, contents: Union[bytes, str] = "") -> None:
        super().__init__(name)
        self.contents = contents

    def write(self, contents: str, start: int = 0) -> None:
        self._write(contents, start)

    def _write(self, contents: str, start: int = 0, append: bool = False) -> None:
        pass

    def read(self, start: int = 0, end: int = -1) -> None:
        pass

    def move(self, start: int, end: int, target: Any) -> None:
        # TODO: WTH does this means
        pass

    def truncate(self, end: int) -> None:
        pass


class ReadableFile(File):
    file: File

    def __init__(self, file: File):
        super().__init__(file.name, file.contents)
        self.file = file

    def read(self, start: int = 0, end: int = -1) -> None:
        super().read(start, end)

    def write(self, contents: str, start: int = 0, append: bool = False) -> None:
        raise UnsupportedOperation("Not writable")

    def move(self, start: int, end: int, target: Any) -> None:
        raise UnsupportedOperation("Not writable")

    def truncate(self, end: int) -> None:
        raise UnsupportedOperation("Not writable")


class Writeable(File):
    file: File

    def __init__(self, file: File):
        super().__init__(file.name, file.contents)
        self.file = file

    def write(self, contents: str, start: int = 0) -> None:
        self.file._write(contents, start, True)

    def read(self, start: int = 0, end: int = -1) -> None:
        raise UnsupportedOperation("Not readable")

    def move(self, start: int, end: int, target: Any) -> None:
        self.file.move(start, end, target)

    def truncate(self, end: int) -> None:
        self.file.truncate(end)


class Appendable(File):
    file: File

    def __init__(self, file: File):
        super().__init__(file.name, file.contents)
        self.file = file

    def write(self, contents: str, start: int = 0) -> None:
        self.file._write(contents, start, True)

    def read(self, start: int = 0, end: int = -1) -> None:
        raise UnsupportedOperation("Not readable")

    def move(self, start: int, end: int, target: Any) -> None:
        self.file.move(start, end, target)

    def truncate(self, end: int) -> None:
        self.file.truncate(end)


