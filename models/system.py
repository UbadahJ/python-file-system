from __future__ import annotations
from typing import Optional

import marshal
from models.folder import Folder
from types import asserttype, notnone


class FileSystem:
    root: Folder
    current: Folder

    @staticmethod
    def load() -> FileSystem:
        fs: FileSystem
        try:
            with open('fs.dat', 'rb') as f:
                fs = marshal.load(f)
        except IOError:
            fs = FileSystem(Folder('root', None))
            with open('fs.dat', 'wb') as f:
                marshal.dump(fs, f, 3)

        return fs

    def __init__(self, root: Folder):
        self.root = root
        self.current = root

    def change_directory(self, path: str) -> Folder:
        self.current = self._get_folder(path)
        return self.current

    def create_directory(self, path: str) -> None:
        name = path.rsplit('/', maxsplit=1)[-1]
        self._get_parent(path).nodes[name] = Folder(name, self.current)

    def move_directory(self, src: str, dest: str):
        self._get_folder(src).parent = self._get_folder(dest)

    def delete_directory(self, path: str) -> None:
        folder = self._get_folder(path)
        if len(folder.nodes) == 0:
            self._get_parent(path).nodes.pop(folder.name)

    # TODO: Return type to be decided
    def show_memory_map(self) -> bytes:
        pass

    def _get_folder(self, path) -> Folder:
        def resolve_folder() -> Folder:
            return self.current if folder is None else folder

        folder: Optional[Folder] = None
        for node in path.split('/'):
            if node == '..':
                folder = resolve_folder().parent
            elif node in self.current.nodes:
                folder = asserttype(Folder, resolve_folder().nodes[node])

            raise IOError("Is File")

        return notnone(folder)

    def _get_parent(self, path) -> Folder:
        parent = self.current
        if len(path.rsplit('/', maxsplit=1)) >= 1:
            parent = self._get_folder(path.rsplit('/', maxsplit=1)[0])

        return parent
