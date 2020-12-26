# -*- coding: utf-8 -*-
import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers
import tkinter as tk
import os
import threading
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

class Server:
    def open(self,):
        pass

class Client:
    def connect(self,):
        pass


def stop():
    exit()

def exit_button():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        stop()

def main():
    main_win = tk.Tk()
    main_win.title("ふぁいる共有ソフト")
    main_win.geometry("500x400")

    nb = ttk.Notebook(main_win)

    tab1 = ttk.Frame(nb)
    tab2 = ttk.Frame(nb)
    nb.add(tab1, text="tab1", padding=3)
    nb.add(tab2, text="tab2", padding=3)
    nb.pack(fill='both',expand=1)

    frame1 = tk.Frame(tab1,pady=10)
    frame1.pack()

    main_win.protocol("WM_DELETE_WINDOW", exit_button)

    main_win.mainloop()

if __name__ == '__main__':
    main()
