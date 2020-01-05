import arxiv
from googletrans import Translator
import requests
import boto3
import pickle

# ユーザ設定
EVENT_NAME1 = "example_line"  # 自分のWebhooksのEvent Name
EVENT_NAME2 = "example_slack"  # 自分のWebhooksのEvent Name
WEBHOOKS_KEY = "EXAMPLE"  # 自分のWebhooksのキー
API_URL1 = "https://maker.ifttt.com/trigger/{}/with/key/{}".format(EVENT_NAME1, WEBHOOKS_KEY)
API_URL2 = "https://maker.ifttt.com/trigger/{}/with/key/{}".format(EVENT_NAME2, WEBHOOKS_KEY)

# 論文検索クエリ
QUERY = """\
cat: cs.CV AND \
abs: 'pose estimation' \
"""

def get_papers(start=0):
    """
    クエリにしたがって一度に100件取得，投稿日が新しい順
    input:
        int: start
            論文取得開始オフセット
    output:
        list: papers
            論文リスト
    """
    papers = arxiv.query(
        query=QUERY,
        max_results=100,
        start=start,
        sort_by="submittedDate")
    
    return papers


def lambda_handler(event, context):
    # s3
    s3 = boto3.resource("s3")
    BUCKET = "example_backet"  # s3のバケット名
    KEY   = "example.pkl"  # ファイル名
    
    obj = s3.Object(BUCKET, KEY)
    try: 
        sended_papers = pickle.loads(obj.get()['Body'].read())
    except:
        # 初回用
        sended_papers = []
        obj.put(Body=pickle.dumps(sended_papers))
    
    # main
    translator = Translator()
    send_flag = 1
    start = 0
    while(send_flag):
        papers = get_papers(start=start)
        for paper in papers:
            if paper["id"] in sended_papers:
                pass
            else:
                summary = paper["summary"].replace("\n", " ")
                text1 = " ".join([
                    "TITLE:<br>", paper["title"], "<br><br>", 
                    "PUBLISHED:<br>", paper["published"], "<br><br>", 
                    "URL:<br>", paper["pdf_url"], "<br><br>", ])
                text2 = " ".join([
                    "SUMMARY:<br>", summary, "<br><br>"])
                text3 = " ".join([
                    "SUMMARY_JP:<br>", translator.translate(summary, dest='ja').text])

                # POST to Webhooks
                response = requests.post(API_URL1, data={"value1": text1, "value3": text3})  # LINE用
                response = requests.post(API_URL2, data={"value1": text1, "value2": text2, "value3": text3})  # Slack用

                # 送信済み論文listの更新
                sended_papers.append(paper["id"])
                obj.put(Body=pickle.dumps(sended_papers))
                send_flag = 0
                break
        start+=100
