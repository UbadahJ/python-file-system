import json
import platform
import socket
import struct
import subprocess
from time import sleep
from typing import Optional, Sequence, Callable
from urllib.request import urlopen

from exttypes.nullsafe import notnone


def get_local_ip() -> str:
    """ Get the local IP address

    Uses the local address to send the packet and fetch the results using the
    socket name. On exception, return 127.0.0.1
    :return: local ip address or 127.0.0.1
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(("10.255.255.255", 1))
            ip = s.getsockname()[0]
        except Exception as e:
            ip = "127.0.0.1"
    return ip


def get_public_ip() -> str:
    """ Get the actual ip of the device

    Sends a request to external website to get the public IP of
    the machine
    :return: Public IP or empty string
    """
    try:
        return json.loads(urlopen("https://api.myip.com").read())["ip"]
    except Exception as e:
        return ""


def ping(url: str) -> bool:
    """ Ping the given URL using system level ping commands

    :param url: The url to ping
    :return: boolean indicating success status code
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", url]
    return subprocess.call(command) == 0


def check_sock(ip: str, port: int) -> bool:
    """ Verify if the socket is in use or not

    :param ip: The given IP address
    :param port: The given port
    :return: boolean indicating port availability
    """
    with socket.socket() as sock:
        try:
            sock.bind((ip, port))
        except Exception as e:
            return False
        else:
            return True


def create_server_connection(ip: str, port: int) -> socket.socket:
    """ Returns the socket with a server created on ip and port

    :param ip: The given ip to use
    :param port: The given port to use
    :return: socket being used
    """
    return socket.create_server((ip, port))


def create_connection(ip: str, port: int) -> Optional[socket.socket]:
    """ Create a connection to server on the given ip and port

    :param ip: The given ip to use
    :param port: The given socket to use
    :return: the socket connected with ip:socket or None if ConnectionRefused
    """
    soc = socket.socket()
    try:
        soc.connect((ip, port))
    except ConnectionRefusedError as e:
        return None
    return soc


def recv_bytes(
        soc: socket.socket,
        size: int,
        wait: bool = True,
        retries: int = 3,
        progress: Optional[Callable[[int, int, int], None]] = None
) -> Optional[bytearray]:
    """ Receive bytes for the socket

    This function allows the system to receive binary data from
    the given socket with the defined socket while providing updates
    using the progress callback

    Not indented to be used directly, see network.get_request

    :param soc: The socket to listen from
    :param size: The size of the data to receive
    :param wait: To retry on failure or not
    :param retries: Total number of retries
    :param progress: The callback to notify on progress changes
    :return: The received data or None on OSError
    """
    data = bytearray()
    while len(data) < size:
        packet: Optional[bytes] = None
        try:
            packet = soc.recv(size - len(data))
            if progress is not None:
                progress(len(data), size, len(packet))
        except OSError as e:
            if wait:
                retries -= 1
                sleep(0.1)
            else:
                raise e
        if packet is None or packet == b'' or retries <= 0:
            return None
        data.extend(packet)
    return data


def encode_parameter(*param: str) -> bytes:
    """ Convert the given string parameters to bytes

    :param param: Given parameters
    :return: bytes representation of the params
    """
    return "::".join(param).encode("utf-8")


def decode_parameter(param: bytes) -> Sequence[str]:
    """ Convert the given bytes to a sequence of string

    :param param: The bytes to decode
    :return: The output sequence
    """
    return param.decode("utf-8").split("::")


def get_request(soc: socket.socket,
                progress: Optional[Callable[[int, int, int], None]] = None) -> Optional[bytes]:
    """ Provides higher level call to recv_bytes with auto size management

    :param soc: The given socket to receive request from
    :param progress: The progress callback
    :return: The bytes from request or None on error
    """
    try:
        size = struct.unpack("I", notnone(recv_bytes(soc, 4)))
        return bytes(notnone(recv_bytes(soc, size[0], progress=progress)))
    except (TypeError, AssertionError):
        return None


def send_request(soc: socket.socket, param: bytes) -> None:
    """ Higher level call to send data to socket

    :param soc: The socket to send data to
    :param param: The bytes to send
    :return: None
    """
    try:
        soc.sendall(struct.pack("I", len(param)) + param)
    except OSError:
        pass
