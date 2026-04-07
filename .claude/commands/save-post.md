以下の投稿文をGoogleドキュメントの該当セクションに保存して。

媒体・種別・本文: $ARGUMENTS

save_post.py を使って保存すること。

## 実行手順

1. 引数から以下を読み取る：
   - 媒体（X / TikTok / OC）
   - 種別（例：投票、ジェイどこ動画、放送前リマインド）※省略可
   - 本文（保存する投稿テキスト）

2. 以下のコマンドを実行：

```bash
python save_post.py \
  --媒体 "X" \
  --種別 "投票" \
  --本文 "本文テキスト"
```

種別が不要な場合（TikTokなど）は --種別 を省略する。

3. 保存完了後に以下のURLを表示：
https://docs.google.com/document/d/18joYd8QNFwzLUUz0VFbihK0_Ij1JwpA-n3Y0FbbpZl8/edit

## ドキュメントのセクション構成

### X投稿
- 投票
- 放送前リマインド
- ジェイどこ動画
- HPお知らせ
- 応援素材配布
- アイコンフレーム配布
- タグイベ
- スミンパーティー
- 公式投稿引用

### TikTok投稿
（種別なし）

### OC（オープンチャット）
- 投票リマインド

## 必要なパッケージ（未インストールの場合）

```bash
pip install google-auth google-api-python-client
```

## 認証

環境変数 `GA4_SERVICE_ACCOUNT_KEY` にサービスアカウントのJSONキーが必要。
未設定の場合はエラーになるので、実行前に確認すること。
