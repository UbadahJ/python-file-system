from typing import Type

from models import FileSystem
from factory import *


class Interpreter:
    fs: FileSystem
    src: str
    threads: int
    statements: List[Statement]

    def __init__(self, fs: FileSystem, src: str, threads: int = 4):
        self.fs = fs
        self.src = src
        self.threads = threads
        with open(self.src) as f:
            self.statements = [
                self.parse(line.strip())
                for line in f.readlines()
            ]

    def parse(self, statement: str) -> Statement:
        factories: List[Type[Statement]] = [
            OpenFile,
            WriteToFile,
            CloseFile,
            MemoryMap
        ]

        for f in factories:
            if f.command == statement.split()[0]:
                return f(self.fs, statement)

        raise RuntimeError(f"Interpreter error: Invalid statement {statement}")
