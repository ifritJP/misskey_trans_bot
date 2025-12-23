import asyncio
import json
import os
import sys
import websockets
import re
import traceback
from datetime import datetime

import use_translate
import use_text2speech
import use_gemini
import use_misskey_send


host = os.environ.get("MISSKEY_HOST")
token = os.environ.get("MISSKEY_TOKEN")
target_user = os.environ.get("TARGET_USER")

if not host:
    print("Error: MISSKEY_HOST must be set.", file=sys.stderr)
    sys.exit(1)


def process_message( text, note_id ):
    enc = use_gemini.generate( text )
    if enc is None:
        print( "gemini is None" )
        enc = use_translate.translate_text( text )
        print ( enc )

    if enc is None:
        return

    print( "enc", enc )

    encTxt = enc[ "result" ]

    # 現在日時を取得
    output_file = "output.mp3"
    
    use_text2speech.synthesize_text_with_voice_type(
        encTxt, output_file,
        language_code = "en-US",
        voice_name = "en-US-Chirp-HD-D",
        speed = 0.75 )

    word_desc = ""
    for item in enc[ "word-list" ]:
        word_desc += "%s: %s\n" %(item["word"], item["mean"])
    if word_desc != "":
        encTxt += "\n-----\n"
        encTxt += word_desc

    now = datetime.now()
    gen_file = now.strftime("%Y/%m/%Y_%m_%d_%H-%M-%S-" + output_file )

    use_misskey_send.upload_and_post(
        host, token, encTxt, output_file, gen_file, note_id )
    

async def process_note( note, target_user ):
    text = note.get("text")
    created_at = note.get("createdAt") # ISO 8601 UTC
    user = note.get("user", {}).get("username")
    note_id = note.get( "id" )
    
    # "本文（text）が存在する投稿のみを表示する。"
    if text:
        # Convert to local time
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        local_time = dt.astimezone().strftime("%Y-%m-%d %H:%M:%S")
        
        # Output format: [YYYY-MM-DD HH:MM:SS] @username: text
        print(f"[{local_time}] {note_id} @{user}: {text}")
        sys.stdout.flush()
        if user == target_user:
            text = re.sub( "http[^\n]+", "", text )
            process_message( text, note_id )

async def stream():
    # Use wss:// for secure websocket
    url = f"wss://{host}/streaming"
    if token:
        url += f"?i={token}"
    else:
        print("Warning: MISSKEY_TOKEN is not set. Connecting as guest.", file=sys.stderr)

    while True:
        try:
            async with websockets.connect(url) as ws:
                print(f"Connected to {host}", file=sys.stderr)

                # Connect to globalTimeline channel
                resp = await ws.send(json.dumps({
                    "type": "connect",
                    "body": {
                        #"channel": "localTimeline",
                        "channel": "homeTimeline",
                        "id": "antigravity-gtl"
                    }
                }))
                

                async for message in ws:
                    data = json.loads(message)
                    # Check if it's a note event from our channel
                    if data.get("type") == "channel" and data.get("body", {}).get("id") == "antigravity-gtl":
                        body = data.get("body", {})
                        if body.get("type") == "note":
                            note = body.get("body", {})
                            await process_note( note, target_user )
        except Exception as e:
            print(f"Error: Reconnecting in 5 minuts...", file=sys.stderr)
            traceback.print_exc()

            await asyncio.sleep( 5 * 60 )

def run():
    try:
        asyncio.run(stream())
    except KeyboardInterrupt:
        print("\nExit.", file=sys.stderr)
        sys.exit(0)
    
if __name__ == "__main__":
    run()
