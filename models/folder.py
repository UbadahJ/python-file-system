from __future__ import annotations

from typing import Optional, Dict

from models import File
from models.file import Readable, Writeable, Appendable
from models.node import Node
from exttypes import asserttype


class Folder(Node):
    parent: Folder
    nodes: Dict[str, Node]

    def __init__(self, name: str, parent: Optional[Folder], nodes: Optional[Dict[str, Node]] = None) -> None:
        super().__init__(name)
        self.parent = parent
        if nodes is None:
            nodes = {}

        self.nodes = nodes

    def create_file(self, name: str) -> None:
        self.nodes[name] = File(name)

    def open_file(self, name: str, mode: str = 'r') -> File:
        try:
            if name in self.nodes:
                if mode == 'r':
                    return Readable(asserttype(File, self.nodes[name]))
                elif mode == 'w':
                    return Writeable(asserttype(File, self.nodes[name]))
                elif mode == 'a':
                    return Appendable(Writeable(asserttype(File, self.nodes[name])))
                elif mode == 'rw':
                    return asserttype(File, self.nodes[name])
                elif mode == 'ra':
                    return Appendable(asserttype(File, self.nodes[name]))
        except AssertionError:
            raise IOError("Is directory")

    def delete_file(self, name: str) -> None:
        self.nodes.pop(name)
