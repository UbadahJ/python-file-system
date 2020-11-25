import logging
from tkinter import *
from tkinter import ttk
from typing import Dict

from models import FileSystem, Node, Folder

log = logging.getLogger('Gui')


class Gui:
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

        self.tree.grid(column=0, row=0, sticky=(N, W, E, S))
        self.tree.heading('size', text='Size')
        self.tree.heading('type', text='Type')
        self.tree.insert('', 'end', self.fs.root.name, text='/')
        self.tree.set(self.fs.root.name, 'type', 'root')
        self._load_nodes(self.fs.root, self.fs.root.nodes)
        self.configure_menu()

    def configure_menu(self):
        self.root.option_add('*tearOff', FALSE)
        file = Menu(self.menu)
        self.menu.add_cascade(menu=file, label='File')
        file.add_command(label='New')
        file.add_command(label='New Folder')
        file.add_command(label='Move')
        file.add_command(label='Delete')
        file.add_command(label='Exit', command=lambda: exit(0))

    def _load_nodes(self, parent: Node, nodes: Dict[str, Node]):
        for _, node in nodes.items():
            log.debug(f'Inserting node {node.name} with parent {parent.name}')
            if isinstance(node, Folder):
                self.tree.insert(parent.name, 'end', node.name, text=node.name, tags=('folder',))
                self.tree.set(node.name, 'type', 'folder')
                self._load_nodes(node, node.nodes)
            else:
                self.tree.insert(parent.name, 'end', node.name, text=node.name, tags=('file',))
                self.tree.set(node.name, 'type', 'file')