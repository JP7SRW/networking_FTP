# -*- coding: utf8 -*-
import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers
import tkinter
import socket
import os
import threading
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import disp_serverinfo

# メインウィンドウ
main_win = tkinter.Tk()
main_win.title("FTPサーバの起動")
main_win.geometry("500x230")

# メインフレーム
main_frm = ttk.Frame(main_win)
main_frm.grid(column=0, row=0, sticky=tkinter.NSEW, padx=5, pady=10)

def open():
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
    server = pyftpdlib.servers.FTPServer(("127.0.0.1", port), handler)
    server.serve_forever()

def folder():
    path = filedialog.askdirectory()
    folder_path.set(path)

def stop():
    server.close_all()
    exit()

def disp(): # サーバ接続情報確認ホップアップ
    ip = socket.gethostbyname(socket.gethostname())
    disp_serverinfo.main(ip,port_box.get(),user_box.get(),password_box.get())

def exit_button(): # ×ボタンが押下された際の終了処理
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        main_win.destroy()
        stop()

thread1 = threading.Thread(target=open)

folder_path = tkinter.StringVar()

# ウィジェット作成（フォルダパス）
folder_label = ttk.Label(main_frm, text="フォルダ指定")
folder_box = ttk.Entry(main_frm, textvariable = folder_path)
folder_btn = ttk.Button(main_frm, text="参照", command = folder)

# ウィジェット作成(ポート番号)
port_label = ttk.Label(main_frm, text="ポート番号")
port_box = ttk.Entry(main_frm)

# ウィジェット作成(ユーザー)
user_label = ttk.Label(main_frm, text="ユーザー")
user_box = ttk.Entry(main_frm)

# ウィジェット作成(パスワード)
password_label = ttk.Label(main_frm, text="パスワード")
password_box = ttk.Entry(main_frm)

# ウィジェット作成（実行ボタン）
ftp_open = ttk.Button(main_frm, text="起動", command = thread1.start)
ftp_close = ttk.Button(main_frm, text="終了", command = stop)
disp_info = ttk.Button(main_frm, text="接続情報表示", command = disp)

# ウィジェットの配置
folder_label.grid(column=0, row=0, pady=10)
folder_box.grid(column=1, row=0, sticky=tkinter.EW, padx=5)
folder_btn.grid(column=2, row=0)
folder_box.insert(0, os.path.realpath('.'))

port_label.grid(column=0, row=1, pady=10)
port_box.grid(column=1, row=1, sticky=tkinter.EW, padx=5)
port_box.insert(0, "21")

user_label.grid(column=0, row=2, pady=10)
user_box.grid(column=1, row=2, sticky=tkinter.EW, padx=5)
user_box.insert(0, "user")

password_label.grid(column=0, row=3, pady=10)
password_box.grid(column=1, row=3, sticky=tkinter.EW, padx=5)
password_box.insert(0, "password")

ftp_open.grid(column=1, row=4, sticky=tkinter.W, padx=90)
ftp_close.grid(column=1, row=4, sticky=tkinter.E, padx=90)
disp_info.grid(column=1, row=5, sticky=tkinter.S, padx=90)

# 配置設定
main_win.columnconfigure(0, weight=1)
main_win.rowconfigure(0, weight=1)
main_frm.columnconfigure(1, weight=1)
main_win.protocol("WM_DELETE_WINDOW", exit_button)
main_win.mainloop()
