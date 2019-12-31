# sending_of_paper_bot

## require
### module
`pip install arxiv`<br>
`pip install googletrans`

### IFTTT(2019.12現在)
#### 登録
https://ifttt.com/

#### THISの設定
- 右上のアイコンからCreate(https://ifttt.com/create)
- Thisをクリック
- webhooksを検索
- Receive a web request
- 任意のEvent Name

#### THATの設定
- Thatをクリック
- 連携先を検索(twitter, LINE, etc...)
- (LINEの場合)Recipient…1:1でLINE Notifyから通知を受け取る
- (LINEの場合)Message…{{Value1}}に文字列が渡される

#### webhooksのキー確認
- 右上のアイコンからMy services
- Webhooks
- Setting
- URL: https://maker.ifttt.com/use/YOUR_KEY

## usage

## issue
LINEだと英語abstractで文字列が途切れる．

## references
https://note.nkmk.me/python-arxiv-api-download-rss/ <br>
https://qiita.com/sugup/items/31911ae21c17a1de89ad

