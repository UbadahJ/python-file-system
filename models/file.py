from typing import Union

from models.node import Node


class File(Node):
    contents: Union[bytes, str]

    def __init__(self, name: str, contents: Union[bytes, str] = "") -> None:
        super().__init__(name)
        self.contents = contents
