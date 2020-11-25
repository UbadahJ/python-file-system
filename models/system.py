from __future__ import annotations

import pickle
from typing import Optional

from exttypes import asserttype, notnone
from models.folder import Folder


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
        self.current = self._get_folder(path)
        return self.current

    def create_directory(self, path: str) -> None:
        name = path.rsplit('/', maxsplit=1)[-1]
        self._get_parent(path).nodes[name] = Folder(name, self.current)
        self.save()

    def move_directory(self, src: str, dest: str):
        self._get_folder(src).parent = self._get_folder(dest)
        self.save()

    def delete_directory(self, path: str) -> None:
        folder = self._get_folder(path)
        if len(folder.nodes) == 0:
            self._get_parent(path).nodes.pop(folder.name)

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
        for node in path.split('/'):
            if node == '..':
                folder = resolve_folder().parent
            elif node in self.current.nodes:
                folder = asserttype(Folder, resolve_folder().nodes[node])
            else:
                raise IOError("Is File")

        return notnone(folder)

    def _get_parent(self, path) -> Folder:
        parent = self.current
        if len(path.rsplit('/', maxsplit=1)) > 1:
            parent = self._get_folder(path.rsplit('/', maxsplit=1)[0])

        return parent
