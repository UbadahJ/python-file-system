import pickle

from client.models.connection import Connection
from client.models.remotefolder import RemoteFolder
from exttypes import asserttype, Any
from models import FileSystem, Memory, Folder
from network.network import send_request, get_request, encode_parameter


class RemoteFileSystem(FileSystem):
    ip: str
    port: int

    def __init__(self, ip: str, port: int) -> None:
        super().__init__(Folder("/", None))
        self.ip = ip
        self.port = port

    def change_directory(self, path: str) -> Folder:
        with self.__create_connection() as soc:
            send_request(soc, encode_parameter('fs', 'change_directory', path))
            return RemoteFolder(self.__create_connection, asserttype(Folder, pickle.loads(get_request(soc))))

    def create_directory(self, path: str) -> None:
        with self.__create_connection() as soc:
            send_request(soc, encode_parameter('fs', 'create_directory', path))

    def move(self, src: str, dest: str) -> None:
        with self.__create_connection() as soc:
            send_request(soc, encode_parameter('fs', 'move', src, dest))

    def delete(self, path: str) -> None:
        with self.__create_connection() as soc:
            send_request(soc, encode_parameter('fs', 'delete', path))

    def save(self):
        with self.__create_connection() as soc:
            send_request(soc, encode_parameter('fs', 'save'))

    def memory_map(self) -> Memory:
        with self.__create_connection() as soc:
            send_request(soc, encode_parameter('fs', 'memory_map'))
            return asserttype(Memory, pickle.loads(get_request(soc)))

    @property
    def root(self):
        with self.__create_connection() as soc:
            send_request(soc, encode_parameter('fs', 'root'))
            return RemoteFolder(self.__create_connection, asserttype(Folder, pickle.loads(get_request(soc))))

    @root.setter
    def root(self, _: Any): pass

    @property
    def current(self):
        with self.__create_connection() as soc:
            send_request(soc, encode_parameter('fs', 'current'))
            return RemoteFolder(self.__create_connection, asserttype(Folder, pickle.loads(get_request(soc))))

    @current.setter
    def current(self, _: Any): pass

    def __create_connection(self) -> Connection:
        return Connection(self.ip, self.port)
