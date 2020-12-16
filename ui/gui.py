import logging
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, Optional, List, Callable

from exttypes import asserttype
from interpreter.interpreter import Interpreter
from models import FileSystem, Node, Folder, File, Memory

log = logging.getLogger('Gui')


class FileManager:
    fs: FileSystem
    root: Tk = Tk()
    menu: Menu = Menu(root)
    tree: ttk.Treeview = ttk.Treeview(root, columns=('type', 'size'))

    def __init__(self, fs: FileSystem):
        self.fs = fs
        self.init_view()
        self.root.mainloop()

    def init_view(self):
        self.root.title('FS manager')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root['menu'] = self.menu

        self.configure_tree()
        self.configure_menu()

    def configure_tree(self):
        self.tree.grid(column=0, row=0, sticky=(N, W, E, S))
        self.tree.heading('size', text='Size')
        self.tree.heading('type', text='Type')
        root = self.fs.root
        self.tree.bind('<Double-1>', self.open_notepad)
        self.tree.insert('', 'end', root.path(), text='/', tags=('root', root.path()), open=True)
        self.tree.set(root.path(), 'type', 'root')
        self._load_nodes(root, root.nodes)

    def configure_menu(self):
        self.root.option_add('*tearOff', FALSE)
        file = Menu(self.menu)
        self.menu.add_cascade(menu=file, label='File')
        file.add_command(label='New', command=self.new_file)
        file.add_command(label='New Folder', command=self.new_folder)
        file.add_command(label='Move', command=self.move)
        file.add_command(label='Delete', command=self.delete)
        file.add_separator()
        file.add_command(label='Memory map', command=self.open_memory_map)
        file.add_command(label='Interpreter', command=self.open_interpreter)
        file.add_command(label='Exit', command=lambda: exit(0))

    def open_notepad(self, event):
        item = self.tree.item(self.tree.selection()[0])
        path, name = item['tags'][1][1:len(item['tags'][1]) - 1].rsplit('/', maxsplit=1)
        log.debug(f'Opening file => {path}, {name}')
        parent = self.fs.change_directory('/' + path)
        if isinstance(parent.nodes[name], File):
            Notepad(Toplevel(self.root), self.fs, asserttype(File, parent.nodes[name]))

    def new_file(self):
        if len(self.tree.selection()) < 1:
            messagebox.showerror(title='Error', message='No file was selected')
            return

        item = self.tree.item(self.tree.selection()[0])
        name = simpledialog.askstring(title='New File', prompt='Enter new file name')
        if name is not None:
            log.debug(f'Creating file at {item["tags"][1]}: {name}')
            self.fs.change_directory(item['tags'][1]).create_file(name)
            self.fs.save()
        else:
            messagebox.showerror(title='Error', message='Invalid name entered')

        self.tree.delete(*self.tree.get_children())
        self.configure_tree()

    def new_folder(self):
        if len(self.tree.selection()) < 1:
            messagebox.showerror(title='Error', message='No folder was selected')
            return

        item = self.tree.item(self.tree.selection()[0])
        name = simpledialog.askstring(title='New Folder', prompt='Enter new folder name')
        if name is not None:
            log.debug(f'Creating folder at {item["tags"][1] + name}')
            self.fs.create_directory(item['tags'][1] + name)
        else:
            messagebox.showerror(title='Error', message='Invalid name entered')

        self.tree.delete(*self.tree.get_children())
        self.configure_tree()

    def move(self):
        if len(self.tree.selection()) < 1:
            messagebox.showerror(title='Error', message='No folder was selected')
            return

        item = self.tree.item(self.tree.selection()[0])
        path = simpledialog.askstring(title='Destination', prompt='Enter new destination')

        if path is not None:
            log.debug(f'Moving folder from {item["tags"][1]} to {path}')
            self.fs.move(item['tags'][1], path)
        else:
            messagebox.showerror(title='Error', message='Invalid path')

        self.tree.delete(*self.tree.get_children())
        self.configure_tree()

    def delete(self):
        if len(self.tree.selection()) < 1:
            messagebox.showerror(title='Error', message='No folder was selected')
            return

        item = self.tree.item(self.tree.selection()[0])
        if item["tags"][1] == '/':
            messagebox.showerror(title='Error', message="Can't delete root folder")
            return

        log.debug(f'Deleting folder at {item["tags"][1]}')
        try:
            self.fs.delete(item["tags"][1])
        except IOError as e:
            messagebox.showerror(title='Error', message=e)
            return

        self.tree.delete(*self.tree.get_children())
        self.configure_tree()

    def open_memory_map(self):
        MemoryView(Toplevel(self.root), self.fs.memory_map())

    def open_interpreter(self):
        def _clean() -> None:
            self.tree.delete(*self.tree.get_children())
            self.configure_tree()

        InterpreterView(Toplevel(self.root), self.fs, _clean)

    def _load_nodes(self, parent: Node, nodes: Dict[str, Node]):
        for _, node in nodes.items():
            log.debug(f'Inserting node {node.name} with parent {parent.name}')
            if isinstance(node, Folder):
                self.tree.insert(parent.path(), 'end', node.path(), text=node.name, tags=('folder', node.path()),
                                 open=True)
                self.tree.set(node.path(), 'type', 'folder')
                self._load_nodes(node, node.nodes)
            else:
                self.tree.insert(parent.path(), 'end', node.path(), text=node.name, tags=('file', node.path()))
                self.tree.set(node.path(), 'type', 'file')
                self.tree.set(node.path(), 'size', f'{len(asserttype(File, node).contents)} bytes')


class Notepad:
    file: File
    fs: FileSystem
    root: Toplevel
    menu: Menu
    text: Text

    def __init__(self, top: Toplevel, fs: FileSystem, file: File) -> None:
        self.fs = fs
        self.file = file
        self.root = top
        self.menu = Menu(self.root)
        self.text = Text(self.root)
        self.init_view()

    def init_view(self):
        self.root.title(f'Notepad - {self.file.name}')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root['menu'] = self.menu
        self.text.grid(column=0, row=0, sticky=(N, W, E, S))

        self.text.insert('1.0', self.file.contents)
        self.configure_menu()

    def configure_menu(self):
        self.root.option_add('*tearOff', FALSE)
        file = Menu(self.menu)
        self.menu.add_cascade(menu=file, label='File')
        file.add_command(label='Save', command=self.save_file)
        file.add_command(label='Truncate', command=self.truncate)
        file.add_command(label='Exit', command=lambda: exit(0))

    def save_file(self):
        self.file.contents = self.text.get('1.0', 'end')
        self.fs.save()

    def truncate(self):
        size = simpledialog.askinteger(title='Number of bytes', prompt='Enter number of bytes')
        if size is not None and int(size) < len(self.file.contents):
            log.debug(f'Truncating file: {self.file.name}')
            self.file.truncate(int(size))
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', self.file.contents)
        else:
            messagebox.showerror(title='Error', message='Invalid number entered')

        self.fs.save()


class MemoryView:
    memory: Memory
    root: Toplevel
    text: Text

    def __init__(self, top: Toplevel, memory: Memory) -> None:
        self.memory = memory
        self.root = top
        self.text = Text(top)

        self.init_view()

    def init_view(self):
        self.root.title(f'Memory View')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.text.grid(column=0, row=0, sticky=(N, W, E, S))

        self.text.insert('1.0', self.memory.get_formatted_string())
        self.text.config(state=DISABLED)


class InterpreterView:
    fs: FileSystem
    root: Toplevel
    text: Text
    interpreters: List[Interpreter]
    on_complete: Optional[Callable[[None], None]] = None

    def __init__(self, top: Toplevel, fs: FileSystem, on_complete: Optional[Callable[[None], None]] = None) -> None:
        self.fs = fs
        self.root = top
        self.text = Text(top)
        self.on_complete = on_complete

        contents: Optional[str] = simpledialog.askstring(
            title='Open', prompt='Enter files separated by comma\nEach file is executed in new thread'
        )
        if contents is None or contents == '':
            self.root.destroy()
            return

        files = [
            (StringIO(), open(file.strip(), 'r'))
            for file in contents.split(',')
        ]
        self.interpreters = [
            Interpreter(self.fs, file, out=io)
            for io, file in files
        ]

        self.init_view()
        self.launch_threads()

    def init_view(self) -> None:
        self.root.title(f'Interpreter')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.text.grid(column=0, row=0, sticky=(N, W, E, S))
        self.text['font'] = ("Monospace", 10, "normal")
        self.text['state'] = DISABLED

    def launch_threads(self) -> None:
        with ThreadPoolExecutor(max_workers=len(self.interpreters)) as executor:
            executor.map(lambda x: x.launch(), self.interpreters)

        self.text['state'] = NORMAL
        for index, i in enumerate(self.interpreters, start=1):
            self.text.insert('end', f'Thread {index}\n')
            i.out.seek(0)
            self.text.insert('end', f'{i.out.read()}')
            self.text.insert('end', f'End of thread {index}\n')

        self.text['state'] = DISABLED

        if self.on_complete is not None:
            self.on_complete()
