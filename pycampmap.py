import requests
import json
from flask import Flask, render_template
import os
import requests
from bs4 import BeautifulSoup

import ScrapePyCampList as SPCL


app = Flask(__name__)

prefnames = ('_', '北海道', '青森', '岩手', '宮城', '秋田', '山形', '福島', '茨城', '栃木',
            '群馬', '埼玉', '千葉', '東京', '神奈川', '新潟', '富山', '石川', '福井', '山梨', 
            '長野', '岐阜', '静岡', '愛知', '三重', '滋賀', '京都', '大阪', '兵庫', '奈良', 
            '和歌山', '鳥取', '島根', '岡山', '広島', '山口', '徳島', '香川', '愛媛', '高知', 
            '福岡', '佐賀', '長崎', '熊本', '大分', '宮崎', '鹿児島', '沖縄')


prefdic = {'北海道':1, '青森':2, '岩手':3, '宮城':4, '秋田':5, '山形':6, '福島':7, '茨城':8, '栃木':9,
            '群馬':10, '埼玉':11, '千葉':12, '東京':13, '神奈川':14, '新潟':15, '富山':16, '石川':17, '福井':18, '山梨':19,
            '長野':20, '岐阜':21, '静岡':22, '愛知':23, '三重':24, '滋賀':25, '京都':26, '大阪':27, '兵庫':28, '奈良':29,
            '和歌山':30, '鳥取':31, '島根':32, '岡山':33, '広島':34, '山口':35, '徳島':36, '香川':37, '愛媛':38, '高知':39,
            '福岡':40, '佐賀':41, '長崎':42, '熊本':43, '大分':44, '宮崎':45, '鹿児島':46, '沖縄':47}

area = [
        [ 1, '', '#aaa'], [ 2, '', '#aaa'], [ 3, '', '#aaa'], [ 4, '', '#aaa'], [ 5, '', '#aaa'],
        [ 6, '', '#aaa'], [ 7, '', '#aaa'], [ 8, '', '#aaa'], [ 9, '', '#aaa'], [10, '', '#aaa'],
        [11, '', '#aaa'], [12, '', '#aaa'], [13, '', '#aaa'], [14, '', '#aaa'], [15, '', '#aaa'],
        [16, '', '#aaa'], [17, '', '#aaa'], [18, '', '#aaa'], [19, '', '#aaa'], [20, '', '#aaa'],
        [21, '', '#aaa'], [22, '', '#aaa'], [23, '', '#aaa'], [24, '', '#aaa'], [25, '', '#aaa'], 
        [26, '', '#aaa'], [27, '', '#aaa'], [28, '', '#aaa'], [29, '', '#aaa'], [30, '', '#aaa'], 
        [31, '', '#aaa'], [32, '', '#aaa'], [33, '', '#aaa'], [34, '', '#aaa'], [35, '', '#aaa'],
        [36, '', '#aaa'], [37, '', '#aaa'], [38, '', '#aaa'], [39, '', '#aaa'], [40, '', '#aaa'],
        [41, '', '#aaa'], [42, '', '#aaa'], [43, '', '#aaa'], [44, '', '#aaa'], [45, '', '#aaa'],
        [46, '', '#aaa'], [47, '', '#aaa']
        ]
def parse_pycampPref():
    '''
    PyCamp開催県情報をパースして，connpassの開催県情報をタプルで返す
    '''
    prefs = list()
    url = 'https://www.pycon.jp/support/bootcamp.html#id8'
    res = requests.get(url)
    content = res.content
    soup = BeautifulSoup(content, 'html.parser')
    for pref in soup.find_all('strong'):
        prefs.append(str(pref).replace('<strong>','').replace('</strong>',''))

    return prefs

@app.route('/')
def main():
    prefs = parse_pycampPref()

    for pref in prefs:
        i = prefdic[pref]
        area[i - 1] = [i, pref, '#8888ff']

    return render_template('index.html', title='Pycamp Map', area=area)


@app.route('/old')
def old():
    content = SPCL.api()
    
    for i in range(1, 48):
        if str(i) in content:
            if content[str(i)] == 1:
                area[i-1] = [i, prefnames[i], '#8888ff']
            else:
                area[i-1] = [i, prefnames[i], '#cc00cc']
            
    return render_template('index2.html', title='Pycamp Map(old version)', area=area)



@app.route('/update')
def update():
    SPCL.update()
    return 'Done' 


if __name__ == '__main__':
    app.run(host=os.environ.get("IP", '0.0.0.0'), port=int(os.environ.get("PORT", 5000)), debug=False)

