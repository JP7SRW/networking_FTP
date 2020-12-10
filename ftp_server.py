# -*- coding: utf8 -*-
import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers
<<<<<<< HEAD

# 認証ユーザーを作る
authorizer = pyftpdlib.authorizers.DummyAuthorizer()
authorizer.add_user('user', 'password', 'C:/Users/shou/Desktop/programming/network_programming', perm='elradfmw')
=======
import sys

# コマンドライン引数の判断
args = sys.argv
argvlen =len(sys.argv)
if argvlen > 0:
    directory = args[1]
if argvlen < 1:
    directory = 'C:/Users/shou/Desktop/programming/network_programming'

# 認証ユーザーを作る
authorizer = pyftpdlib.authorizers.DummyAuthorizer()
authorizer.add_user('user', 'password', directory, perm='elradfmw')
>>>>>>> 750e13caa4d201a06e65f811101a1a7539370658

# 個々の接続を管理するハンドラーを作る
handler = pyftpdlib.handlers.FTPHandler
handler.authorizer = authorizer

# FTPサーバーを立ち上げる
server = pyftpdlib.servers.FTPServer(("127.0.0.1", 21), handler)
server.serve_forever()
<<<<<<< HEAD
=======

# hoge
>>>>>>> 750e13caa4d201a06e65f811101a1a7539370658
