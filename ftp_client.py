# -*- coding: utf8 -*-
from ftplib import FTP
host = '127.0.0.1'
user = 'user'
password = 'password'
file_name = 'test.txt'

print("--Starting FTP Client--")

ftp = FTP(host, user, password)
files = ftp.nlst()
print(files)

with open(file_name, 'wb') as f:
    ftp.retrbinary('RETR ' + file_name, f.write)

print("--Closing FTP Client--")
ftp.close()