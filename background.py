# coding: UTF-8
# speed計算バックグラウンドプログラム

import time

start = 0

while(True):
    try:
        # データ読み込み
        f = open('./data/timedata', 'r')
        data = f.readlines()
        f.close()

        length = len(data)

        # 数値データに変換
        dataCon = []
        for i in range(0, length):
            dataCon.append(float(data[i]))

        # 境界時刻の取得
        line = time.time() - 1

        # 境界時刻の位置を探す
        while(start < length and dataCon[start] < line):
            start += 1

        # 個数情報を書き込む
        f = open('./data/speed', 'w')
        f.write(str(length - start))
        f.close()

        # logを出力
        f = open('./data/log', 'a')
        f.write(str(int(time.time())) + '[back]speed:' + str(length - start) + '\n')
        f.close()

        time.sleep(0.5)
    except:
        try:
            f = open('./data/log', 'a')
            f.write(str(int(time.time())) + '[Error][back]Background ERROR\n')
            f.close()
        except:
            print('[Error][back]Background ERROR\n')
