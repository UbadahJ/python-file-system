from __future__ import annotations

from threading import Lock


class Node:
    name: str
    parent: Node
    lock: Lock = Lock()

    def __init__(self, name: str, parent: Node) -> None:
        super().__init__()
        self.name = name
        self.parent = parent

    def path(self) -> str:
        if self.parent is None:
            return '/'

        return self.parent.path() + self.name + '/'
