from google.cloud import texttospeech
import os

# あなたのAPIキーをここに設定
API_KEY = os.environ.get("GCP_API_KEY")

def synthesize_text_with_voice_type(
        text, output_filename, language_code, voice_name, speed):
    """
    指定した音声タイプ（voice_name）でテキストを音声に変換する
    """
    # クライアントの初期化
    client = texttospeech.TextToSpeechClient(
        client_options={"api_key": API_KEY}
    )
    

    # 入力テキストの設定
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # 音声の選択設定
    # voice_name に 'ja-JP-Neural2-B' などを指定することでタイプが決まる
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    # オーディオ設定（ファイル形式）
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        # 0.25 - 4.0
        speaking_rate=speed,
    )

    # APIリクエストの実行
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # ファイルへの書き出し
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'音声内容を "{output_filename}" に書き込みました。')

# --- 実行例 ---

# # 1. Neural2 (高品質・中価格)
# synthesize_text_with_voice_type(
#     "hello. this is a voice of Neural2.", 
#     "output_neural2.mp3",
#     language_code = "en-US",
#     voice_name = "en-US-Chirp-HD-D",
#     speed = 0.75 )
