from bottle import route, response, run
import json
import ScrapePyCampList as SPCL


@route('/api', method=['GET'])
def resp():
    '''
    呼び出されたらScrapePyCampListのapi()を呼び出して，帰ってきた辞書をjson形式で返す
    '''
    dic = SPCL.api()
    return json.dumps(dic)

@route('/update', method=['GET'])
def update():
    SPCL.update()
    return 0

def main():
    '''
    bottleの起動
    '''
    run(host='0.0.0.0', port='5963')

if __name__ == "__main__":
        main()

