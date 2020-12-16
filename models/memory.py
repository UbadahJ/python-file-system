from binascii import hexlify, b2a_qp
from os.path import getsize
from typing import List, Tuple


class Memory:
    file: str
    sector: int

    def __init__(self, file: str, sector: int = 16):
        self.file = file
        self.sector = sector

    def get_map(self) -> List[Tuple[bytes, bytes]]:
        _l: List[Tuple[bytes, bytes]]
        with open(self.file, 'rb') as f:
            _l = [
                (hexlify(c, sep=' '), b2a_qp(c))
                for c in iter(lambda: f.read(8), b'')
            ]

        return _l

    def get_formatted_string(self):
        return '\n'.join([
            f'{(i * 8):08d} :: {str(p[0])[2:len(p[0]) + 2]:32}| {str(p[1])[2:len(p[1]) + 2]:18} |'
            for i, p in enumerate(self.map.get_map())
        ])