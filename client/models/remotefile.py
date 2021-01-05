from typing import Union, Callable

from client.models.connection import Connection
from models import File
from network.network import send_request, encode_parameter, get_request, decode_parameter


class RemoteFile(File):
    conn: Callable[[], Connection]

    def __init__(self, conn: Callable[[], Connection], file: File) -> None:
        super().__init__(file.name, file.parent, file.contents)
        self.conn = conn

    def write(self, contents: Union[str, bytes], start: int = 0) -> None:
        self._write(contents, start, True)

    def _write(self, contents: str, start: int = 0, append: bool = False) -> None:
        with self.conn() as soc:
            send_request(soc, encode_parameter('fs', 'write_file', self.path(), contents, str(start), str(append)))

    def read(self, start: int = 0, end: int = -1) -> Union[str, bytes]:
        with self.conn() as soc:
            send_request(soc, encode_parameter('fs', 'read_file', self.path(), str(start), str(end)))
            return ''.join(decode_parameter(get_request(soc)))

    def move(self, start: int, end: int, target: int) -> None:
        with self.conn() as soc:
            send_request(soc, encode_parameter('fs', 'move_file', self.path(), str(start), str(end), str(target)))

    def truncate(self, end: int) -> None:
        with self.conn() as soc:
            send_request(soc, encode_parameter('fs', 'write_file', self.path(), str(end)))

    def close(self):
        pass
