import requests
import json
import os


def get_local_timeline( token, host = "misskey.io" ):
    url = f"https://{host}/api/notes/timeline"
    
    notes_found = []
    until_id = None

    print( token )
    
    data = {
        "i": token,
        "limit": 1,
    }
    if until_id:
        data["untilId"] = until_id
        
    response = requests.post(url, json=data)
    
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return None
    
    notes = response.json()
    if not notes:
        return None
    
    print( notes )

    if len( notes ) == 0:
        return None
    return notes[0]

def test():
    token = os.environ.get("MISSKEY_TOKEN")
    
    # 実行
    note = get_local_timeline(token)

    if note:
        # 結果の表示（新しい順に表示されます）
        user = note['user']['username']
        text = note.get('text', '(本文なし)')
        print(f"[{note['createdAt']}] @{user}: {text[:30]}...")
