import os
import html

# あなたのAPIキーをここに設定
API_KEY = os.environ.get("GCP_API_KEY")

import requests

def translate_text(text):

    url = "https://translation.googleapis.com/language/translate/v2"
    
    # APIへのパラメータ
    params = {
        "q": text,
        "target": "en",
        "source": "ja",
        "key": API_KEY
    }

    response = requests.post(url, data=params) # POSTの方が長い文章に強いです
    
    if response.status_code == 200:
        result = response.json()
        text = result["data"]["translations"][0]["translatedText"]
        return { "result": html.unescape( text ), "word-list":[] }
    else:
        print({response.status_code}, {response.text})
        return None

# 実行
# print(translate_text("お腹が空きました。", API_KEY))
