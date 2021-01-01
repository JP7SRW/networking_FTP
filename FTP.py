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

#�T�[�o�N�����̃E�B���h�E�N���֐�
def server_window():

    def stop_server():
        server.close_all()
        server_win.destroy()
        ftp_open.config(state = tk.NORMAL)

    #main_win�̎q�E�B���h�E�Ƃ���server_win���쐬
    server_win = tk.Toplevel()

    #�T�[�o�E�B���h�E�̃^�C�g����ύX
    server_win.title("�T�[�o�Ǘ��E�B���h�E")

    #�T�[�o�E�B���h�E�̃T�C�Y��ύX
    server_win.geometry("200x100")

    #�E�B���h�E�A�C�R���̐ݒ�
    server_win.iconbitmap("soft_ico.ico")

    #�T�[�o�E�B���h�E�Ƀt���[�����쐬�E�z�u
    server_frm = ttk.Frame(server_win)
    server_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

    #��IP�\��
    ip = combo.get()
    ip_label_s = ttk.Label(server_frm, text="��IP�A�h���X :")
    ip_label_s.grid(column=0, row=0, sticky=tk.W, pady=5)
    ttk.Label(server_frm, text=ip).grid(column=1, row=0, sticky=tk.W, padx=5)

    #�I���{�^���쐬�E�z�u
    ftp_close = ttk.Button(server_frm, text="�I��", command = stop_server)
    ftp_close.grid(column=0, row=1, sticky=tk.W, padx=5)

    #windows���I���{�^���������֐��Ăяo��
    server_win.protocol("WM_DELETE_WINDOW", exit_button)

#�T�[�o�N���֐�
def server_open():

    server_window()

    global server_flag
    server_flag = True

    ip = combo.get()
    port = port_box_s.get()
    user = user_box_s.get()
    password = password_box_s.get()
    directory = folder_box_s.get()

    # �F�؃��[�U�[�����
    authorizer = pyftpdlib.authorizers.DummyAuthorizer()

    if auth_value.get():
        #anonymous�F�؎�
        #TODO : ������r�݂̂ɕς���K�v�L?(����͉��ł��o���Ă��܂�)
        authorizer.add_anonymous(directory, perm="elradfmw")
    else:
        authorizer.add_user(user, password, directory, perm="elradfmw")

    # �X�̐ڑ����Ǘ�����n���h���[�����
    handler = pyftpdlib.handlers.FTPHandler
    handler.authorizer = authorizer

    # FTP�T�[�o�[�𗧂��グ��
    global server
    server = pyftpdlib.servers.FTPServer((ip, port), handler)
    server.serve_forever()


#�N���C�A���g�N�����̃E�B���h�E�N���֐�
def client_window():

    def stop_client():
        ftp.close()
        client_win.destroy()
        ftp_connect.config(state = tk.NORMAL)

    client_win = tk.Toplevel()

    #�T�[�o�E�B���h�E�̃^�C�g����ύX
    client_win.title("�N���C�A���g�Ǘ��E�B���h�E")

    #�T�[�o�E�B���h�E�̃T�C�Y��ύX
    client_win.geometry("620x400")

    #�E�B���h�E�A�C�R���̐ݒ�
    client_win.iconbitmap("soft_ico.ico")

    #�T�[�o�E�B���h�E�Ƀt���[�����쐬�E�z�u
    client_frm = ttk.Frame(client_win)
    client_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

    #�I�����ꂽ�t�@�C�����p�t�H���_�Ƀ_�E�����[�h
    def select_lb(event):

        def status():
            while True:
                print(os.path.getsize(dl_directory + "\\" + files[i]))
                time.sleep(0.01)

        theread4 = threading.Thread(target=status)
        theread4.setDaemon(True)


        #�_�E�����[�h�f�B���N�g�����擾
        dl_directory = dl_folder_box_s.get()
        #���X�g�{�b�N�X�̑I������Ă��鍀�ڂ��擾
        for i in lb.curselection():

            #�_�E�����[�h�i�s���̃z�b�v�A�b�v���o��
            nowload_win = tk.Toplevel()
            nowload_win.title("�_�E�����[�h���Ă��܂�...")
            nowload_win.geometry("400x100")
            nowload_win.iconbitmap("soft_ico.ico")
            nowload_frm = ttk.Frame(nowload_win)
            nowload_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

            #�t�@�C���T�C�Y���擾
            ftp.voidcmd("TYPE I")
            size = ftp.size(files[i])

            #�e��E�B�W�F�b�g(�t�@�C�����C�_�E�����[�h��C�T�C�Y)��\��
            nowload_filename = ttk.Label(nowload_frm, text="�_�E�����[�h����t�@�C��: " + files[i] )
            nowload_filename.grid(column=0, row=0, pady=5, sticky=tk.W)

            nowload_filename = ttk.Label(nowload_frm, text="�_�E�����[�h��: " + dl_directory)
            nowload_filename.grid(column=0, row=1, pady=5, sticky=tk.W)

            nowload_filesize = ttk.Label(nowload_frm, text="�t�@�C���T�C�Y:    {}[byte]".format(size))
            nowload_filesize.grid(column=0, row=2, pady=5, sticky=tk.W)

            #�t�@�C�����o�C�i���]�����[�h�Ŏ擾
            with open(dl_directory + "\\" + files[i], "wb") as f:
                theread4.start()
                ftp.retrbinary("RETR " + files[i], f.write)
            #ToDo: �_�E�����[�h���I������炱�̃E�B���h�E���������

    lb_label = ttk.Label(client_frm, text="�_�E�����[�h����t�@�C�� :")
    lb_label.grid(column=0, row=0, pady=5, sticky=tk.N)

    #�T�[�o���̃t�@�C���̈ꗗ�擾
    files = ftp.nlst(".")

    #�t�@�C�������擾
    fname = tk.StringVar(value=files)
    
    #�T�[�o���̃t�@�C���T�C�Y���擾
    #fsize = ftp.size(tk.StringVar(value=files))

    #���X�g�{�b�N�X�쐬�E�ݒu
    lb = tk.Listbox(client_frm, listvariable=fname, width=70, height=16)
    lb.grid(column=1, row=0)

    #���X�g�{�b�N�X�̒��g��I��������select_lb�����s
    lb.bind("<<ListboxSelect>>", select_lb)

    #���X�g�{�b�N�X���̕����I�����\�ɂ���
    lb.configure(selectmode= tk.EXTENDED )

    #�t�H���_�[�I���֌W
    def dl_folder():
        dl_path = filedialog.askdirectory()
        dl_folder_path.set(dl_path)

    dl_folder_path = tk.StringVar()
    dl_folder_label_s = ttk.Label(client_frm, text="�t�H���_�w�� :")
    dl_folder_label_s.grid(column=0, row=1, pady=5)

    dl_folder_box_s = ttk.Entry(client_frm, textvariable = dl_folder_path)
    dl_folder_box_s.grid(column=1, row=1, sticky=tk.EW, padx=10)
    dl_folder_box_s.insert(0, os.path.realpath("./download"))

    dl_folder_btn_s = ttk.Button(client_frm, text="�Q��", command = dl_folder)
    dl_folder_btn_s.grid(column=2, row=1)

    #�X�N���[���o�[�̍쐬�E�z�u
    scrollbar = ttk.Scrollbar(client_frm,orient=tk.VERTICAL,command=lb.yview)
    scrollbar.grid(column=2, row=0, sticky=tk.NS)

    #�I���{�^���̍쐬�E�z�u
    ftp_close = ttk.Button(client_frm, text="�I��", command = stop_client)
    ftp_close.grid(column=1, row=2, sticky=tk.N, padx=5)

    #windows���I���{�^���������֐��Ăяo��
    client_win.protocol("WM_DELETE_WINDOW", exit_button)


#�N���C�A���g�N���֐�
def client_connect():

    global client_flag
    client_flag = True

    ip = ip_box_c.get()
    #TODO: ���̂�port����int�ɃL���X�g���Ȃ��ƃG���[�ɂȂ�
    port = int(port_box_c.get())
    user = user_box_c.get()
    password = password_box_c.get()

    #FTP�I�u�W�F�N�g�̃C���X�^���X��
    global ftp
    ftp = FTP()

    #FTP�T�[�o�Ƀ��O�C��
    ftp.connect(ip,port)

    #�������O�C���̗L��
    if login_value.get():
        ftp.login()
    else:
        ftp.login(user,password)

    client_window()

#FTP&�v���O�����I���֐�
def stop():
    if (server_flag):
        server.close_all()
    if (client_flag):
        ftp.close()
    exit()

#windows���I���{�^���������֐�
def exit_button():
    if messagebox.askokcancel("�m�F","�v���O�������I�����Ă���낵���ł����H\
                            \nFTP�ŒʐM���̏ꍇ�A�T�[�o�ƃN���C�A���g�̗������I������܂��B"):
        stop()

#���v��\��
def showclock():
    while True:
        clock = ttk.Label(tab1, text=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        clock.grid(column=0, row=7, sticky=tk.W, padx=0)
        time.sleep(1)

#�X���b�f�B���O�錾
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

theread3 = threading.Thread(target=showclock)
theread3.setDaemon(True)

#���C���E�B���h�E���쐬
main_win = tk.Tk()

#���C���E�B���h�E�̃^�C�g����ύX
main_win.title("�ӂ����鋤�L�\�t�g")

#���C���E�B���h�E�T�C�Y��ύX
main_win.geometry("650x400")

#�E�B���h�E�A�C�R���̐ݒ�
main_win.iconbitmap("soft_ico.ico")

#�e�[�}�ݒ�
ttk.Style().theme_use("classic")

#���C���E�B���h�E�Ƀm�[�g�u�b�N���쐬
nb = ttk.Notebook(main_win)

#�m�[�g�u�b�N�Ɋւ���t���[�����쐬
tab1 = ttk.Frame(nb)
tab2 = ttk.Frame(nb)

#�m�[�g�u�b�N�Ƀ^�u��ǉ�
nb.add(tab1, text="�T�[�o", padding=3)
nb.add(tab2, text="�N���C�A���g", padding=3)

#���C���E�B���h�E�Ƀm�[�g�u�b�N��z�u
nb.pack(fill="both",expand=1)

#------�ȉ�tab1�֌W-------

#��IP�\��
ip_label_s = ttk.Label(tab1, text="��IP�A�h���X :")
ip_label_s.grid(column=0, row=0, sticky=tk.E,pady=5)

#�T�[�o�@�̎���IP�A�h���X�̃��X�g���擾
ip_list = socket.gethostbyname_ex(socket.gethostname())[2]
combo = ttk.Combobox(tab1, state="readonly", values=ip_list)
combo.set(ip_list[0])
combo.grid(column=1, row=0, sticky=tk.W, padx=5)

if len(ip_list)>1:
    ip_label = ttk.Label(tab1, text="���t�@�C�����L���LAN�ɑ�����IP�A�h���X��I�����Ă�������")
    ip_label.grid(column=2, row=0, sticky=tk.E,pady=5)

#�|�[�g�֌W
port_label_s = ttk.Label(tab1, text="�|�[�g�ԍ� :")
port_label_s.grid(column=0, row=1,sticky=tk.E, pady=5)

port_box_s = ttk.Entry(tab1)
port_box_s.grid(column=1, row=1, sticky=tk.W,padx=5)
port_box_s.insert(0, "21")

#�t�H���_�[�I���֌W
def folder():
    path = filedialog.askdirectory()
    folder_path.set(path)

folder_path = tk.StringVar()
folder_label_s = ttk.Label(tab1, text="�t�H���_�w�� :")
folder_label_s.grid(column=0, row=2, sticky=tk.E, pady=5)

folder_box_s = ttk.Entry(tab1, textvariable = folder_path)
folder_box_s.grid(column=1, row=2, sticky=tk.EW, padx=5)
folder_box_s.insert(0, os.path.realpath("."))

folder_btn_s = ttk.Button(tab1, text="�Q��", command = folder)
folder_btn_s.grid(column=2, row=2)

#���[�U�[�I���֌W
user_label_s = ttk.Label(tab1, text="���[�U�[ :")
user_label_s.grid(column=0, row=3, sticky=tk.E, pady=10)
user_box_s = ttk.Entry(tab1)
user_box_s.grid(column=1, row=3, sticky=tk.EW, padx=5)
user_box_s.insert(0, "user")

#�p�X���[�h�I���֌W
password_label_s = ttk.Label(tab1, text="�p�X���[�h :")
password_label_s.grid(column=0, row=4, sticky=tk.E, pady=10)
password_box_s = ttk.Entry(tab1)
password_box_s.grid(column=1, row=4, sticky=tk.EW, padx=5)
password_box_s.insert(0, "password")

#�F�ؑI���֌W
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
                                    text="�������O�C��", command=auth_change_state)
login_anonymous_btn_c.grid(column=0, row=5, pady=10)

#�N���{�^���֌W
ftp_open = ttk.Button(tab1, text="�N��", command=start_theread1)
ftp_open.grid(column=1, row=6, sticky=tk.W, padx=90)

#���v�X�^�[�g
theread3.start()

#------�ȏ�tab1�֌W-------

#------�ȉ�tab2�֌W-------

#�ڑ���IP�֌W
ip_label_c = ttk.Label(tab2, text="�ڑ���IP�A�h���X :")
ip_label_c.grid(column=0, row=0, sticky=tk.E,pady=10)
ip_box_c = ttk.Entry(tab2)
ip_box_c.grid(column=1, row=0, sticky=tk.W,padx=5)

#�|�[�g�֌W
port_label_c = ttk.Label(tab2, text="�ڑ���|�[�g�ԍ� :")
port_label_c.grid(column=0, row=1, sticky=tk.E, pady=5)

port_box_c = ttk.Entry(tab2)
port_box_c.grid(column=1, row=1, sticky=tk.W,padx=5)
port_box_c.insert(0, "21")

#���[�U�[�I���֌W
user_label_c = ttk.Label(tab2, text="���[�U�[ :")
user_label_c.grid(column=0, row=4, sticky=tk.E, pady=10)
user_box_c = ttk.Entry(tab2)
user_box_c.grid(column=1, row=4, sticky=tk.EW, padx=5)
user_box_c.insert(0, "user")

#�p�X���[�h�I���֌W
password_label_c = ttk.Label(tab2, text="�p�X���[�h :")
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
                                    text="�������O�C��", command=login_change_state)
login_anonymous_btn_c.grid(column=0, row=6, pady=10)

#�N���{�^���֌W
ftp_connect = ttk.Button(tab2, text="�ڑ�", command=start_theread2)
ftp_connect.grid(column=1, row=7, sticky=tk.W, padx=90)

#------�ȏ�tab2�֌W-------

main_win.columnconfigure(0, weight=1)
main_win.rowconfigure(0, weight=1)
tab1.columnconfigure(1, weight=1)

main_win.protocol("WM_DELETE_WINDOW", exit_button)

main_win.mainloop()
