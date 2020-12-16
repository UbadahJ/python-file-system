from interpreter.statement import Statement


class StatementError(SyntaxError):
    statement: Statement

    def __init__(self, statement: Statement, *args: object) -> None:
        super().__init__(*args)
        self.statement = statement

    def __repr__(self) -> str:
        return f"Failed to parse {self.statement.statement}: {super().__repr__()}"


class InterpretionError(SyntaxError):
    statstrement: str

    def __init__(self, statement: str, *args: object) -> None:
        super().__init__(*args)
        self.statement = statement

    def __repr__(self) -> str:
        return f"Failed to parse {self.statement}: {super().__repr__()}"
