from __future__ import annotations

import logging
import pickle
from typing import Optional

from exttypes import asserttype, notnone
from models.folder import Folder

log = logging.getLogger('FileSystem')


class FileSystem:
    root: Folder
    current: Folder

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
        self.current = self._get_folder(path)
        return self.current

    def create_directory(self, path: str) -> None:
        log.debug(f'create_directory: path = {path}')
        name = path.rsplit('/', maxsplit=1)[-1]
        parent = self._get_parent(path)
        parent.nodes[name] = Folder(name, parent)
        self.save()

    def move_directory(self, src: str, dest: str):
        log.debug(f'move_directory: src = {src} => dest = {dest}')
        _src, _dest = self._get_folder(src), self._get_folder(dest)
        asserttype(Folder, _src.parent).nodes.pop(_src.name)
        _src.parent = _dest
        _dest.nodes[_src.name] = _src
        self.save()

    def delete_directory(self, path: str) -> None:
        folder = self._get_folder(path)
        if len(folder.nodes) == 0:
            asserttype(Folder, folder.parent).nodes.pop(folder.name)
        else:
            raise IOError('Not empty')
        self.save()

    # TODO: Return type to be decided
    def show_memory_map(self) -> bytes:
        pass

    def save(self):
        with open('fs.dat', 'wb') as f:
            pickle.dump(self, f, 3)

    def _get_folder(self, path) -> Folder:
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

        _path = path.rsplit('/', maxsplit=1)
        if path.startswith('/'):
            if path.count('/') == 1:
                return self.root

            _path[0] = '/' + _path[0]

        if len(_path) > 1:
            parent = self._get_folder(_path[0])

        return parent
