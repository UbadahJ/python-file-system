import datetime
import pickle
from typing import Optional, Sequence

from exttypes.nullsafe import notnone
from models import FileSystem
from network import network


class Server:
    id: int
    port: int
    fs: FileSystem
    request: Optional[str] = None

    def __init__(self, *, id: int, port: int, fs: FileSystem = FileSystem.load()):
        self.id = id
        self.port = port
        self.fs = fs

        self._start()

    def _start(self):
        with network.create_server_connection(network.get_local_ip(), self.port) as soc:
            while True:
                self.request = None
                try:
                    soc.listen()
                    if soc:
                        c_soc, _ = soc.accept()
                        code = self.execute(network.decode_parameter(
                            notnone(network.get_request(c_soc))
                        ))
                        if code is not None:
                            network.send_request(c_soc, pickle.dumps(code))

                        c_soc.close()
                except (OSError, AssertionError) as e:
                    print(f"Error occurred: {e}")
                    with open('log_server.log', 'a+') as f:
                        f.write(f'[{datetime.datetime.now()}] ERROR {type(e)}: {e}\n')

    def execute(self, _params: Sequence[str]):
        _type, *params = _params
        if _type != 'fs':
            raise OSError(f"Invalid starting sequence: {_type}")

        if params[0] == 'change_directory':
            return self.fs.change_directory(params[1])
        elif params[0] == 'create_directory':
            self.fs.create_directory(params[1])
        elif params[0] == 'move':
            self.fs.move(params[1], params[2])
        elif params[0] == 'delete':
            self.fs.delete(params[1])
        elif params[0] == 'save':
            self.fs.save()
        elif params[0] == 'memory_map':
            return self.fs.memory_map()
        elif params[0] == 'root':
            return self.fs.root
        elif params[0] == 'current':
            return self.fs.current
