# Python Boot Camp 開催県を可視化する

Python Boot Campの開催地一覧( https://www.pycon.jp/support/bootcamp.html#id8 )を元に開催県を塗りつぶした白地図を描きます。

## Python Boot Campについて

Python Boot Campは一般社団法人PyConJPが開催している初心者向けのPythonチュートリアルイベントです。
https://www.pycon.jp/support/bootcamp.html

日本各地でPythonが盛り上がることを目的のひとつに掲げ，東京を覗く46道府県での開催を目指しています。

## このアプリを作った背景

46道府県のうち，どこで開催済みで，どこが開催予定で，どこがまだなのか，一目でわかる地図があったら便利だな〜と思い，勉強を兼ねて作成することにしました。

## 仕組み

Python Boot Campのページにある開催地リストからConnpassページへのリンクを取得
↓
Connpassページの情報をもとに会場の県名と開催済みかどうかを取得
↓
開催済み，開催予定，未開催に塗り分けた白地図を描画（https://takemaru-hirai.github.io/japan-map/ をちょっと改造して利用）

## 工夫

- 会場の住所に県名が入っているとは限らないので郵便番号を使って県名を取得しています
- 情報の取得を毎回やると処理が重いので，取得処理と表示処理を分けています
- 取得処理(/update)は個人サーバーからcronで毎日1回叩いています
- このままでIBM Bluemix上で動くようにしてあります

## License

This app is released under the MIT License.

## history
- 2018/02/17 個人サーバー上で動くバージョンを公開
- 2018/02/18 IBM Bluemix上で動くようにProcfile,runtime.txtを書きました
- 2018/03/25 Python Boot Campの開催ページのテンプレート変更に対応しました
