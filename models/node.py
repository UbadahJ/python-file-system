from __future__ import annotations

class Node:
    name: str
    parent: Node

    def __init__(self, name: str, parent: Node) -> None:
        super().__init__()
        self.name = name
        self.parent = parent

    def path(self) -> str:
        if self.parent is None:
            return '/'

        return self.parent.path() + self.name + '/'
