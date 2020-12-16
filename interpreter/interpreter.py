import sys
from io import TextIOBase
from typing import Type

from interpreter.factory import *
from models import FileSystem


class Interpreter:
    fs: FileSystem
    src: TextIOBase
    out: TextIOBase
    threads: int
    log: bool
    statements: List[Statement]

    def __init__(self, fs: FileSystem, src: TextIOBase, out: TextIOBase = sys.stdout, log: bool = False,
                 threads: int = 4) -> None:
        self.fs = fs
        self.src = src
        self.threads = threads
        self.out = out
        self.log = log
        self.statements = [
            self.parse(line.strip())
            for line in self.src.readlines()
            if line.strip() != ''
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
                return f(self.fs, statement, self.out, log=self.log)

        raise RuntimeError(f"Interpreter error: Invalid statement {statement}")

    def launch(self):
        for s in self.statements:
            s.execute()