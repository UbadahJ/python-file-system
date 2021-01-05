from models import FileSystem
from network import network
from server.headless import Server

if __name__ == '__main__':
    _fs = FileSystem.load()
    print(network.get_local_ip())
    Server(id=1, port=5500, fs=_fs)
