import requests
import os


def upload_and_post(instance_url, token, text, file_path, gen_path, reply_id):
    # --- Step 1: ファイルをアップロード ---
    upload_url = f"https://{instance_url}/api/drive/files/create"
    
    with open(file_path, "rb") as f:
        # ドライブへのアップロードは multipart/form-data 形式

        files = {
            "file": (gen_path, f)
        }
        # トークンもフォームデータとして送信
        payload = {
            "i": token
        }
        
        upload_res = requests.post(upload_url, data=payload, files=files)


    if upload_res.status_code != 200:
        print("アップロード失敗")
        return None

    file_id = upload_res.json()["id"]
    print(f"ファイルアップロード完了 ID: {file_id}")

    # --- Step 2: ノートを投稿 ---
    post_url = f"https://{instance_url}/api/notes/create"
    
    post_data = {
        "i": token,
        "replyId": reply_id,
        "text": text,
        "fileIds": [file_id] # 配列で渡す（複数可）
    }

    response = requests.post(post_url, json=post_data)
    
    if response.status_code == 200:
        print("添付付き投稿成功！")
        return response.json()
    else:
        print("投稿失敗")
        return None

# # 使い方
# host = os.environ.get("MISSKEY_HOST")
# token = os.environ.get("MISSKEY_TOKEN")
# FILE = "output_neural2.mp3" # 投稿したい画像パス
# upload_and_post(host, token, "画像付き投稿テスト！", FILE)
