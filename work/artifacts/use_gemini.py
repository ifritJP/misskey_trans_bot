# To run this code you need to install the following dependencies:
# pip install google-genai


import os
import io
import re
import json

from google import genai
from google.genai import types


def generate(txt):

    prompt = """
次の日本語を英語に翻訳してください。
出来るだけシンプルな文法を使って翻訳してください。
レスポンスは次の JSON 形式で返してください。
Markdown は使わずに application/json 形式にしてください。
{
   "result": "ここに翻訳後の結果を入れる",
   "word-list": [ { "word": "", "mean": "" } ],
}
中学生レベルで難しい単語がある場合は、単語と意味のリスト(word-list)を追加してください。
単語は英単語を入れてください。
意味は翻訳元の文の語から拾ってください。
-----
"""
    prompt += txt
    
    
    try:
        client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )
    
        #model = "gemini-2.5-flash"
        model = "gemini-2.5-flash-lite"
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
        return json.loads( jsonTxt )
    
    except Exception as e:
        print(f"Error: {e}" )
        return None

if __name__ == "__main__":
    print( generate( "本日発表された消費者物価指数についてお報せします。" ) )

