from binascii import hexlify, b2a_qp
from io import BytesIO
from typing import List, Tuple


class Memory:
    file: BytesIO
    sector: int

    def __init__(self, file: BytesIO, sector: int = 16):
        self.file = file
        self.sector = sector

    def get_map(self) -> List[Tuple[bytes, bytes]]:
        return [
            (hexlify(c, sep=' '), b2a_qp(c))
            for c in iter(lambda: self.file.read(8), b'')
        ]

    def get_formatted_string(self):
        return '\n'.join([
            f'{(i * 8):08d} :: {str(p[0])[2:len(p[0]) + 2]:32}| {str(p[1])[2:len(p[1]) + 2]:18} |'
            for i, p in enumerate(self.get_map())
        ])
