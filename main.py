from bottle import route, get, redirect, template, TEMPLATE_PATH, run, request
#from __future__ import print_function
#import socket
#from contextlib import closing
import time

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
    #累計情報の更新
    try:
        f = open('num', 'r')
        n = int(f.read().strip())+1
        f.close()
        f = open('num','w')
        f.write(str(n))
        f.close()
    except:
        return '累計数値操作エラーが発生しました。操作をやり直してください。'
    #タイム情報の更新
    try:
        f = open('timedata','a')#追記モードで開く
        n = str(time.time())+'\n'
        f.write(n)
        f.close()
    except:
        return 'タイム記録エラーが発生しました。操作をやり直してください。'

    #log
    try:
        f = open('log','a')
        f.write(str(int(time.time()))+'[post]Button was pushed\n')
        f.close()
    except:
        return 'ログ記録エラー'

    redirect(mainURL+'page/', 301)

# --------------------------
# Configページ
# --------------------------

@get('/config/')
def config():
    return template('config',)

@route('/config/',method='POST')
def do_config():
    line = request.forms.get('line')
    num = request.forms.get('num')
    speed = request.forms.get('speed')

    line = int(line)
    num = int(num)
    speed = int(speed)

    retext = '設定の変更を完了しました。<br/>'#完了文の生成

    #0は設定を現状維持
    if(line != 0):
        f = open('line','w')
        f.write(str(line))
        retext += '<br/>閾値：' + str(line)
    else:
        retext += '<br/>閾値：変化なし'
    if(num != 0):
        f = open('num','w')
        f.write(str(num))
        retext += '<br/>累計数：' + str(num)
    else:
        retext += '<br/>累計数：変化なし'
    if(speed != 0):
        f = open('speed','w')
        f.write(str(speed))
        retext += '<br/>秒速：' + str(speed)
    else:
        retext += '<br/>秒速：変化なし'

    return (retext)



run(host='0.0.0.0', port=8080, debug=True)