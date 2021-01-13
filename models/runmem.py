from exttypes import asserttype
from models import Node


class RuntimeMemory:
    __loaded: set[Node]

    def __init__(self) -> None:
        self.__loaded = set()

    def open(self, node: Node) -> None:
        self.__loaded.add(asserttype(Node, node))

    def close(self, node: Node) -> None:
        self.__loaded.remove(asserttype(Node, node))

    def __len__(self):
        return self.__loaded.__len__()
