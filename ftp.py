# -*- coding: utf8 -*-
import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers
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

# 個々の接続を管理するハンドラーを作る
handler = pyftpdlib.handlers.FTPHandler
handler.authorizer = authorizer

# FTPサーバーを立ち上げる
server = pyftpdlib.servers.FTPServer(("127.0.0.1", 21), handler)
server.serve_forever()
