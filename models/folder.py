from __future__ import annotations

from typing import List, Optional

from models import File
from models.node import Node


class Folder(Node):
    nodes: List[Node] = []

    def __init__(self, name: str, nodes: Optional[List[Node]] = None) -> None:
        super().__init__(name)
        if nodes is not None:
            self.nodes = nodes

    def create_file(self, name: str) -> None:
        pass

    def open_file(self, name: str, mode: str = 'r') -> File:
        pass

    def delete_file(self, name: str) -> None:
        pass
