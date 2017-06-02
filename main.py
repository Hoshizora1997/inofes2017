#coding: UTF-8
from bottle import route, get, redirect, template, TEMPLATE_PATH, run, request, static_file, hook, response
import time
import sys
import fcntl
import io

mainURL = 'http://www.j-wave.co.jp/iwf2017/specialtalklive/'

TEMPLATE_PATH.append("./page")

@route('/data/<filename>')
def static_file_crossdomain(filename):
    response = static_file(filename, root="./data")
    response.set_header('Access-Control-allow-Origin', '*')
    return response

#@get('/page/')
#def page():
#    return template('index',)

@get('/')
def red():
    redirect(mainURL, 301)

@route('/', method='POST')
def do():
    #累計情報の更新
    #try:
        #f = open('./data/num', 'r+')
        #n = int(f.read().strip())+1
        #f.seek(0)
        #f.close()
        #f = open('./data/num','w')
        #f.write(str(n))
        #f.truncate()
        #f.close()

    with open('./data/num') as f: # ロックを獲得できるまで待機
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            n = int(f.read().strip()) + 1
            f.seek(0)
            f.write(str(n))
            f.truncate()
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    #except:
    #    try:
    #        f = open('./data/log', 'a')
    #        f.write(str(int(time.time())) + '[Error][post]Button was pushed NUM ERROR\n')
    #        f.close()
    #    except:
    #        return '累計数値操作エラーのログ記録エラーが発生しました。操作をやり直してください。'
    #    return '累計数値操作エラーが発生しました。操作をやり直してください。'
    #タイム情報の更新
    try:
        f = open('./data/timedata','a')#追記モードで開く
        n = str(time.time())+'\n'
        f.write(n)
        f.close()
    except:
        try:
            f = open('./data/log', 'a')
            f.write(str(int(time.time())) + '[Error][post]Button was pushed TIMEDATA ERROR\n')
            f.close()
        except:
            return 'タイム記録エラーのログ記録エラーが発生しました。操作をやり直してください。'
        return 'タイム記録エラーが発生しました。操作をやり直してください。'

    #log
    try:
        f = open('./data/log','a')
        f.write(str(int(time.time()))+'[post]Button was pushed\n')
        f.close()
    except:
        return '成功ログ記録に失敗しました。操作をやり直してください。'

    redirect(mainURL, 301)

# --------------------------
# Configページ
# --------------------------

@get('/config/')
def config():
    return template('config',)

@route('/config/',method='POST')
def do_config():
    try:
        line = request.forms.get('line')
        num = request.forms.get('num')
        speed = request.forms.get('speed')

        line = int(line)
        num = int(num)
        speed = int(speed)
    except:
        try:
            f = open('./data/log','a')
            f.write(str(int(time.time()))+'[Error][Config]get data ERROR\n')
            f.close()
            return('初期引数読み込みでエラーが発生しました。')
        except:
            return('初期引数読み込みでエラーが発生しました。ログ記録も失敗しました。')

    try:
        retext = '設定の変更が完了しました。<br/>'#完了文の生成

        #0は設定を現状維持
        if(line != 0):
            f = open('./data/line','w')
            f.write(str(line))
            f.close()
            retext += '<br/>閾値：' + str(line)
        else:
            retext += '<br/>閾値：変化なし'
    except:
        try:
            f = open('./data/log','a')
            f.write(str(int(time.time()))+'[Error][Config]line:'+str(line)+' Write ERROR\n')
            f.close()
            return('Lineの書き込みでエラーが発生しました。')
        except:
            return('Lineの書き込みでエラーが発生しました。ログ記録も失敗しました。')

    try:
        if(num != 0):
            f = open('./data/num','w')
            f.write(str(num))
            f.close()
            retext += '<br/>累計数：' + str(num)
        else:
            retext += '<br/>累計数：変化なし'
    except:
        try:
            f = open('./data/log','a')
            f.write(str(int(time.time()))+'[Error][Config]Num:'+str(num)+' Write ERROR\n')
            f.close()
            return('Numの書き込みでエラーが発生しました。')
        except:
            return('Numの書き込みでエラーが発生しました。ログ記録も失敗しました。')

    try:
        if(speed != 0):
            f = open('./data/speed','w')
            f.write(str(speed))
            f.close()
            retext += '<br/>秒速：' + str(speed)
        else:
            retext += '<br/>秒速：変化なし'
    except:
        try:
            f = open('./data/log','a')
            f.write(str(int(time.time()))+'[Error][Config]Speed:'+str(speed)+' Write ERROR\n')
            f.close()
            return('Speedの書き込みでエラーが発生しました。')
        except:
            return('Speedの書き込みでエラーが発生しました。ログ記録も失敗しました。')

    try:
        f = open('./data/log','a')
        f.write(str(int(time.time()))+'[Config]line:'+str(line)+' num:'+str(num)+' speed:'+str(speed)+'\n')
        f.close()
        return (retext)
    except:
        try:
            f = open('./data/log','a')
            f.write(str(int(time.time()))+'[Error][Config]line:'+str(line)+' num:'+str(num)+' speed:'+str(speed)+'\n')
            f.close()
            return ('最終ロフ記録に失敗しました。')
        except:
            return('最終ログ記録に失敗しました。ログも記録できませんでした。')

run(host='202.222.13.37', port=80, debug=True)