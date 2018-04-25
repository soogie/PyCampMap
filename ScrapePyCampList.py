import requests
from bs4 import BeautifulSoup
import japanmap as jm
import json
from sendmailgun import sendMessage

prefnames = ('_', '北海道', '青森', '岩手', '宮城', '秋田', '山形', '福島', '茨城', '栃木',
            '群馬', '埼玉', '千葉', '東京', '神奈川', '新潟', '富山', '石川', '福井', '山梨',
            '長野', '岐阜', '静岡', '愛知', '三重', '滋賀', '京都', '大阪', '兵庫', '奈良',
            '和歌山', '鳥取', '島根', '岡山', '広島', '山口', '徳島', '香川', '愛媛', '高知',
            '福岡', '佐賀', '長崎', '熊本', '大分', '宮崎', '鹿児島', '沖縄')


def parse_connpass(url):
    '''
    input:
      url: connpassのPyCamp開催情報URL
    output:
      address: 郵便番号を含むPyCamp開催会場の所在地
      status: 開催済みかどうか　1=開催済み 0=開催予定
    '''
    res = requests.get(url)
    content = res.content
    soup = BeautifulSoup(content, 'html.parser')
    info = soup.find_all('div', class_='group_inner clearfix')
    statusinfo = soup.find_all('span', class_='label_status_event close')
    if len(info[0].select('ul')[3].select('li'))== 3:
        address = info[0].select('ul')[3].select('li')[1].get_text()
    elif len(info[0].select('ul')[4].select('li'))== 3:
        address = info[0].select('ul')[4].select('li')[1].get_text()
    else:
        address = 'サイトの構成が変わっている'
        sendMessage('parse_connpassでエラー', 'サイトの構成が変わっているようです。確認してください¥n¥n' + url)
    if len(statusinfo)>0:
        status = 1 # 終了
    else:
        status = 0 # 開催予定
    return address, status


def pref_code(address):
    '''
    input:
      address: 郵便番号を含む開催会場の所在地
    output:
      県コード(1〜43) 
      該当する県を見つけられなかった場合は0
    '''
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
        sendMessage('pref_codeで失敗', '郵便番号でも所在地でも都道府県が指定できませんでした。確認してください¥n¥n' + address)
        return 0

def parse_pycamp():
    '''
    PyCamp開催情報をパースして，connpassの開催情報URLをすべて返す
    '''
    url = 'https://www.pycon.jp/support/bootcamp.html#id8'
    res = requests.get(url)
    content = res.content
    soup = BeautifulSoup(content, 'html.parser')
    return soup.find_all('a', class_='reference external') 


def api():
    '''
    PyCampの開催地リストを取得して，県コードをキー，開催済みかどうかを値とする辞書を返す
    '''
    with open('info.dic') as f:
        response = json.loads(f.read())
    return response

def update():
    '''
    PyCampの開催地リストを取得して，県コードをキー，開催済みかどうかを値とする辞書をjsonで保存
    '''
    pycamps = parse_pycamp()
    response = {}
    for pycamp in pycamps:
        url = pycamp['href']
        name = pycamp.text

        if ' in ' in name:
            address, status = parse_connpass(url)
            code = pref_code(address)
            if code not in response: # まだなければ追加
                response[code] = status
            elif response[code] == 0: # すでにあっても未開催なら上書き
                response[code] = status
            else:
                pass # どちらでもなければなにもしない（開催済み情報がすでにある）
    with open('info.dic', 'w') as f:
        f.write(json.dumps(response))

    return 0

if __name__ == '__main__':
    update()
    print(api())

