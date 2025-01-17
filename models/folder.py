from __future__ import annotations

from typing import Optional, Dict

from exttypes import asserttype
from models.file import File, Readable, Writeable, Appendable, Hybrid
from models.node import Node


class Folder(Node):
    nodes: Dict[str, Node]

    def __init__(self, name: str, parent: Optional[Folder], nodes: Optional[Dict[str, Node]] = None) -> None:
        super().__init__(name, parent)
        if nodes is None:
            nodes = {}

        self.nodes = nodes

    def create_file(self, name: str) -> None:
        self.nodes[name] = File(name, self)

    def open_file(self, name: str, mode: str = 'r') -> File:
        try:
            if mode == 'r':
                if name in self.nodes:
                    return Readable(asserttype(File, self.nodes[name]))

                raise IOError("No such file")

            if name not in self.nodes:
                self.create_file(name)

            if mode == 'w':
                return Writeable(asserttype(File, self.nodes[name]))
            elif mode == 'a':
                return Appendable(Writeable(asserttype(File, self.nodes[name])))
            elif mode == 'rw':
                return Hybrid(asserttype(File, self.nodes[name]))
            elif mode == 'ra':
                return Appendable(Hybrid(asserttype(File, self.nodes[name])))
        except AssertionError:
            raise IOError("Is directory")

    def delete_file(self, name: str) -> None:
        self.nodes.pop(name)
