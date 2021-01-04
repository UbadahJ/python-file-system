import pickle
from socket import socket

from client.models.remotefolder import RemoteFolder
from exttypes import asserttype
from models import FileSystem, Memory, Folder
from network.network import send_request, get_request, encode_parameter


class RemoteFileSystem(FileSystem):
    soc: socket

    def __init__(self, soc: socket) -> None:
        super().__init__(Folder("/", None))
        self.soc = soc

    def change_directory(self, path: str) -> Folder:
        send_request(self.soc, encode_parameter('fs', 'change_directory', path))
        return RemoteFolder(self.soc, asserttype(Folder, pickle.loads(get_request(self.soc))))

    def create_directory(self, path: str) -> None:
        send_request(self.soc, encode_parameter('fs', 'create_directory', path))

    def move(self, src: str, dest: str) -> None:
        send_request(self.soc, encode_parameter('fs', 'move', src, dest))

    def delete(self, path: str) -> None:
        send_request(self.soc, encode_parameter('fs', 'delete', path))

    def save(self):
        send_request(self.soc, encode_parameter('fs', 'save'))

    def memory_map(self) -> Memory:
        send_request(self.soc, encode_parameter('fs', 'memory_map'))
        return asserttype(Memory, pickle.loads(get_request(self.soc)))
