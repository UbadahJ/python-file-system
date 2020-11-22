from typing import Union

from models.node import Node


class File(Node):
    contents: Union[bytes, str]

    def __init__(self, name: str, contents: Union[bytes, str] = "") -> None:
        super().__init__(name)
        self.contents = contents

    def write(self, contents: str, start: int = 0, append: bool = False) -> None:
        pass

    def read(self, start: int = 0, end: int = -1) -> None:
        pass

    def move(self, start: int, end: int, target: Any) -> None:
        # TODO: WTH does this means
        pass

    def truncate(self, end: int) -> None:
        pass
