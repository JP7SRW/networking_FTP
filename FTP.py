# -*- coding: utf-8 -*-
import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers
import tkinter as tk
import os
import threading
import socket
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

server_flag = False
#client_flag = False

def server_window():
    server_win = tk.Toplevel()
    server_win.title("サーバ管理ウィンドウ")
    server_win.geometry("200x100")
    server_frm = ttk.Frame(server_win)
    server_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

    ip_label = ttk.Label(server_frm, text="自IPアドレス :")
    ip_label.grid(column=0, row=0, sticky=tk.W, pady=5)
    ttk.Label(server_frm, text=ip).grid(column=1, row=0, sticky=tk.W, padx=5)

    ftp_close = ttk.Button(server_frm, text="終了", command = stop)
    ftp_close.grid(column=0, row=1, sticky=tk.W, padx=5)

def server_open():

    server_window()

    server_flag = True

    port = port_box.get()
    user = user_box.get()
    password = password_box.get()
    directory = folder_box.get()

    # 認証ユーザーを作る
    authorizer = pyftpdlib.authorizers.DummyAuthorizer()
    authorizer.add_user(user, password, directory, perm='elradfmw')

    # 個々の接続を管理するハンドラーを作る
    handler = pyftpdlib.handlers.FTPHandler
    handler.authorizer = authorizer

    # FTPサーバーを立ち上げる
    global server
    server = pyftpdlib.servers.FTPServer((ip, port), handler)
    server.serve_forever()

def client():
    pass

#FTP&プログラム終了関数
def stop():
    if server_flag == True:
        server.close_all()
    exit()

#windows側終了ボタン押下時関数
def exit_button():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        stop()

#スレッディング宣言
theread1 = threading.Thread(target=server_open)
theread1.setDaemon(True)
theread2 = threading.Thread(target=server_window)

#メインウィンドウを作成
main_win = tk.Tk()

#メインウィンドウのタイトルを変更
main_win.title("ふぁいる共有ソフト")

#メインウィンドウサイズを変更
main_win.geometry("500x400")

#テーマ設定
ttk.Style().theme_use("classic")

#メインウィンドウにノートブックを作成
nb = ttk.Notebook(main_win)

#ノートブックに関するフレームを作成
tab1 = ttk.Frame(nb)
tab2 = ttk.Frame(nb)

#ノートブックにタブを追加
nb.add(tab1, text="サーバ", padding=3)
nb.add(tab2, text="クライアント", padding=3)

#メインウィンドウにノートブックを配置
nb.pack(fill='both',expand=1)

#------以下tab1関係-------

#自IP表示
ip = socket.gethostbyname(socket.gethostname())
ip_label = ttk.Label(tab1, text="自IPアドレス :")
ip_label.grid(column=0, row=0, pady=5)
ttk.Label(tab1, text=ip).grid(column=1, row=0, sticky=tk.W, padx=5)

#ポート関係
port_label = ttk.Label(tab1, text="ポート番号 :")
port_label.grid(column=0, row=1, pady=5)

port_box = ttk.Entry(tab1)
port_box.grid(column=1, row=1, sticky=tk.W,padx=5)
port_box.insert(0, "21")

#フォルダー選択関係
def folder():
    path = filedialog.askdirectory()
    folder_path.set(path)

folder_path = tk.StringVar()
folder_label = ttk.Label(tab1, text="フォルダ指定 :")
folder_label.grid(column=0, row=2, pady=5)

folder_box = ttk.Entry(tab1, textvariable = folder_path)
folder_box.grid(column=1, row=2, sticky=tk.EW, padx=5)
folder_box.insert(0, os.path.realpath('.'))

folder_btn = ttk.Button(tab1, text="参照", command = folder)
folder_btn.grid(column=2, row=2)

#認証選択関係
def entry_on():
    user_box.configure(state=tk.DISABLED)
    password_box.configure(state=tk.DISABLED)

def entry_off():
    user_box.configure(state=tk.NORMAL)
    password_box.configure(state=tk.NORMAL)

radio_value = tk.IntVar()
AuthSelect_label = ttk.Label(tab1, text="認証 :")
AuthSelect_label.grid(column=0, row=3, padx=5)

AuthSelect_on_btn = ttk.Radiobutton(tab1, text="あり",
                                    variable=radio_value,
                                    value=0,
                                    command=entry_off)
AuthSelect_on_btn.grid(column=1, row=3, sticky=tk.W, padx=5)

AuthSelect_off_btn = ttk.Radiobutton(tab1, text="なし",
                                    variable=radio_value,
                                    value=1,
                                    command=entry_on)
AuthSelect_off_btn.grid(column=1, row=3, sticky=tk.W, padx=100)

#ユーザー選択関係
user_label = ttk.Label(tab1, text="ユーザー :")
user_label.grid(column=0, row=4, pady=10)
user_box = ttk.Entry(tab1)
user_box.grid(column=1, row=4, sticky=tk.EW, padx=5)
user_box.insert(0, "user")

#パスワード選択関係
password_label = ttk.Label(tab1, text="パスワード :")
password_label.grid(column=0, row=5, pady=10)
password_box = ttk.Entry(tab1)
password_box.grid(column=1, row=5, sticky=tk.EW, padx=5)
password_box.insert(0, "password")

#起動ボタン関係
ftp_open = ttk.Button(tab1, text="起動", command=theread1.start)
ftp_open.grid(column=1, row=6, sticky=tk.W, padx=90)

#------以上tab1関係-------

#------以下tab2関係-------



#------以上tab2関係-------

main_win.columnconfigure(0, weight=1)
main_win.rowconfigure(0, weight=1)
tab1.columnconfigure(1, weight=1)

main_win.protocol("WM_DELETE_WINDOW", exit_button)

main_win.mainloop()