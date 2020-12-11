# -*- coding: utf8 -*-
import ftplib
import tkinter
import os
import threading
from ftplib import FTP
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

# メインウィンドウ
main_win = tkinter.Tk()
main_win.title("FTPクライアント")
main_win.geometry("500x200")

# メインフレーム
main_frm = ttk.Frame(main_win)
main_frm.grid(column=0, row=0, sticky=tkinter.NSEW, padx=5, pady=10)

def connect():
    host = host_box.get()
    port = port_box.get()
    user = user_box.get()
    password = password_box.get()

    # FTPオブジェクトをインスタンス化
    ftp = FTP()

    # FTPサーバに接続
    ftp.connect(host, port)
    #FTPサーバにログイン
    ftp.login(user, password)
    # FTPサーバのファイル一覧を取得
    files = ftp.nlst("/dir")

def stop():
    

# ウィジェット作成(ホスト)
host_label = ttk.Label(main_frm, text="ホスト")
host_box = ttk.Entry(main_frm)

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
ftp_connect = ttk.Button(main_frm, text="接続", command = connect)
ftp_close = ttk.Button(main_frm, text="終了", command = stop)

# ウィジェットの配置
host_label.grid(column=0, row=0, pady=10)
host_box.grid(column=1, row=0, sticky=tkinter.EW, padx=5)
host_box.insert(0, "127.0.0.1")

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

# 配置設定
main_win.columnconfigure(0, weight=1)
main_win.rowconfigure(0, weight=1)
main_frm.columnconfigure(1, weight=1)

main_win.mainloop()
