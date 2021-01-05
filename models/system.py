from __future__ import annotations

import io
import logging
import pickle
from threading import Lock
from typing import Optional

from exttypes import asserttype, notnone
from models import Node, File
from models.folder import Folder
from models.memory import Memory

log = logging.getLogger('FileSystem')


class FileSystem:
    root: Folder
    current: Folder
    lock: Lock = Lock()

    @staticmethod
    def load() -> FileSystem:
        fs: FileSystem
        try:
            with open('fs.dat', 'rb') as f:
                fs = pickle.load(f)
        except IOError:
            print('WARN: fs.dat not found')
            fs = FileSystem(Folder('root', None))
            fs.save()

        return fs

    def __init__(self, root: Folder) -> None:
        self.root = root
        self.current = root

    def change_directory(self, path: str) -> Folder:
        log.debug(f'change_directory: path = {path}')
        self.current = self.get_folder(path)
        return self.current

    def create_directory(self, path: str) -> None:
        log.debug(f'create_directory: path = {path}')
        name = path.rsplit('/', maxsplit=1)[-1]
        parent = self._get_parent(path)
        parent.nodes[name] = Folder(name, parent)
        self.save()

    def move(self, src: str, dest: str) -> None:
        log.debug(f'move_directory: src = {src} => dest = {dest}')
        _src, _dest = self._get_node(src), self.get_folder(dest)
        asserttype(Folder, _src.parent).nodes.pop(_src.name)
        _src.parent = _dest
        _dest.nodes[_src.name] = _src
        self.save()

    def delete(self, path: str) -> None:
        node = self._get_node(path)
        try:
            if isinstance(node, File) or (isinstance(node, Folder) and len(node.nodes) == 0):
                asserttype(Folder, node.parent).nodes.pop(node.name)
            else:
                raise IOError('Not empty')
        except KeyError:
            raise IOError('Not found')
        self.save()

    def save(self):
        with open('fs.dat', 'wb') as f:
            pickle.dump(self, f, 3)

    def _get_node(self, path: str) -> Node:
        return self._get_parent(path).nodes[
            [p for p in path.split('/') if p != ''][-1]
        ]

    def get_folder(self, path) -> Folder:
        def resolve_folder() -> Folder:
            return self.current if folder is None else folder

        folder: Optional[Folder] = None
        if len(path) == 0:
            log.debug(f'_get_folder: path = {path}, returning self.root')
            return self.root

        if path.startswith('/'):
            folder = self.root
            path = path[1:]

        log.debug(f'_get_folder: path = {path}, resolved = {resolve_folder().path()}')
        for node in [i for i in path.split('/') if i != '']:
            try:
                if node == '..':
                    folder = asserttype(Folder, resolve_folder().parent)
                elif node in resolve_folder().nodes:
                    folder = asserttype(Folder, resolve_folder().nodes[node])
                else:
                    raise IOError(f"{path} Not found")
            except AssertionError:
                raise IOError(f"Is File")

        return notnone(folder)

    def _get_parent(self, path: str) -> Folder:
        parent = self.root if path.startswith('/') else self.current
        log.debug(f'_get_parent: path = {path}, parent = {parent.path()}')

        if path.endswith('/'):
            path = path[:len(path) - 1]

        _path = path.rsplit('/', maxsplit=1)
        if path.startswith('/'):
            if path.count('/') == 1:
                return self.root

            _path[0] = '/' + _path[0]

        if len(_path) > 1:
            parent = self.get_folder(_path[0])

        return parent

    def memory_map(self) -> Memory:
        return Memory(io.BytesIO(pickle.dumps(self, 3)))
