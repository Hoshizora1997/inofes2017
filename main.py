from bottle import route, get, redirect, template, TEMPLATE_PATH, run
#from __future__ import print_function
import socket
from contextlib import closing

mainURL = 'http://0.0.0.0:8080/'
#targetIP = '127.0.0.1'
#port = 4000

TEMPLATE_PATH.append("./page")

@get('/page/')
def page():
    return template('index',)

@get('/')
def red():
    redirect(mainURL+'page/', 301)


@route('/', method='POST')
def do():
    try:
        f = open('num', 'r')
        print('ファイル読み込み完了')
        n = int(f.read().strip())
        print(n)
        print('読み込み完了')
        n += 1
        print(n)
        f.close()
        f = open('./num','w')
        print('ファイル書き込み準備完了')
        f.write(str(n))
        f.close()
        print('ファイル書き換え成功\n')
    except:
        return '数値操作エラーが発生しました。操作をやり直してください'
#    try:
#        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#        with closing(sock):
#            message = n.encode('utf-8')
#            sock.sendto(message, (targetIP, port))
#        print('送信成功\n'+message)
#
#    except:
#        return '通信エラーが発生しました。操作をやり直してください'
    redirect(mainURL+'page/', 301)

run(host='0.0.0.0', port=8080, debug=True)