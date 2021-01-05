import pickle

from client.models.connection import Connection
from client.models.remotefile import RemoteFile
from exttypes import asserttype, Callable
from models import Folder, File
from network.network import encode_parameter, send_request, get_request


class RemoteFolder(Folder):
    conn: Callable[[], Connection]

    def __init__(self, conn: Callable[[], Connection], folder: Folder) -> None:
        super().__init__(folder.name, folder.parent, folder.nodes)
        self.conn = conn

    def create_file(self, name: str) -> None:
        with self.conn() as soc:
            send_request(soc, encode_parameter('fs', 'create_file', self.path(), name))

    def open_file(self, name: str, mode: str = 'r') -> File:
        with self.conn() as soc:
            send_request(soc, encode_parameter('fs', 'open_file', self.path(), name))
            return RemoteFile(self.conn, asserttype(File, pickle.loads(get_request(soc))))

    def delete_file(self, name: str) -> None:
        with self.conn() as soc:
            send_request(soc, encode_parameter('fs', 'delete_file', self.path(), name))
