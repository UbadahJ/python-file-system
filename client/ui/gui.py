import sys
from tkinter import Tk, Entry, Button, Label, N, W, E, messagebox, S
from traceback import print_exception

from client.models.remotesystem import RemoteFileSystem
from models.auth import Authentication
from services.authservice import AuthService
from ui.gui import FileManager


class ClientConfig:
    root: Tk = Tk()
    ip_entry: Entry
    port_entry: Entry
    name_entry: Entry
    launch_btn: Button

    def __init__(self) -> None:
        self.ip_entry = Entry(self.root)
        self.port_entry = Entry(self.root)
        self.name_entry = Entry(self.root)
        self.launch_btn = Button(self.root, text='Launch', command=self.launch)

        self.init_view()
        self.root.mainloop()

    def init_view(self) -> None:
        self.root.title('Client configuration')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        Label(self.root, text="Enter the configuration for the fields").grid(column=0, columnspan=2, row=0,
                                                                             sticky=(N, W, E, S))
        Label(self.root, text="IP Address").grid(column=0, row=1, sticky=(N, W))
        self.ip_entry.grid(column=1, row=1, sticky=(N, W, E, S))
        Label(self.root, text="Port number").grid(column=0, row=2, sticky=(N, W))
        self.port_entry.grid(column=1, row=2, sticky=(N, W, E, S))
        Label(self.root, text="Client name").grid(column=0, row=3, sticky=(N, W))
        self.name_entry.grid(column=1, row=3, sticky=(N, W, E, S))
        self.launch_btn.grid(column=0, columnspan=2, row=4, sticky=(N, W, E, S))

    def launch(self) -> None:
        if self.verify():
            ip = self.ip_entry.get()
            port = int(self.port_entry.get())
            name = self.name_entry.get()
            self.root.destroy()
            try:
                AuthService.init(Authentication(name))
                FileManager(RemoteFileSystem(ip, port))
            except Exception as e:
                print_exception(e, Exception, sys.stderr)
                messagebox.showerror('Failed to connect', e)

    def verify(self) -> bool:
        if self.ip_entry.get() == '':
            return False
        elif self.port_entry.get() == '':
            return False
        else:
            try:
                port = int(self.port_entry.get())
            except:
                return False

        return True
