from models import FileSystem
from network import network
from server.headless import Server

if __name__ == '__main__':
    _fs = FileSystem.load()
    print("FS Manager Server, v0.1")
    print("Local Ip Address", network.get_local_ip())
    print("Public Ip Address", network.get_public_ip())
    print("Port", 5500)
    print("-" * 20)

    Server(id=1, port=5500, fs=_fs)
