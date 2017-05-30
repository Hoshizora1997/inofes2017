from bottle import route, get, redirect
#from __future__ import print_function
import socket
from contextlib import closing

mainURL = 'http://0.0.0.0/page/'
targetIP = '127.0.0.1'
port = 4000

@get('/')
def red():
    redirect(mainURL)


@route('/', method='POST')
def do():
    try:
        f = open('num', 'w')
        n = f.read()
        n = int(n)+1
        f.write(n)
        f.close()
        print('ファイル書き換え成功\n')
    except:
        return '数値操作エラーが発生しました。操作をやり直してください'
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        with closing(sock):
            message = n.encode('utf-8')
            sock.sendto(message, (targetIP, port))
        print('送信成功\n'+message)

    except:
        return '通信エラーが発生しました。操作をやり直してください'


    redirect(mainURL, 301)