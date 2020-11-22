from models.folder import Folder


class FileSystem:
    root: Folder
    current: Folder

    def change_directory(self, path: str) -> Folder:
        pass

    def create_directory(self, path: str) -> Folder:
        pass

    def move_directory(self, src: str, dest: str):
        pass

    def delete_directory(self, path: str) -> None:
        pass

    # TODO: Return type to be decided
    def show_memory_map(self) -> bytes:
        pass
