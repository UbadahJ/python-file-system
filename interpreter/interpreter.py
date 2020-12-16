import sys
from typing import Type, TextIO

from interpreter.exception import InterpretationError
from interpreter.factory import *
from models import FileSystem


class Interpreter:
    fs: FileSystem
    src: TextIO
    out: TextIO
    log: bool
    statements: List[Statement]

    def __init__(self, fs: FileSystem, src: TextIO, out: TextIO = sys.stdout, log: bool = False) -> None:
        self.fs = fs
        self.src = src
        self.out = out
        self.log = log
        self.statements = []
        for i, line in enumerate(self.src.readlines(), start=1):
            try:
                if line.strip() != '':
                    self.statements.append(self.parse(line.strip()))
            except InterpretationError as e:
                print(f'Error at line {i}: Syntax error\n{e.statement}', file=self.out)
                exit(1)

    def parse(self, statement: str) -> Statement:
        factories: List[Type[Statement]] = [
            CreateFile,
            DeleteFile,
            OpenFile,
            ReadFile,
            WriteToFile,
            CloseFile,
            TruncateFile,
            MemoryMap
        ]

        for f in factories:
            if f.command == statement.split()[0]:
                return f(self.fs, statement, self.out, log=self.log)

        raise InterpretationError(statement)

    def launch(self):
        for i, s in enumerate(self.statements, start=1):
            try:
                s.execute()
            except StatementError as e:
                print(f'Error at line {i}: {e.msg}\n{e.statement.statement}', file=self.out)
                exit(1)
