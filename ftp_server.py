# -*- coding: utf8 -*-
import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers
import sys

ip_address = # your NIC's ip address
port = # free (21 is default value)
# コマンドライン引数の判断
args = sys.argv
argvlen =len(sys.argv)
if argvlen > 1:
    directory = args[1]
if argvlen < 2:
    directory = 'C:\\Users\\akira\\Desktop\\network_ftp'

# 認証ユーザーを作る
authorizer = pyftpdlib.authorizers.DummyAuthorizer()
authorizer.add_user('user', 'password', directory, perm='elradfmw')

# 個々の接続を管理するハンドラーを作る
handler = pyftpdlib.handlers.FTPHandler
handler.authorizer = authorizer

# FTPサーバーを立ち上げる
server = pyftpdlib.servers.FTPServer((ip_address, port), handler)
server.serve_forever()
