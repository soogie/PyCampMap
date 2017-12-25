import requests
from bs4 import BeautifulSoup
import japanmap as jm
import json
from flask import Flask, render_template
import os
app = Flask(__name__)

prefnames = ('_', '北海道', '青森', '岩手', '宮城', '秋田', '山形', '福島', '茨城', '栃木',
            '群馬', '埼玉', '千葉', '東京', '神奈川', '新潟', '富山', '石川', '福井', '山梨', 
            '長野', '岐阜', '静岡', '愛知', '三重', '滋賀', '京都', '大阪', '兵庫', '奈良', 
            '和歌山', '鳥取', '島根', '岡山', '広島', '山口', '徳島', '香川', '愛媛', '高知', 
            '福岡', '佐賀', '長崎', '熊本', '大分', '宮崎', '鹿児島', '沖縄')

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
    

@app.route('/')
def simple():

    main()

    return render_template('index.html', title='flask test', area=area) #変更



def parse_compass(url):
    res = requests.get(url)
    content = res.content
    soup = BeautifulSoup(content, 'html.parser')
    info = soup.find_all('div', class_='group_inner clearfix')
    
    address = info[0].select('ul')[3].select('li')[1].get_text()
    return address

def pref_code(address):
    # zip = address[1:9] # これでは甘かった
    start = address.find('〒')
    zip = address[start+1:start+9]
    
    res = requests.get('http://geoapi.heartrails.com/api/json?method=searchByPostal&postal=' + zip)
    try:
        prefecture = res.json()['response']['location'][0]['prefecture']
        return jm.pref[prefecture]
    except:
        # 郵便番号がだめなら所在地から無理やり
        for key, value in jm.pref.items():
            if key in address:
                return value
        # それでもだめなら
        return 0


def main():
    url = 'https://www.pycon.jp/support/bootcamp.html#id8'
    res = requests.get(url)
    content = res.content
    soup = BeautifulSoup(content, 'html.parser')
    referenceexternals = soup.find_all('a', class_='reference external')
    
    
    for referenceexternal in referenceexternals:
        url = referenceexternal['href']
        name = referenceexternal.text
        if ' in ' in name:
            address = parse_compass(url)
            code = pref_code(address)
            #print(name, url, address, code)
            area[code - 1] = [code, prefnames[code], '#00ffff']


if __name__ == '__main__':
    #main()
    app.run(host=os.environ.get("IP", '0.0.0.0'), port=int(os.environ.get("PORT", 5000)), debug=False)