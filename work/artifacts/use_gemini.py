# To run this code you need to install the following dependencies:
# pip install google-genai


import os
import io
import re
import json
import random

from google import genai
from google.genai import types


def generate(txt, link_list):

    prompt = """
末尾に添付した日本語を英語に翻訳してください。
出来るだけシンプルな文法を使って翻訳してください。
レスポンスは次の JSON 形式で返してください。
Markdown は使わずに application/json 形式にしてください。
{
   "result": "ここに翻訳後の結果を入れる",
   "word-list": [ { "word": "", "mean": "" } ],
   "comment": "ここに添付した日本後の内容に対するコメントを入れる",
}
中学生レベルで難しい単語がある場合は、単語と意味のリスト(word-list)を追加してください。
word の値には、英単語を入れてください。
mean の値には、翻訳元の文の日本語訳の何に対応するのかを簡潔に説明してください。
comment の値には、添付した日本語の内容に関するファクトチェック。
さらに、その内容の専門家としての様々な観点(肯定、批評等)のコメントを日本語で入れてください。
長さは JSON 全体で最大でも 2000 文字程度にしてください。
"""
    # リンクがある場合はリンクについてのコメントも追加
    if len( link_list ) > 0:
        prompt += """
なお、添付した日本語は次の URL のリンク先の内容に関するコメントです。
リンク先の内容にも考慮に入れて言及してください。
"""
        prompt += "\n".join( link_list )

    prompt += "\n---\n"
    prompt += txt
    
    
    try:
        client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )

        # 使用するモデルの定義。
        # 上限にならないようにランダムで利用するモデルを変更する。 
        # 高精度モデルの比率を挙げるために、定義数を上げる。
        # 本来はリスエスト回数をカウントして越えないように調整した方が良いが
        # 面倒なのでランダムで分散させる。
        # 現状 1 日に 20 回制限なので、普通に考えて 20 回は使わないはず
        model_list =[
            #"gemini-3-flash",
            "gemini-2.5-flash",
            "gemini-2.5-flash",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
        ]
        model = model_list[ random.randint(0,len( model_list ) - 1 ) ]
        print( model )
        
        
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]
        tools = [
            types.Tool(googleSearch=types.GoogleSearch(
            )),
        ]
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_budget=-1,
            ),
            tools=tools,
        )
    
        result = io.StringIO()
        
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            result.write( chunk.text )
        ans = result.getvalue()
        jsonTxt = re.sub( r"```.*", "", ans )

        jsonObj = json.loads( jsonTxt )
        comment = jsonObj[ "comment" ]
        if len( comment ) > 2800:
            jsonObj[ "comment" ] = comment[ :2800 ] + "..."
        jsonObj["model"] = model
        return jsonObj
    
    except Exception as e:
        print(f"Error: {e}" )
        return None

if __name__ == "__main__":
    print( generate( "本日発表された消費者物価指数についてお報せします。" ) )

