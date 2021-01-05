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
                            print(f'=> {code}')
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

        print(*_params)

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
        elif params[0] == 'create_file':
            path, name = params[1], params[2]
            self.fs.get_folder(path).create_file(name)
        elif params[0] == 'open_file':
            path, name, mode = params[1], params[2], params[3]
            return self.fs.get_folder(path).open_file(name, mode)
        elif params[0] == 'delete_file':
            path, name = params[1], params[2]
            self.fs.get_folder(path).delete_file(name)
            self.fs.save()
        elif params[0] == 'write_contents':
            path, name, contents, start, append = params[1], params[2], params[3], int(params[4]), bool(params[5])
            self.fs.get_folder(path).open_file(name, 'rw').write(contents, start)
            self.fs.save()
        elif params[0] == 'read_contents':
            path, name, start, end = params[1], params[2], int(params[3]), int(params[4])
            return self.fs.get_folder(path).open_file(name, 'rw').read(start, end)
        elif params[0] == 'move_contents':
            path, name, start, end, target = params[1], params[2], int(params[3]), int(params[4]), int(params[5])
            self.fs.get_folder(path).open_file(name, 'rw').move(start, end, target)
            self.fs.save()
        elif params[0] == 'truncate_contents':
            path, name, end = params[1], params[2], int(params[3])
            self.fs.get_folder(path).open_file(name, 'rw').truncate(end)
            self.fs.save()
        else:
            raise OSError(f'Invalid command: {" ".join(_params)}')
