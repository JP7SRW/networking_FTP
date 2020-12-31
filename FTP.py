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
import datetime
import time

server_flag = False
client_flag = False

#サーバ起動時のウィンドウ起動関数
def server_window():

    def stop_server():
        server.close_all()
        server_win.destroy()
        ftp_open.config(state = tk.NORMAL)

    #main_winの子ウィンドウとしてserver_winを作成
    server_win = tk.Toplevel()

    #サーバウィンドウのタイトルを変更
    server_win.title("サーバ管理ウィンドウ")

    #サーバウィンドウのサイズを変更
    server_win.geometry("200x100")

    #ウィンドウアイコンの設定
    server_win.iconbitmap("soft_ico.ico")

    #サーバウィンドウにフレームを作成・配置
    server_frm = ttk.Frame(server_win)
    server_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

    #自IP表示
    ip = combo.get()
    ip_label_s = ttk.Label(server_frm, text="自IPアドレス :")
    ip_label_s.grid(column=0, row=0, sticky=tk.W, pady=5)
    ttk.Label(server_frm, text=ip).grid(column=1, row=0, sticky=tk.W, padx=5)

    #終了ボタン作成・配置
    ftp_close = ttk.Button(server_frm, text="終了", command = stop_server)
    ftp_close.grid(column=0, row=1, sticky=tk.W, padx=5)

    #windows側終了ボタン押下時関数呼び出し
    server_win.protocol("WM_DELETE_WINDOW", exit_button)

#サーバ起動関数
def server_open():

    server_window()

    global server_flag
    server_flag = True

    ip = combo.get()
    port = port_box_s.get()
    user = user_box_s.get()
    password = password_box_s.get()
    directory = folder_box_s.get()

    # 認証ユーザーを作る
    authorizer = pyftpdlib.authorizers.DummyAuthorizer()

    if auth_value.get():
        #anonymous認証時
        #TODO : 権限をrのみに変える必要有?(現状は何でも出来てしまう)
        authorizer.add_anonymous(directory, perm="elradfmw")
    else:
        authorizer.add_user(user, password, directory, perm="elradfmw")

    # 個々の接続を管理するハンドラーを作る
    handler = pyftpdlib.handlers.FTPHandler
    handler.authorizer = authorizer

    # FTPサーバーを立ち上げる
    global server
    server = pyftpdlib.servers.FTPServer((ip, port), handler)
    server.serve_forever()


#クライアント起動時のウィンドウ起動関数
def client_window():

    def stop_client():
        ftp.close()
        client_win.destroy()
        ftp_connect.config(state = tk.NORMAL)

    client_win = tk.Toplevel()

    #サーバウィンドウのタイトルを変更
    client_win.title("クライアント管理ウィンドウ")

    #サーバウィンドウのサイズを変更
    client_win.geometry("620x400")

    #ウィンドウアイコンの設定
    client_win.iconbitmap("soft_ico.ico")

    #サーバウィンドウにフレームを作成・配置
    client_frm = ttk.Frame(client_win)
    client_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

    #選択されたファイルを専用フォルダにダウンロード
    def select_lb(event):

        #ダウンロードディレクトリを取得
        dl_directory = dl_folder_box_s.get()
        #リストボックスの選択されている項目を取得
        for i in lb.curselection():

            #ダウンロード進行中のホップアップを出す
            nowload_win = tk.Toplevel()
            nowload_win.title("ダウンロードしています...")
            nowload_win.geometry("400x100")
            nowload_win.iconbitmap("soft_ico.ico")
            nowload_frm = ttk.Frame(nowload_win)
            nowload_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

            #ファイルサイズを取得
            ftp.voidcmd("TYPE I")
            size = ftp.size(files[i])

            #各種ウィジェット(ファイル名，ダウンロード先，サイズ)を表示
            nowload_filename = ttk.Label(nowload_frm, text="ダウンロードするファイル: " + files[i])
            nowload_filename.grid(column=0, row=0, pady=5, sticky=tk.W)

            nowload_filename = ttk.Label(nowload_frm, text="ダウンロード先: " + dl_directory)
            nowload_filename.grid(column=0, row=1, pady=5, sticky=tk.W)

            nowload_filesize = ttk.Label(nowload_frm, text="ファイルサイズ:    {}[byte]".format(size))
            nowload_filesize.grid(column=0, row=2, pady=5, sticky=tk.W)

            #ファイルをバイナリ転送モードで取得
            with open(dl_directory + "\\" + files[i], "wb") as f:
                ftp.retrbinary("RETR " + files[i], f.write)
            #ToDo: ダウンロードが終わったらこのウィンドウを閉じさせる

    lb_label = ttk.Label(client_frm, text="ダウンロードするファイル :")
    lb_label.grid(column=0, row=0, pady=5, sticky=tk.N)

    #サーバ側のファイルの一覧取得
    files = ftp.nlst(".")

    #ファイル名を取得
    txt = tk.StringVar(value=files)

    #リストボックス作成・設置
    lb = tk.Listbox(client_frm, listvariable=txt, width=70, height=16)
    lb.grid(column=1, row=0)

    #リストボックスの中身を選択したらselect_lbを実行
    lb.bind("<<ListboxSelect>>", select_lb)

    #リストボックス内の複数選択を可能にする
    lb.configure(selectmode= tk.EXTENDED )

    #フォルダー選択関係
    def dl_folder():
        dl_path = filedialog.askdirectory()
        dl_folder_path.set(dl_path)

    dl_folder_path = tk.StringVar()
    dl_folder_label_s = ttk.Label(client_frm, text="フォルダ指定 :")
    dl_folder_label_s.grid(column=0, row=1, pady=5)

    dl_folder_box_s = ttk.Entry(client_frm, textvariable = dl_folder_path)
    dl_folder_box_s.grid(column=1, row=1, sticky=tk.EW, padx=10)
    dl_folder_box_s.insert(0, os.path.realpath("./download"))

    dl_folder_btn_s = ttk.Button(client_frm, text="参照", command = dl_folder)
    dl_folder_btn_s.grid(column=2, row=1)

    #スクロールバーの作成・配置
    scrollbar = ttk.Scrollbar(client_frm,orient=tk.VERTICAL,command=lb.yview)
    scrollbar.grid(column=2, row=0, sticky=tk.NS)

    #終了ボタンの作成・配置
    ftp_close = ttk.Button(client_frm, text="終了", command = stop_client)
    ftp_close.grid(column=1, row=2, sticky=tk.N, padx=5)

    #windows側終了ボタン押下時関数呼び出し
    client_win.protocol("WM_DELETE_WINDOW", exit_button)


#クライアント起動関数
def client_connect():

    global client_flag
    client_flag = True

    ip = ip_box_c.get()
    #TODO: 何故かportだけintにキャストしないとエラーになる
    port = int(port_box_c.get())
    user = user_box_c.get()
    password = password_box_c.get()

    #FTPオブジェクトのインスタンス化
    global ftp
    ftp = FTP()

    #FTPサーバにログイン
    ftp.connect(ip,port)

    #匿名ログインの有無
    if login_value.get():
        ftp.login()
    else:
        ftp.login(user,password)

    client_window()

#FTP&プログラム終了関数
def stop():
    if (server_flag):
        server.close_all()
    if (client_flag):
        ftp.close()
    exit()

#windows側終了ボタン押下時関数
def exit_button():
    if messagebox.askokcancel("確認","プログラムを終了してもよろしいですか？\
                            \nFTPで通信中の場合、サーバとクライアントの両方が終了されます。"):
        stop()

#時計を表示
def change_label_text():
    while True:
        clock = ttk.Label(tab1, text=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        clock.grid(column=0, row=7, sticky=tk.W, padx=0)
        time.sleep(1)

#スレッディング宣言
def start_theread1():
    ftp_open.config(state = tk.DISABLED)
    theread1 = threading.Thread(target=server_open)
    theread1.setDaemon(True)
    theread1.start()

def start_theread2():
    ftp_connect.config(state = tk.DISABLED)
    theread2 = threading.Thread(target=client_connect)
    theread2.setDaemon(True)
    theread2.start()

theread3 = threading.Thread(target=change_label_text)
theread3.setDaemon(True)

#メインウィンドウを作成
main_win = tk.Tk()

#メインウィンドウのタイトルを変更
main_win.title("ふぁいる共有ソフト")

#メインウィンドウサイズを変更
main_win.geometry("650x400")

#ウィンドウアイコンの設定
main_win.iconbitmap("soft_ico.ico")

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
nb.pack(fill="both",expand=1)

#------以下tab1関係-------

#自IP表示
ip_label_s = ttk.Label(tab1, text="自IPアドレス :")
ip_label_s.grid(column=0, row=0, sticky=tk.E,pady=5)

#サーバ機の持つIPアドレスのリストを取得
ip_list = socket.gethostbyname_ex(socket.gethostname())[2]
combo = ttk.Combobox(tab1, state="readonly", values=ip_list)
combo.set(ip_list[0])
combo.grid(column=1, row=0, sticky=tk.W, padx=5)

if len(ip_list)>1:
    ip_label = ttk.Label(tab1, text="※ファイル共有先のLANに属するIPアドレスを選択してください")
    ip_label.grid(column=2, row=0, sticky=tk.E,pady=5)

#ポート関係
port_label_s = ttk.Label(tab1, text="ポート番号 :")
port_label_s.grid(column=0, row=1,sticky=tk.E, pady=5)

port_box_s = ttk.Entry(tab1)
port_box_s.grid(column=1, row=1, sticky=tk.W,padx=5)
port_box_s.insert(0, "21")

#フォルダー選択関係
def folder():
    path = filedialog.askdirectory()
    folder_path.set(path)

folder_path = tk.StringVar()
folder_label_s = ttk.Label(tab1, text="フォルダ指定 :")
folder_label_s.grid(column=0, row=2, sticky=tk.E, pady=5)

folder_box_s = ttk.Entry(tab1, textvariable = folder_path)
folder_box_s.grid(column=1, row=2, sticky=tk.EW, padx=5)
folder_box_s.insert(0, os.path.realpath("."))

folder_btn_s = ttk.Button(tab1, text="参照", command = folder)
folder_btn_s.grid(column=2, row=2)

#ユーザー選択関係
user_label_s = ttk.Label(tab1, text="ユーザー :")
user_label_s.grid(column=0, row=3, sticky=tk.E, pady=10)
user_box_s = ttk.Entry(tab1)
user_box_s.grid(column=1, row=3, sticky=tk.EW, padx=5)
user_box_s.insert(0, "user")

#パスワード選択関係
password_label_s = ttk.Label(tab1, text="パスワード :")
password_label_s.grid(column=0, row=4, sticky=tk.E, pady=10)
password_box_s = ttk.Entry(tab1)
password_box_s.grid(column=1, row=4, sticky=tk.EW, padx=5)
password_box_s.insert(0, "password")

#認証選択関係
def auth_change_state():
    if auth_value.get():
        user_box_s.delete(0, tk.END)
        user_box_s.insert(0, "anonymous")
        user_box_s.configure(state=tk.DISABLED)

        password_box_s.delete(0, tk.END)
        password_box_s.insert(0, "")
        password_box_s.configure(state=tk.DISABLED)
    else:
        user_box_s.configure(state=tk.NORMAL)
        user_box_s.delete(0, tk.END)
        user_box_s.insert(0, "user")

        password_box_s.configure(state=tk.NORMAL)
        password_box_s.delete(0, tk.END)
        password_box_s.insert(0, "password")

auth_value = tk.BooleanVar()
login_anonymous_btn_c = tk.Checkbutton(tab1, variable=auth_value,
                                    text="匿名ログイン", command=auth_change_state)
login_anonymous_btn_c.grid(column=0, row=5, pady=10)

#起動ボタン関係
ftp_open = ttk.Button(tab1, text="起動", command=start_theread1)
ftp_open.grid(column=1, row=6, sticky=tk.W, padx=90)

#時計スタート
theread3.start()

#------以上tab1関係-------

#------以下tab2関係-------

#接続先IP関係
ip_label_c = ttk.Label(tab2, text="接続先IPアドレス :")
ip_label_c.grid(column=0, row=0, sticky=tk.E,pady=10)
ip_box_c = ttk.Entry(tab2)
ip_box_c.grid(column=1, row=0, sticky=tk.W,padx=5)

#ポート関係
port_label_c = ttk.Label(tab2, text="接続先ポート番号 :")
port_label_c.grid(column=0, row=1, sticky=tk.E, pady=5)

port_box_c = ttk.Entry(tab2)
port_box_c.grid(column=1, row=1, sticky=tk.W,padx=5)
port_box_c.insert(0, "21")

#ユーザー選択関係
user_label_c = ttk.Label(tab2, text="ユーザー :")
user_label_c.grid(column=0, row=4, sticky=tk.E, pady=10)
user_box_c = ttk.Entry(tab2)
user_box_c.grid(column=1, row=4, sticky=tk.EW, padx=5)
user_box_c.insert(0, "user")

#パスワード選択関係
password_label_c = ttk.Label(tab2, text="パスワード :")
password_label_c.grid(column=0, row=5, sticky=tk.E, pady=10)
password_box_c = ttk.Entry(tab2)
password_box_c.grid(column=1, row=5, sticky=tk.EW, padx=5)
password_box_c.insert(0, "password")

def login_change_state():
    if login_value.get():
        user_box_c.delete(0, tk.END)
        user_box_c.insert(0, "anonymous")
        user_box_c.configure(state=tk.DISABLED)

        password_box_c.delete(0, tk.END)
        password_box_c.insert(0, "")
        password_box_c.configure(state=tk.DISABLED)
    else:
        user_box_c.configure(state=tk.NORMAL)
        user_box_c.delete(0, tk.END)
        user_box_c.insert(0, "user")

        password_box_c.configure(state=tk.NORMAL)
        password_box_c.delete(0, tk.END)
        password_box_c.insert(0, "password")

login_value = tk.BooleanVar()
login_anonymous_btn_c = tk.Checkbutton(tab2, variable=login_value,
                                    text="匿名ログイン", command=login_change_state)
login_anonymous_btn_c.grid(column=0, row=6, pady=10)

#起動ボタン関係
ftp_connect = ttk.Button(tab2, text="接続", command=start_theread2)
ftp_connect.grid(column=1, row=7, sticky=tk.W, padx=90)

#------以上tab2関係-------

main_win.columnconfigure(0, weight=1)
main_win.rowconfigure(0, weight=1)
tab1.columnconfigure(1, weight=1)

main_win.protocol("WM_DELETE_WINDOW", exit_button)

main_win.mainloop()
