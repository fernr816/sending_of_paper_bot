# sending_of_paper_bot

main.py … ローカル用<br>
lambda_function.py … lambda用

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
- 任意の`Event Name`

#### THATの設定
- Thatをクリック
- 連携先を検索(Slack, LINE, etc...)
- (LINEの場合)Recipient…1:1でLINE Notifyから通知を受け取る
- (LINEの場合)Message…{{Value1}}に文字列が渡される

#### webhooksのキー確認
- 右上のアイコンからMy services
- Webhooks
- Setting
- URL: https://maker.ifttt.com/use/<WEBHOOKS_KEY>

## usage
run `python main.py`

### ユーザ設定
`EVENT_NAME` … IFTTTのTHISで設定した`EventName`<br>
`WEBHOOKS_KEY` … 自分のWebhooksのキー<br>
`BUCKET` … S3のバケット名<br>
`KEY` … S3に保存するpickleファイル名<br>

### 論文検索クエリ
例はcvカテゴリでabstract(summary)に"pose estimation"の語を含むもの

カテゴリ一覧<br>
https://arxiv.org/help/api/user-manual#subject_classifications

### 定期実行
AWS lambdaや研究室のワークステーションで

## issues
LINEだと英語abstractで文字列が途切れる(原因不明)ためLINEには日本語abstract，Slackには英語+日本語abstractを送るという運用…

## references
https://note.nkmk.me/python-arxiv-api-download-rss/ <br>
https://qiita.com/sugup/items/31911ae21c17a1de89ad

