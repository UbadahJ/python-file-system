from typing import List, Optional

from models.node import Node


class Folder(Node):
    nodes: List[Node] = []

    def __init__(self, name: str, nodes: Optional[List[Node]] = None) -> None:
        super().__init__(name)
        if nodes is not None:
            self.nodes = nodes




