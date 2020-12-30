# -*- coding: utf-8 -*-
import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers
import tkinter as tk
import ftplib
import os
import threading
import socket
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from ftplib import FTP

server_flag = False
client_flag = False

#サーバ起動時のウィンドウ起動関数
def server_window():

    #main_winの子ウィンドウとしてserver_winを作�??
    server_win = tk.Toplevel()

    #サーバウィンドウのタイトルを変更
    server_win.title("サーバ管�?ウィンドウ")

    #サーバウィンドウのサイズを変更
    server_win.geometry("200x100")

    #ウィンドウアイコンの設�?
    server_win.iconbitmap("soft_ico.ico")

    #サーバウィンドウにフレー�?を作�?��?�配置
    server_frm = ttk.Frame(server_win)
    server_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

    #自IP表示
    ip = combo.get()
    ip_label = ttk.Label(server_frm, text="自IPアドレス :")
    ip_label.grid(column=0, row=0, sticky=tk.W, pady=5)
    ip_label_s = ttk.Label(server_frm, text="自IPアドレス :")
    ip_label_s.grid(column=0, row=0, sticky=tk.W, pady=5)
    ttk.Label(server_frm, text=ip).grid(column=1, row=0, sticky=tk.W, padx=5)

    #終�?ボタン作�?��?�配置
    ftp_close = ttk.Button(server_frm, text="終�?", command = stop)
    ftp_close.grid(column=0, row=1, sticky=tk.W, padx=5)

    #windows側終�?ボタン押下時関数呼び出�?
    server_win.protocol("WM_DELETE_WINDOW", exit_button)

#サーバ起動関数
def server_open():

    server_window()

    global server_flag
    server_flag = True

    ip = combo.get()
<<<<<<< HEAD
    port = port_box.get()
    user = user_box.get()
    password = password_box.get()
    directory = folder_box.get()
=======
    port = port_box_s.get()
    user = user_box_s.get()
    password = password_box_s.get()
    directory = folder_box_s.get()
>>>>>>> ad1828d56da7950dbab737e8c438c1d00c103141

    # 認証ユーザーを作る
    authorizer = pyftpdlib.authorizers.DummyAuthorizer()

    if radio_value.get() == 0:
        #TODO : 権限をrのみに変える�?要有?(現状は何でも�?�来てしま�?)
        authorizer.add_user(user, password, directory, perm="elradfmw")
    elif radio_value.get() == 1:
        #anonymous認証�?
        authorizer.add_anonymous(directory, perm="elradfmw")

    # 個�?の接続を管�?するハンドラーを作る
    handler = pyftpdlib.handlers.FTPHandler
    handler.authorizer = authorizer

    # FTPサーバ�?�を立ち上げ�?
    global server
    server = pyftpdlib.servers.FTPServer((ip, port), handler)
    server.serve_forever()


#クライアント起動時のウィンドウ起動関数
def client_window():

    client_win = tk.Toplevel()

    #サーバウィンドウのタイトルを変更
    client_win.title("クライアント管�?ウィンドウ")

    #サーバウィンドウのサイズを変更
    client_win.geometry("300x200")

    #ウィンドウアイコンの設�?
    client_win.iconbitmap("soft_ico.ico")

    #サーバウィンドウにフレー�?を作�?��?�配置
    client_frm = ttk.Frame(client_win)
    client_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

    def select_lb(event):
        for i in lb.curselection():
            print(str(i)+"番目を選択中")
        print("")

    #サーバ�?�のファイルの一覧取�?
    files = ftp.nlst(".")
    txt = tk.StringVar(value=files)
    lb = tk.Listbox(client_frm, listvariable=txt, width=30, height=6)
    lb.bind("<<ListboxSelect>>", select_lb)
    lb.grid(column=0, row=0)
    lb.configure(selectmode="extended")

    #スクロールバ�?�の作�?��?�配置
    scrollbar = ttk.Scrollbar(client_frm,orient=tk.VERTICAL,command=lb.yview)
    scrollbar.grid(column=1, row=0, sticky=tk.NS)

    #終�?ボタンの作�?��?�配置
    ftp_close = ttk.Button(client_frm, text="終�?", command = stop)
    ftp_close.grid(column=0, row=1, sticky=tk.W, padx=5)

    #windows側終�?ボタン押下時関数呼び出�?
    client_win.protocol("WM_DELETE_WINDOW", exit_button)


#クライアント起動関数
def client_connect():

    ip = ip_box_c.get()
    #TODO: 何故かport�?けintにキャストしな�?とエラーにな�?
    port = int(port_box_c.get())
    user = user_box_c.get()
    password = password_box_c.get()

    #FTPオブジェクト�?�インスタンス�?
    global ftp
    ftp = FTP()

    #FTPサーバにログイン
    ftp.connect(ip,port)
    ftp.login(user,password)

    client_window()

#FTP&プログラ�?終�?関数
def stop():
    if (server_flag):
        server.close_all()
    if (client_flag):
        ftp.close()
    exit()

#windows側終�?ボタン押下時関数
def exit_button():
    if messagebox.askokcancel("確�?","プログラ�?を終�?してもい�?ですか?��\
                                \nFTPで通信中の場合�?通信も終�?されま�?"):
        stop()

#スレ�?�?ィング宣言
theread1 = threading.Thread(target=server_open)
theread1.setDaemon(True)
theread2 = threading.Thread(target=client_connect)
theread2.setDaemon(True)

#メインウィンドウを作�??
main_win = tk.Tk()

#ウィンドウアイコンの設�?
main_win.iconbitmap('soft_ico.ico')

#メインウィンドウのタイトルを変更
main_win.title("ふぁいる�?�有ソフト")

#メインウィンドウサイズを変更
main_win.geometry("600x300")

#ウィンドウアイコンの設�?
main_win.iconbitmap("soft_ico.ico")

#�?ーマ設�?
ttk.Style().theme_use("classic")

#メインウィンドウにノ�?�トブ�?クを作�??
nb = ttk.Notebook(main_win)

#ノ�?�トブ�?クに関するフレー�?を作�??
tab1 = ttk.Frame(nb)
tab2 = ttk.Frame(nb)

#ノ�?�トブ�?クにタブを追�?
nb.add(tab1, text="サー�?", padding=3)
nb.add(tab2, text="クライアン�?", padding=3)

#メインウィンドウにノ�?�トブ�?クを�?�置
nb.pack(fill='both',expand=1)

#------以下tab1関�?-------

#自IP表示
<<<<<<< HEAD
ip_label = ttk.Label(tab1, text="自IPアドレス :")
ip_label.grid(column=0, row=0, sticky=tk.W,pady=5)

ip_list = socket.gethostbyname_ex(socket.gethostname())[2] #サーバ機�?�持つIPアドレスのリストを取�?
combo = ttk.Combobox(tab1, state='readonly', values=ip_list)
combo.set(ip_list[0])
combo.grid(column=1, row=0, sticky=tk.W,pady=5)
=======
ip_label_s = ttk.Label(tab1, text="自IPアドレス :")
ip_label_s.grid(column=0, row=0, sticky=tk.W,pady=5)

#サーバ機�?�持つIPアドレスのリストを取�?
ip_list = socket.gethostbyname_ex(socket.gethostname())[2]
combo = ttk.Combobox(tab1, state='readonly', values=ip_list)
combo.set(ip_list[0])
combo.grid(column=1, row=0, sticky=tk.W, padx=5)
>>>>>>> ad1828d56da7950dbab737e8c438c1d00c103141

if len(ip_list)>1:
    ip_label = ttk.Label(tab1, text="※ファイル共有�?��?�LANに属するIPアドレスを選�?")
    ip_label.grid(column=2, row=0, sticky=tk.W,pady=5)

#ポ�?�ト関�?
port_label_s = ttk.Label(tab1, text="ポ�?�ト番号 :")
port_label_s.grid(column=0, row=1, pady=5)

port_box_s = ttk.Entry(tab1)
port_box_s.grid(column=1, row=1, sticky=tk.W,padx=5)
port_box_s.insert(0, "21")

#フォルダー選択関�?
def folder():
    path = filedialog.askdirectory()
    folder_path.set(path)

folder_path = tk.StringVar()
folder_label_s = ttk.Label(tab1, text="フォルダ�?�? :")
folder_label_s.grid(column=0, row=2, pady=5)

folder_box_s = ttk.Entry(tab1, textvariable = folder_path)
folder_box_s.grid(column=1, row=2, sticky=tk.EW, padx=5)
folder_box_s.insert(0, os.path.realpath('.'))

<<<<<<< HEAD
folder_btn = ttk.Button(tab1, text="参�?�", command = folder)
folder_btn.grid(column=2, row=2, sticky=tk.W)
=======
folder_btn_s = ttk.Button(tab1, text="参�?�", command = folder)
folder_btn_s.grid(column=2, row=2)
>>>>>>> ad1828d56da7950dbab737e8c438c1d00c103141

#認証選択関�?
def entry_on():
    user_box_s.configure(state=tk.DISABLED)
    password_box_s.configure(state=tk.DISABLED)

def entry_off():
    user_box_s.configure(state=tk.NORMAL)
    password_box_s.configure(state=tk.NORMAL)

radio_value = tk.IntVar()
AuthSelect_label_s = ttk.Label(tab1, text="認証 :")
AuthSelect_label_s.grid(column=0, row=3, padx=5)

AuthSelect_on_btn_s = ttk.Radiobutton(tab1, text="あり",
                                    variable=radio_value,
                                    value=0,
                                    command=entry_off)
AuthSelect_on_btn_s.grid(column=1, row=3, sticky=tk.W, padx=5)

AuthSelect_off_btn_s = ttk.Radiobutton(tab1, text="な�?",
                                    variable=radio_value,
                                    value=1,
                                    command=entry_on)
AuthSelect_off_btn_s.grid(column=1, row=3, sticky=tk.W, padx=100)

#ユーザー選択関�?
user_label_s = ttk.Label(tab1, text="ユーザー :")
user_label_s.grid(column=0, row=4, pady=10)
user_box_s = ttk.Entry(tab1)
user_box_s.grid(column=1, row=4, sticky=tk.EW, padx=5)
user_box_s.insert(0, "user")

#パスワード選択関�?
password_label_s = ttk.Label(tab1, text="パスワー�? :")
password_label_s.grid(column=0, row=5, pady=10)
password_box_s = ttk.Entry(tab1)
password_box_s.grid(column=1, row=5, sticky=tk.EW, padx=5)
password_box_s.insert(0, "password")

#起動�?�タン関�?
ftp_open = ttk.Button(tab1, text="起�?", command=theread1.start)
ftp_open.grid(column=1, row=6, sticky=tk.W, padx=90)

#------以上tab1関�?-------

#------以下tab2関�?-------

#接続�??IP関�?
ip_label_c = ttk.Label(tab2, text="接続�??IPアドレス :")
ip_label_c.grid(column=0, row=0, sticky=tk.W,pady=10)
ip_box_c = ttk.Entry(tab2)
ip_box_c.grid(column=1, row=0, sticky=tk.W,padx=5)

#ポ�?�ト関�?
port_label_c = ttk.Label(tab2, text="接続�?��?��?�ト番号 :")
port_label_c.grid(column=0, row=1, pady=5)

port_box_c = ttk.Entry(tab2)
port_box_c.grid(column=1, row=1, sticky=tk.W,padx=5)
port_box_c.insert(0, "21")

#ユーザー選択関�?
user_label_c = ttk.Label(tab2, text="ユーザー :")
user_label_c.grid(column=0, row=4, pady=10)
user_box_c = ttk.Entry(tab2)
user_box_c.grid(column=1, row=4, sticky=tk.EW, padx=5)
user_box_c.insert(0, "user")

#パスワード選択関�?
password_label_c = ttk.Label(tab2, text="パスワー�? :")
password_label_c.grid(column=0, row=5, pady=10)
password_box_c = ttk.Entry(tab2)
password_box_c.grid(column=1, row=5, sticky=tk.EW, padx=5)
password_box_c.insert(0, "password")

#起動�?�タン関�?
ftp_connect = ttk.Button(tab2, text="接�?", command=theread2.start)
ftp_connect.grid(column=1, row=6, sticky=tk.W, padx=90)

#------以上tab2関�?-------

main_win.columnconfigure(0, weight=1)
main_win.rowconfigure(0, weight=1)
tab1.columnconfigure(1, weight=1)

main_win.protocol("WM_DELETE_WINDOW", exit_button)

main_win.mainloop()
