from socket import socket
from typing import Optional

from exttypes import notnone
from network import network


class Connection:
    __ip: str
    __port: int
    __soc: Optional[socket]

    def __init__(self, ip: str, port: int) -> None:
        self.__ip = ip
        self.__port = port

    def __enter__(self) -> socket:
        self.__soc = network.create_connection(self.__ip, self.__port)
        return notnone(self.__soc)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__soc.close()
