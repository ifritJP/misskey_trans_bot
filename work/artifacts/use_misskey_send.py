import requests
import os




# 指定フォルダのファイルをリストアップする
def ls_files( instance_url, token, folderId ):
    upload_url = f"https://{instance_url}/api/drive/files"

    headers = {'Content-type': 'application/json'}
    
    payload = {
        "i": token,
        "limit": 100,
        "folderId": folderId,
    }

    upload_res = requests.post(upload_url, headers=headers, json=payload)

    print( upload_res, upload_res.json() )
    if upload_res.status_code != 200:
        print("失敗")
        return None

    jsonObj = upload_res.json()
    print( jsonObj )

    return jsonObj


path2folderId = {}
folderId2path = {}

# 指定フォルダからの path の folderId を取得する
def find_dir( instance_url, token, folderId, path ):
    if path in path2folderId:
        print( "hit", path )
        return path2folderId[ path ]
    
    upload_url = f"https://{instance_url}/api/drive/folders"

    headers = {'Content-type': 'application/json'}

    if folderId is None:
        parent = "/"
    else:
        parent = folderId2path[ folderId ]
    

    for name in path.split( "/" ):
        parent = os.path.join( parent, name )
        print( name, folderId )

        if parent in path2folderId:
            print( "hit", parent )
            folderId = path2folderId[ parent ]
        else:
            payload = {
                "i": token,
                "limit": 100,
                "folderId": folderId,
            }
        
            upload_res = requests.post(upload_url, headers=headers, json=payload)
        
            print( upload_res, upload_res.json() )
            if upload_res.status_code != 200:
                print("失敗")
                return None
    
            jsonObj = upload_res.json()
            print( jsonObj )
    
    
            folderId = None
            for item in jsonObj:
                if item[ "name" ] == name:
                    folderId = item[ "id" ]
                    break
            if folderId is None:
                return None
    
            path2folderId[ parent ] = folderId
            folderId2path[ folderId ] = parent

    return folderId

# 指定フォルダからの相対パス path のフォルダを作成する
def make_dirs( instance_url, token, folderId, path ):
    upload_url = f"https://{instance_url}/api/drive/folders/create"

    headers = {'Content-type': 'application/json'}

    if folderId is None:
        work_path = "/"
    else:
        work_path = folderId2path[ folderId ]

    
    for name in path.split( "/" ):
        sub_id = find_dir( instance_url, token, folderId, name )
        if sub_id is None:
            print( name, folderId )
            payload = {
                "i": token,
                "name": name,
                "parentId": folderId,
            }
            
            upload_res = requests.post(upload_url, headers=headers, json=payload)
            
            print( upload_res, upload_res.json() )
            if upload_res.status_code != 200:
                print("失敗")
                return None
            
            jsonObj = upload_res.json()
            print( "result", jsonObj )
            
            folderId = jsonObj[ "id" ]

            work_path = os.path.join( work_path, name )
            path2folderId[ work_path ] = folderId
            folderId2path[ folderId ] = work_path
            
        else:
            folderId = sub_id

    return folderId

# file_path のファイルを、 サーバの gen_path にアップロードする
def upload( instance_url, token, file_path, gen_path ):
    parent = os.path.dirname( gen_path )
    print( "parent", parent )
    folderId = make_dirs( instance_url, token, None, parent )

    return upload_with_folderId( instance_url, token, file_path,
                                 os.path.basename( gen_path ), folderId )
    

# file_path のファイルを、 サーバの folderId に gen_name としてアップロードする
def upload_with_folderId( instance_url, token, file_path, gen_name, folderId ):
    print( "upload_with_folderId", gen_name, folderId )
    
    # --- Step 1: ファイルをアップロード ---
    upload_url = f"https://{instance_url}/api/drive/files/create"
    
    with open(file_path, "rb") as f:
        # ドライブへのアップロードは multipart/form-data 形式

        # folderId を指定すると何故かエラーする
        files = {
            "file": (gen_name,f),
        }
        # トークンもフォームデータとして送信
        payload = {
            "i": token,
            "folderId": folderId,
            "name": gen_name,
        }
        
        upload_res = requests.post(upload_url, data=payload, files=files)


    if upload_res.status_code != 200:
        print("アップロード失敗", upload_res.json())
        return None

    file_id = upload_res.json()["id"]
    print(f"ファイルアップロード完了 ID: {file_id}")

    return file_id

def post(instance_url, token, text, reply_id, file_id_list ):
    
    # --- Step 2: ノートを投稿 ---
    post_url = f"https://{instance_url}/api/notes/create"
    
    post_data = {
        "i": token,
        "replyId": reply_id,
        "text": text,
    }

    if not file_id_list is None:
        post_data[ "fileIds" ] = file_id_list


    response = requests.post(post_url, json=post_data)
    
    if response.status_code == 200:
        print("投稿成功！")
        return response.json()
    else:
        print("投稿失敗")
        return None



# file_path のファイルをアップロードして、 text の内容をポストする。
# どうやら、同じ内容のファイルをアップロードすると、
# gen_path に何を指定しても、同じ内容のファイルとしてアップロードされるらしい
def upload_and_post(instance_url, token, text, file_path, gen_path, reply_id):
    
    # --- Step 1: ファイルをアップロード ---
    file_id = upload( instance_url, token, file_path, gen_path )

    if file_id is None:
        file_id_list = None
    else:
        file_id_list = [ file_id ]

    return post( instance_url, token, text, reply_id, file_id_list )


def test():

    # API リクエストリミットになった時に、その解除時間を確認する場合は以下を実行
    # date -d @1766476802  ←← 1766476802 はレスポンスに返ってきた値
    # 基本的には 45 分程度で解除される
    
    host = os.environ.get("MISSKEY_HOST")
    token = os.environ.get("MISSKEY_TOKEN")
    upload(host, token, "test.txt", "2025/12/test.txt")
    upload(host, token, "test2.txt", "2025/11/hoge.txt")

    # ls_dir(host, token )
    #ls_files(host, token )
    # find_dir( host, token, None, "2025/12" )
    # find_dir( host, token, None, "2025/12" )
    # make_dirs( host, token, None, "2025/11" )
    # make_dirs( host, token, None, "2025/11" )

    
