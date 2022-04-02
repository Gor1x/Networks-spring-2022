import argparse
import os
import sys
from ftplib import FTP


def printfiletree(ways):
    print()
    print('Current local directory')
    for w in ways:
        print(w)
    print('----------------------------------------')


clear = lambda: os.system('cls')


class LocalFtp:
    def __init__(self):
        self.ftp = FTP()
        self.ftp.connect("127.0.0.1", 21)
        self.ftp.login('TestUser', '')

    def login(self, user, password):
        self.ftp.login(user, password)

    def printdir(self):
        print()
        print("Current ftp directory")
        data = list(self.ftp.mlsd())
        for d in data:
            print('{:10s} {:5s}'.format(d[0], d[1]['type']))
        print("----------------------------------------")

    def goto(self, name):
        self.ftp.cwd(name)

    def download(self, srcname, destname):
        self.ftp.retrbinary(f'RETR {name}', None)

    def stor(self, srcname, destname):
        with open(srcname, 'rb') as f:
            self.ftp.storbinary(f'STOR ./{destname}', f)

    def readmeread(self):
        with open('readme', 'rb') as fp:
            self.ftp.storbinary('STOR readme', fp)

    def readmewrite(self):
        with open('readme', 'wb') as fp:
            self.ftp.retrbinary('RETR readme', fp.write)

    def up(self):
        self.ftp.cwd('..')


def main():
    ftp = LocalFtp()
    ftp.ftp.dir()


def ls(path='./'):
    ftp = LocalFtp()
    ftp.ftp.dir(path)


def uploadToServer(src_path, dest_path):
    ftp = LocalFtp()
    with open(src_path, "rb") as f:
        ftp.ftp.storbinary(f"STOR {dest_path}", f)


def downloadFromServer(src_path, dest_path):
    ftp = LocalFtp()
    with open(dest_path, "wb") as f:
        ftp.ftp.retrbinary(f"RETR {src_path}", f.write)


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == 'ls':
        print(args[1])
        ls(args[1])
    elif args[0] == 'upload':
        uploadToServer(args[1], args[2])
    elif args[0] == 'download':
        downloadFromServer(args[1], args[2])
    else:
        print("UNKNOWN NAME")
