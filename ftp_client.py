# -*- coding: utf8 -*-

import ftplib
from ftplib import FTP

host = '127.0.0.1'
port = 21
user = 'user'
password = 'password'

# FTPオブジェクトをインスタンス化
ftp = FTP()

# FTPサーバに接続
ftp.connect(host, port)
#FTPサーバにログイン
ftp.login(user, password)
# FTPサーバのファイル一覧を取得
files = ftp.nlst("/dir")
print(files)
ftp.close()