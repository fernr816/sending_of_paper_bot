from pathlib import Path
import arxiv
from googletrans import Translator
import requests

# ユーザ設定
EVENT_NAME1 = "send_paper_line"  # 自分のWebhooksのEvent Name
EVENT_NAME2 = "send_paper_slack"  # 自分のWebhooksのEvent Name
WEBHOOKS_KEY = ""  # 自分のWebhooksのキー
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


if __name__ == "__main__":
    p = Path("./sended_papers.txt")  # 送信済み論文list
    p.touch()
    with p.open(mode="r") as f:
        sended_papers = [s.strip() for s in f.readlines()]

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
                response = requests.post(API_URL1, data={"value1": text1, "value3": text3})  # LINE
                response = requests.post(API_URL2, data={"value1": text1, "value2": text2, "value3": text3})  # Slack

                # 送信済み論文listの更新
                with p.open(mode="a") as f:
                    f.write(paper["id"] + "\n")
                    send_flag = 0
                break
        start+=100
