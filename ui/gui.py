import logging
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
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

        self.configure_tree()
        self.configure_menu()

    def configure_tree(self):
        self.tree.grid(column=0, row=0, sticky=(N, W, E, S))
        self.tree.heading('size', text='Size')
        self.tree.heading('type', text='Type')
        root = self.fs.root
        self.tree.insert('', 'end', root.path(), text='/', tags=('root', root.path()), open=True)
        self.tree.set(root.path(), 'type', 'root')
        self._load_nodes(root, root.nodes)

    def configure_menu(self):
        self.root.option_add('*tearOff', FALSE)
        file = Menu(self.menu)
        self.menu.add_cascade(menu=file, label='File')
        file.add_command(label='New')
        file.add_command(label='New Folder', command=self.new_folder)
        file.add_command(label='Move')
        file.add_command(label='Delete')
        file.add_command(label='Exit', command=lambda: exit(0))

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

    def _load_nodes(self, parent: Node, nodes: Dict[str, Node]):
        for _, node in nodes.items():
            log.debug(f'Inserting node {node.name} with parent {parent.name}')
            if isinstance(node, Folder):
                self.tree.insert(parent.path(), 'end', node.path(), text=node.name, tags=('folder', node.path()), open=True)
                self.tree.set(node.path(), 'type', 'folder')
                self._load_nodes(node, node.nodes)
            else:
                self.tree.insert(parent.path(), 'end', node.path(), text=node.name, tags=('file',))
                self.tree.set(node.path(), 'type', 'file')
