from tkinter import *
from tkinter import ttk
from typing import List, Dict

from models import FileSystem, Node, Folder


class Gui:
    fs: FileSystem
    root: Tk = Tk()
    tree: ttk.Treeview = ttk.Treeview(root)

    def __init__(self, fs: FileSystem):
        self.fs = fs
        self.init_view()
        self.root.mainloop()

    def init_view(self):
        self.root.title('FS manager')
        self.tree.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.tree.insert('', 'end', self.fs.root.name, text='/')
        self._load_nodes(self.fs.root, self.fs.root.nodes)

    def _load_nodes(self, parent: Node, nodes: Dict[str, Node]):
        for _, node in nodes:
            self.tree.insert(parent.name, 'end', node.name, text=node.name)
            if isinstance(node, Folder):
                self._load_nodes(node, node.nodes)
