from abc import ABC, abstractmethod


class Statement(ABC):
    statement: str

    def __init__(self, statement: str):
        self.statement = statement

    @abstractmethod
    def execute(self): ...