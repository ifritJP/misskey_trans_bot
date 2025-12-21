ifndef LOCAL
include ../.info
else
include ../../.info
endif



export GOOGLE_SDK_PYTHON_LOGGING_SCOPE=google
export GOOGLE_SDK_PYTHON_LOGGING_SCOPE=google.cloud.library_v1


help:
	@echo make run


run:
	@MISSKEY_HOST=$(MISSKEY_HOST)			\
		MISSKEY_TOKEN=$(MISSKEY_TOKEN)		\
		TARGET_USER=$(TARGET_USER)		\
		GCP_API_KEY=$(GCP_API_KEY)		\
		GEMINI_API_KEY=$(GEMINI_API_KEY)	\
		uv run main.py



UUID:=$(shell uuid -v 4)
#PERMISSION=read:messaging,write:messaging,write:chat,read:chat,write:notes

#PERMISSION=write:messaging,write:chat,write:notes,read:account,read:blocks,read:drive,read:favorites,read:following,read:messaging,read:mutes,read:notifications,read:reactions,read:pages,read:page-likes,read:user-groups,read:channels,read:gallery,read:gallery-likes,read:flash,read:flash-likes,read:invite-codes,read:clip-favorite,read:federation,read:chat

#PERMISSION=write:messaging,write:chat,write:notes,read:account,read:blocks,read:drive,read:favorites,read:following,read:messaging,read:mutes,read:notifications,read:reactions,read:pages,read:page-likes,read:user-groups,read:channels,read:gallery,read:gallery-likes,read:flash,read:flash-likes,read:clip-favorite,read:federation,read:chat

PERMISSION=write:messaging,write:chat,write:notes,read:account,read:blocks,read:drive,write:drive,read:favorites,read:following,read:messaging,read:mutes,read:notifications,read:reactions,read:pages,read:page-likes,read:user-groups,read:channels,read:gallery,read:gallery-likes,read:flash,read:flash-likes,read:clip-favorite,read:federation,read:chat



get_token:
	@echo "https://misskey.io/miauth/$(UUID)?permission=$(PERMISSION)"
	@echo "curl -v -X POST https://misskey.io/api/miauth/$(UUID)/check"

test_token:
	echo '{ "text": "Hello Misskey API World with My Application!" }' | curl https://misskey.io/api/notes/create -X POST -H "Authorization: Bearer $(MISSKEY_TOKEN)" -H 'Content-Type: application/json' -d @-



# read:account	アカウントの情報を見る
# read:blocks	ブロックを見る
# read:drive	ドライブを見る
# read:favorites	お気に入りを見る
# read:following	フォローの情報を見る
# read:messaging	チャットを見る
# read:mutes	ミュートを見る
# read:notifications	通知を見る
# read:reactions	リアクションを見る
# read:pages	ページを見る
# read:page-likes	ページのいいねを見る
# read:user-groups	ユーザーグループを見る
# read:channels	チャンネルを見る
# read:gallery	ギャラリーを見る
# read:gallery-likes	ギャラリーのいいねを見る
# read:flash	Playを見る
# read:flash-likes	Playのいいねを見る
# read:admin:abuse-user-reports	ユーザーからの通報を見る
# read:admin:index-stats	データベースインデックスに関する情報を見る
# read:admin:table-stats	データベーステーブルに関する情報を見る
# read:admin:user-ips	ユーザーのIPアドレスを見る
# read:admin:meta	インスタンスのメタデータを見る
# read:admin:server-info	サーバーの情報を見る
# read:admin:show-moderation-log	モデレーションログを見る
# read:admin:show-user	ユーザーのプライベートな情報を見る
# read:admin:roles	ロールを見る
# read:admin:relays	リレーを見る
# read:admin:invite-codes	招待コードを見る
# read:admin:announcements	お知らせを見る
# read:admin:avatar-decorations	アバターデコレーションを見る
# read:admin:account	ユーザーに関する情報を見る
# read:admin:emoji	絵文字を見る
# read:admin:queue	ジョブキューに関する情報を見る
# read:admin:drive	ユーザーのドライブの関する情報を見る
# read:admin:ad	広告を見る
# read:invite-codes	招待コードを取得する
# read:clip-favorite	クリップのいいねを見る
# read:federation	連合に関する情報を取得する
# read:chat	チャットを閲覧する
