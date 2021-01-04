from socket import socket
from typing import Union

from models import File
from network.network import send_request, encode_parameter, get_request, decode_parameter


class RemoteFile(File):
    soc: socket

    def __init__(self, soc: socket, file: File) -> None:
        super().__init__(file.name, file.parent, file.contents)
        self.soc = soc

    def write(self, contents: Union[str, bytes], start: int = 0) -> None:
        self._write(contents, start, True)

    def _write(self, contents: str, start: int = 0, append: bool = False) -> None:
        send_request(self.soc, encode_parameter('fs', 'write_file', self.path(), contents, str(start), str(append)))

    def read(self, start: int = 0, end: int = -1) -> Union[str, bytes]:
        send_request(self.soc, encode_parameter('fs', 'read_file', self.path(), str(start), str(end)))
        return ''.join(decode_parameter(get_request(self.soc)))

    def move(self, start: int, end: int, target: int) -> None:
        send_request(self.soc, encode_parameter('fs', 'move_file', self.path(), str(start), str(end), str(target)))

    def truncate(self, end: int) -> None:
        send_request(self.soc, encode_parameter('fs', 'write_file', self.path(), str(end)))

    def close(self):
        pass
