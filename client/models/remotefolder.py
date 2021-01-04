import pickle
from socket import socket

from client.models.remotefile import RemoteFile
from exttypes import asserttype
from models import Folder, File
from network.network import encode_parameter, send_request, get_request


class RemoteFolder(Folder):
    soc: socket

    def __init__(self, soc: socket, folder: Folder) -> None:
        super().__init__(folder.name, asserttype(Folder, folder.parent), folder.nodes)
        self.soc = soc

    def create_file(self, name: str) -> None:
        send_request(self.soc, encode_parameter('fs', 'create_file', self.path(), name))

    def open_file(self, name: str, mode: str = 'r') -> File:
        send_request(self.soc, encode_parameter('fs', 'open_file', self.path(), name))
        return RemoteFile(self.soc, asserttype(File, pickle.loads(get_request(self.soc))))

    def delete_file(self, name: str) -> None:
        send_request(self.soc, encode_parameter('fs', 'delete_file', self.path(), name))
