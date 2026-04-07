#!/usr/bin/env python3
"""
import_keep.py — JAYBIRDSドキュメントに見出し構造＋全テンプレートを一括書き込み

必要なパッケージ:
  pip install google-auth google-api-python-client
"""

import json
import os
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build

DOCUMENT_ID = "18joYd8QNFwzLUUz0VFbihK0_Ij1JwpA-n3Y0FbbpZl8"
SCOPES = ["https://www.googleapis.com/auth/documents"]

SEP = "━━━━━━━━━━━━━━━━━━━━━━"

# ──────────────────────────────────────────────────────────────────────────────
# 全テンプレートデータ
# 構造: [ (セクション見出し, [ (サブセクション見出し or None, [ (タイトル, 本文), ... ]), ... ]), ... ]
# ──────────────────────────────────────────────────────────────────────────────
DOCUMENT_DATA = [
    ("# X投稿", [
        ("## HPお知らせ", [
            ("HP開設",
             "⋱ 💙JAYBIRDS HP公開🪶 ⋰\n\nJAYBIRDS HPを公開しました🎉\n\n✦ 応援情報\n✦ 動画一覧\n✦ 応援ガイド\n✦ 布教素材\n(随時更新予定)\n\nなど応援に役立つ情報をまとめています！\nぜひブックマークを📌💙\n\n🔗 https://x.gd/vja9F\n\n#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"),
            ("🇬🇧HP開設",
             "⋱ 💙 JAYBIRDS SITE IS LIVE 🪶 ⋰\n\nYour go-to hub for all Jay support info is here! 🎉\n\n✦ Updates\n✦ Videos\n✦ Fan Guide\n✦ Promo Materials\n\nBookmark it! 📌💙\n\n🔗 https://x.gd/vja9F\n#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"),
            ("投票ガイド公開",
             "⋱ 💙投票ガイドページ公開🪶 ⋰\n\n🗓️ 初日の1票を逃さないために\n放送前に準備しましょう💪\n\n✦ dアカウント作成（SMS認証まで）\n✦ Leminoアプリ DL＆ログイン\n✦ 海外の方は MNet+アプリ\n\n詳細はこちら🔍ˊ˗\n🔗 https://x.gd/63FPj\n\n#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"),
            ("🇹🇼投票ガイド公開",
             "⋱ 💙 投票指南現已公開 🪶 ⋰\n\n🗓️ 不要錯過第1天的首次投票 —\n請在節目開始前做好準備 💪\n\n✦ 下載並登入 MNet+ 應用程式\n\n🌐 建議使用自動翻譯！\n查看指南請點這裡 🔍ˊ˗\n🔗 https://x.gd/63FPj\n\n#JAY羽ばたくじぇい #ジュアンジェイ"),
            ("番組スケジュール公開",
             "⋱ 💙ロードマップページ公開🪶 ⋰\n\nJAYBIRDSのHPに\n番組スケジュールを追加⟡.*\n\n✦ そもそも日プって何？\n✦ 今後どんな流れで進むの？\n✦ 投票はいつ・何人選べるの？\n\n初めて見る方もこれで安心❣️\n\n🔗 https://x.gd/qN046\n\n#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"),
            ("🇹🇼番組スケジュール公開",
             "⋱ 💙 行程指南現已公開 🪶 ⋰\n\n第一次接觸節目嗎？從這裡開始 ⟡.*\n\n你需要知道的一切 — 全都整理在一頁中 ❣️\n\n🌐 建議使用自動翻譯！\n🔗 https://x.gd/qN046\n\n#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"),
            ("投票ウェイト解説",
             "📊 日プ新世界✦投票の仕組み\n\n‼️徹底検証 & 大解説‼️\n\n✅ 国民票とSEKAI票の違いは？\n✅ 7:3の重みって実際どう効く？\n✅ 1票の価値って何？\n\n👇🏻全部シミュレーターで確かめられます\nhttps://x.gd/w2a6z\n\n全プロデューサー・FDに届け🔍\n\n#PRODUCE101JAPAN新世界\n#101SHINSEKAI #日プ新世界"),
            ("🇹🇼投票ウェイト解説",
             "📊 101新世界✦投票機制\n\n‼️徹底解析 & 大解說‼️\n\n✅ 國民票與SEKAI票有什麼差別？\n✅ 70:30的權重實際上如何影響？\n✅ 1票的價值是什麼？\n\n👇🏻全部都可以用模擬器確認\nhttps://x.gd/w2a6z\n\n傳達給所有製作人・FD🔍\n#PRODUCE101JAPAN新世界\n#101SHINSEKAI #日プ新世界"),
            ("スクショ企画",
             "⋱ 📸 スクショシェア企画 💥⋰\n\nシェアがジェイくんの力になる‼️\nサイトでスクショを引いてポスト🎲\n\nそして…運営だけではスクショが足りない💦\n上手く撮れた方はぜひご提供ください\n\n#ジュアンジェイ #JAYどこ #FINDJAY #PRODUCE101JAPAN新世界\n\n👇🏻まずは一度引いてみて\nhttps://x.gd/FXiv3"),
            ("🇬🇧スクショ企画",
             "⋱ 📸 Spreading Jay's screenshots = direct support‼︎ 💥⋰\n\nDraw a random screenshot & post it on X in one tap✨\nScreenshot donations welcome too🙇\n\n#ChuangJay #JAYどこ #FINDJAY #PRODUCE101JAPAN新世界\n\n▼\nhttps://x.gd/FXiv3"),
            ("🇨🇳スクショ企画",
             "⋱ 📸 擴散莊傑截圖就是支持他的力量‼︎ 💥⋰\n\n隨機抽截圖，一鍵發文到X✨\n也歡迎提供截圖給我們🙇\n#ジュアンジェイ #JAYどこ #FINDJAY #PRODUCE101JAPAN新世界\n\n▼\nhttps://x.gd/FXiv3"),
            ("スクショシェアアプデ",
             "⋱ 📸 スクショシェア機能アップデート 💥⋰\n\n#ジュアンジェイ のスクショを\n\n🪶 各話毎\n🪶 全話\n\nランダムで受け取れるようになりました！\n\n保存・シェア自由です💙\nみんなでジェイ君を盛り上げよう🔥\n\n👉 https://x.gd/FXiv3\n#JAYどこ #FINDJAY #PRODUCE101JAPAN新世界"),
            ("🇬🇧スクショシェアアプデ",
             "📸✨ Screenshot Share feature updated!\n\nGet random screenshots of Chuang Jay —\n🪶 by episode\n🪶 or all episodes together!\n\nFree to save & share 💙\nLet's spread Jay's charm together🔥\n\n👉 https://x.gd/FXiv3\n\n#ChuangJay #FINDJAY #PRODUCE101JAPANShinsekai"),
            ("🇨🇳🇹🇼スクショシェアアプデ",
             "📸✨ 截圖分享功能更新啦！\n\n可以隨機獲得莊宗傑（JAY）的截圖💙\n🪶 按集數選擇\n🪶 或全集一起\n\n可以自由保存・分享🔥\n一起為JAY加油吧！\n\n👉 https://x.gd/FXiv3\n\n#莊宗傑 #FINDJAY #PRODUCE101JAPAN新世界"),
        ]),
        ("## 応援素材配布", [
            ("応援素材配布",
             "⋱ 💙応援素材ページ公開🪶 ⋰\n\nJAYBIRDS のホームページに\nGallery ページを追加しました⟡.*\n\n✦ アイコンフレーム\n✦ X布教画像\n(随時更新予定)\n\nをご用意しています🎉\nご自由にお使いください❣️\n\n🔗 https://x.gd/RkLvF\n\n#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"),
            ("🇬🇧応援素材配布",
             "⋱ 💙SUPPORT MATERIALS PAGE OPEN🪶 ⋰\n\nA Gallery page has been added\nto the JAYBIRDS website⟡.*\n\n✦ Icon Frames\n✦ X Promotion Images\n(More updates coming soon)\n\nAll materials are now available🎉\nFeel free to use them❣️\n\n🔗 https://x.gd/RkLvF\n#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"),
            ("素材シェア企画",
             "⋱ 🎨素材シェア企画🪶 ⋰\n\n応援したいけど素材作りが苦手な方と\n素材を作ってくださる方を\n繋げる企画です💙⟡.*\n\n作った素材をギャラリーに掲載して\n一緒にジェイくんを広めよう🪶✨\n\n詳しくはこちら👇\n🔗 https://x.gd/RkLvF\n\n#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"),
        ]),
        ("## アイコンフレーム配布", [
            ("アイコンフレーム配布",
             "⋱ 💙アイコンフレーム配布‼️🪶 ⋰\n\nJAYBIRDS の皆様、お待たせ致しました⟡.*\n#ジュアンジェイ 応援アイコンフレーム\nを配布いたします🎉\n\n下記リンクよりご自由にお使いください❣️\n\n🔗 https://icondecotter.jp/detail.php?id=107098\n#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"),
            ("布教フライヤー配布",
             "🖼️ 布教フライヤー配布 🎨\n\n有志の方作成の布教フライヤーを配布しています‼️\nSNSでの布教活動、印刷して掲示など\n様々な場面でご活用いただけます🪶\nHPもご確認ください👍\n\n#JAY羽ばたくじぇい\n#ジュアンジェイ\n#PRODUCE101JAPAN新世界"),
            ("🇹🇼布教フライヤー配布",
             "🖼️ 宣傳傳單發放 🎨\n\n由志願者製作的宣傳傳單現正提供下載‼️\n\n可用於SNS宣傳活動，或列印後張貼等\n適用於各種不同場景🪶\n\n也請確認HP👍\n\n#JAY羽ばたくじぇい\n#ジュアンジェイ\n#PRODUCE101JAPAN新世界"),
        ]),
        ("## 公式投稿引用", [
            ("TikTok更新",
             "┊✧ 📹 TikTok up!! ✧┊\n\n公開🪶\n\n🔗\n\n🎬 ジェイくんの新しいTikTok動画が\n投稿されました💙🪶\n\n高評価 👍 コメント💬再投稿🔄\nXでタグをつけてSNSで広めよう⸜💙⸝‍\n#ジュアンジェイ #JAY羽ばたくじぇい\n#PRODUCE101JAPAN新世界"),
            ("Xアップ",
             "┊✧ 📸 X up!! ✧┊\n\n[内容] ⡱ 公開🪶\n\nジェイくんの[内容]が\n投稿されました💙🪶\n\n高評価 👍 コメント💬&\n#ジュアンジェイ #JAY羽ばたくじぇい\nのタグをつけてSNSで広めよう⸜💙⸝‍"),
            ("YouTubeアップ",
             "┊✧ 📹 YouTube up!! ✧┊\n\n公開🪶\n\n🔗\n\n🎬 ジェイくんの新しいショート動画が\n投稿されました💙🪶\n\n高評価 👍 コメント💬&\n#ジュアンジェイ\nのタグをつけてSNSで広めよう⸜💙⸝‍"),
            ("YouTubeハイライトアップ",
             "┊✧ 📹 YouTube up!! ✧┊\n\n公開🪶\n\n🔗\n\n🎬 ジェイくんのハイライト動画が\n投稿されました💙🪶\n\n高評価 👍 コメント💬&\nタグをつけてSNSで広めよう⸜💙⸝‍\n\n👇🏻ワンタッチポストはこちら\nhttps://x.gd/537RC"),
            ("インスタアップ",
             "┊✧ 📸 Instagram up!! ✧┊\n\n公開🪶\n\n🔗\n\n🎬 ジェイくんの新しい画像が\n投稿されました💙🪶\n\n高評価 👍 コメント💬&\n#ジュアンジェイ\nのタグをつけてSNSで広めよう⸜💙⸝‍"),
        ]),
        ("## ジェイどこ動画", [
            ("ジェイどこ動画",
             "┊✧ 🎥ジェイどこ？動画 公開 ✧┊\n\n一緒にジェイくんを\n探してください🕵️˖ ࣪⊹\n🔗\n\n番組でジェイくんを見つけたら🔍ˊ˗\n\n#ジェイどこ #FINDJAY #ジュアンジェイ\nをつけてスクショを投稿💙🪶\n\n👇🏻ワンタッチポスト👇🏻\n\nhttps://x.gd/i18ye"),
            ("🇬🇧ジェイどこ動画",
             '┊✧ 🎥 "Where\'s Jay?" Video — Now Live ✧┊\n\nHelp us find JAY 🕵️˖ ࣪⊹\n🔗\n\nSpot Jay in the show? 🔍ˊ˗\nPost your screenshot with\n#ジェイどこ #FINDJAY #ジュアンジェイ 💙🪶\n\n👇🏻 One-tap post 👇🏻\nhttps://x.gd/i18ye'),
        ]),
        ("## スミンパーティー", [
            ("スミンパーティーお知らせ",
             "┊✧ 💙STREAMING PARTY🪶 ✧┊\n\nスミンパーティー開催のお知らせ📣\n\n📅開催日時\n　[日時]\n🏷タグ\n　#ジュアンジェイ_スミンパーティー\n　#ジュアンジェイ\n　#PRODUCE101JAPAN新世界\n\n画像とURLをチェック🔎ˊ˗\n📘https://x.gd/O9hjUi\n\n👇🏻ワンタッチポスト\nhttps://x.gd/XqCId"),
            ("🇬🇧スミンパーティーお知らせ",
             "┊✧ 💙STREAMING PARTY🪶 ✧┊\n\n📣 Announcement!\n\n📅 Date & Time\n　[日時]\n\n🏷 Tags\n　#ジュアンジェイ_スミンパーティー\n　#ジュアンジェイ\n　#PRODUCE101JAPAN新世界\n\nCheck the image & URL 🔎ˊ˗\n📘 https://x.gd/O9hjUi\n\n👇🏻 One-tap post\nhttps://x.gd/XqCId"),
            ("スミンパーティースタート",
             "▷▶︎▷ 💙STREAMING PARTY START🪶 ▷▶︎▷\n\n▶️[日時]💥\n\n👇🏻視聴完了後タグをつけて投稿‼️\n\n　#ジュアンジェイ_スミンパーティー\n　#ジュアンジェイ\n　#PRODUCE101JAPAN新世界\n\n画像とURLをチェック🔎ˊ˗\n📘https://x.gd/O9hjUi\n\n👇🏻ワンタッチポスト\nhttps://x.gd/XqCId"),
            ("🇬🇧スミンパーティースタート",
             "▷▶︎▷ 💙STREAMING PARTY START🪶 ▷▶︎▷\n\n▶️[日時]💥\n\n👇🏻 Post with the tag after you finish watching‼️\n　#ジュアンジェイ_スミンパーティー\n　#ジュアンジェイ\n　#PRODUCE101JAPAN新世界\n\nCheck 🔎ˊ˗\n📘https://x.gd/O9hjUi\n\n👇🏻 One-tap post\nhttps://x.gd/XqCId"),
            ("🇹🇼スミンパーティースタート",
             "▷▶︎▷ 💙串流派對開始🪶 ▷▶︎▷\n\n▶️[日時]💥\n\n👇🏻觀看完成後請加上標籤並發文‼️\n\n　#ジュアンジェイ_スミンパーティー\n　#ジュアンジェイ\n　#PRODUCE101JAPAN新世界\n\n請確認圖片與URL🔎ˊ˗\n📘https://x.gd/O9hjUi\n\n👇🏻一鍵發文\nhttps://x.gd/XqCId"),
            ("スミンパーティーリマインド",
             "┊✧ 💙開催まで1️⃣時間🪶 ✧┊\n\nスミンパーティーまで1時間となりました‼️\n\n🏷タグ\n　#ジュアンジェイ_スミンパーティー\n　#ジュアンジェイ\n　#PRODUCE101JAPAN新世界\n\n詳細は引用元をチェック🔎ˊ˗\n\n👇🏻ワンタッチポスト\nhttps://x.gd/XqCId"),
            ("🇬🇧スミンパーティーリマインド",
             "┊✧ 💙1️⃣HOUR TO GO 🪶 ✧┊\n\nOnly 1 hour until the Sumin Party‼️\n\n🏷 Tags\n　#ジュアンジェイ_スミンパーティー\n　#ジュアンジェイ\n　#PRODUCE101JAPAN新世界\n\nCheck the quoted post for details 🔎ˊ˗\n\n👇🏻 One-tap post\nhttps://x.gd/XqCId"),
            ("スミンパーティー終了",
             "⋱ 💙STREAMING PARTY END🪶 ⋰\n\nご参加ありがとうございました✨\n次回も一緒に頑張っていきましょう！\n\n📮視聴の感想はタグをつけて投稿\n#ジュアンジェイ_スミンパーティー\n#ジュアンジェイ\n#PRODUCE101JAPAN新世界\n\n👇🏻ワンタッチポスト\nhttps://x.gd/XqCId"),
            ("🇬🇧スミンパーティー終了",
             "⋱ 💙STREAMING PARTY END🪶 ⋰\n\nThank you for joining us✨\nLet's keep cheering together next time too!\n\n📮Share your thoughts with the tags\n　#ジュアンジェイ_スミンパーティー\n　#ジュアンジェイ\n　#PRODUCE101JAPAN新世界\n\n👇🏻One-touch post\nhttps://x.gd/XqCId"),
            ("🇹🇼スミン終了案内",
             "⋱ 💙串流派對結束🪶 ⋰\n\n感謝您的參與✨\n下次也一起加油吧！\n\n📮請附上標籤分享您的觀看感想\n　#ジュアンジェイ_スミンパーティー\n　#ジュアンジェイ\n　#PRODUCE101JAPAN新世界\n\n👇🏻一鍵發文\nhttps://x.gd/XqCId"),
        ]),
        ("## タグイベ", [
            ("タグイベお知らせ",
             "┊✧ 💙HASHTAG EVENT!!🪶 ✧┊\n\n#ジュアンジェイ タグイベント\n開催のお知らせ📣\n\n🔥目指せトレンド入り🔥\n\n📅開催日時\n　[日時]\n🏷指定タグ\n　#JustVoteJay\n　#ジュアンジェイ\n\n詳細は画像とURLをチェック🔎ˊ˗\n🔗https://x.gd/kO2i6\n\n👇🏻ワンタッチポスト\nhttps://x.gd/n2pLz"),
            ("🇬🇧タグイベお知らせ",
             "┊✧ 💙HASHTAG EVENT!!🪶 ✧┊\n\nLet's get him trending! 🔥\n\n📅 [日時] JST\n\n🏷 #JustVoteJay\n      #ジュアンジェイ\n\nDetails in the image & link 🔎˗ˊ\n🔗 https://x.gd/kO2i6\n\n👇🏻 One-tap post\nhttps://x.gd/n2pLz"),
            ("タグイベスタート",
             "▷▶︎▷ 💙 HASHTAG EVENT START🪶 ▷▶︎▷\n\n▶️[日時]💥\n\n🏷️タグをつけて投稿！\n　#JustVoteJay\n　#ジュアンジェイ\n\n詳細は画像とURLをチェック🔎ˊ˗\n🔗https://x.gd/kO2i6\n\n👇🏻ワンタッチポスト\nhttps://x.gd/n2pLz"),
            ("🇬🇧タグイベスタート",
             "▷▶︎▷ 💙 HASHTAG EVENT START 🪶 ▷▶︎▷\n\n▶️ [日時] JST 💥\n\n🏷️ Post with the tags!\n　#JustVoteJay\n　#ジュアンジェイ\n\nCheck the image & URL for details 🔎ˊ˗\n🔗 https://x.gd/kO2i6\n\n👇🏻 One-tap post\nhttps://x.gd/n2pLz"),
            ("タグイベリマインド",
             "┊✧ 💙開催まで1️⃣時間🪶 ✧┊\n\nタグイベまで1時間となりました‼️\n\n🏷タグ\n　#JustVoteJay\n　#ジュアンジェイ\n\n詳細は引用元をチェック🔎ˊ˗\n\n👇🏻ワンタッチポスト\nhttps://x.gd/n2pLz"),
            ("🇬🇧タグイベリマインド",
             "┊✧ 💙 1 HOUR TO GO 🪶 ✧┊\n\nThe tag event starts in 1 hour‼️\n\n🏷 Tags\n　#JustVoteJay\n　#ジュアンジェイ\n\nCheck the quoted post for details 🔎ˊ˗\n\n👇🏻 One-tap post\nhttps://x.gd/n2pLz"),
            ("タグイベ終了",
             "⋱ 💙 HASHTAG EVENT END🪶 ⋰\n\nご参加ありがとうございました✨\n次回も一緒に頑張っていきましょう！\n\nジェイくんの情報はこちらをチェック🔍ˊ˗\n\n🔗https://x.gd/4A61D"),
            ("🇬🇧タグイベ終了",
             "⋱ 💙 HASHTAG EVENT END 🪶 ⋰\n\nThank you for joining us! ✨\nLet's keep cheering together next time!\n\nCheck here for all things Jay 🔍ˊ˗\n\n🔗 https://x.gd/4A61D"),
        ]),
        ("## 投票", [
            ("投票サイト開設",
             "⋱ 💙投票サイト開設🪶 ⋰\n\n🚨dアカウントに事前ログインを！🚨\n\n国民投票にはdアカウントが必要です‼️\n\n開始直後はアクセスが集中しますので\n番組開始前までにログイン完了しましょう✅\n\n詳しくはJAYBIRDSHPもチェック🔍ˊ˗\nhttps://x.gd/63FPj\n\n#JAY羽ばたくじぇい #ジュアンジェイ"),
            ("投票リマインド（短縮版）",
             "🗳️⚡️⚡️投票のお願い⚡️⚡️🗳️\n\n本日分の投票はお済みですか？\n\nどうか毎日2️⃣票🔥🔥お忘れなく🔥🔥\n投票と呼びかけをよろしくお願いします🙇\n\n【JAYBIRDS全員】の投票・布教で\nジェイくんを応援しましょう💙🪶\n\n🗳️ 公式で投票👇\n🔗 https://vote.produce101.jp\n📱 Leminoアプリから投票を！"),
            ("投票リマインド（詳細版）",
             "🗳️⚡️⚡️投票のお願い⚡️⚡️🗳️\n\n本日分の投票はお済みですか？\n\nどうか毎日2️⃣票🔥🔥お忘れなく🔥🔥\n投票と呼びかけをよろしくお願いします🙇\n\n【JAYBIRDS全員】の投票・布教で\nジェイくんを応援しましょう💙🪶\n\n🗳️ 公式で投票👇\n🔗 https://vote.produce101.jp\n📱 Leminoアプリから投票を！\n\n🗳️ 投票の流れはこちら👇\n🔗 https://x.gd/63FPj\n📱 投票方法の動画👇\n🔗 https://vt.tiktok.com/ZSuw3yp3V/"),
            ("🇹🇼投票リマインド",
             "🗳️⚡️⚡️請投票⚡️⚡️🗳️\n\n你今天已經投票了嗎？\n\n別忘了你每天的1️⃣次投票🔥🔥\n\n請投票並幫忙擴散🙇\n\n讓我們用每一位JAYBIRD的投票與支持\n一起為莊宗傑加油💙🪶\n\n投票👇\n📱 請從Mnet+應用程式投票！\n詳細👇\n🔗 https://x.gd/63FPj"),
        ]),
        ("## 放送用", [
            ("放送開始",
             "⋱ 💙 間もなく放送開始!! 🪶 ⋰\n\nオンエアの際に使用するハッシュタグの\nワンタッチツイートです❣️\nJAYBIRDSの皆さま、ぜひご活用ください✨\n\n👇🏻\n\n🔗 https://x.gd/537RC"),
        ]),
    ]),
    ("# TikTok投稿", [
        (None, [
            ("TikTokタグ",
             "TikTokタグ\n\n#ジェイどこ\n#FINDJAY\n#ジュアンジェイ\n#PRODUCE101JAPAN新世界\n#101SHINSEKAI"),
            ("ジェイどこ投稿（TikTok）",
             "┊✧ 🎥ジェイどこ？ ✧┊\nこの動画の中にジェイくんが隠れています🕵️ˊ˗\nあなたは見つけられますか？👀\n見つけた方はぜひコメントで教えてください💙🪶\n#ジェイどこ\n#FINDJAY\n#ジュアンジェイ\n#PRODUCE101JAPAN新世界\n#101SHINSEKAI"),
            ("スクショ共有編（TikTok）",
             "┊✧ 🎥ジェイどこ？ ✧┊\n[話数]のジェイくんの出演場面を発見しました🕵️ˊ˗\nあなたは見つけられましたか？👀\n他にも見つけた方はぜひ\nコメントで教えてください💙🪶\n#ジェイどこ\n#FINDJAY\n#ジュアンジェイ\n#PRODUCE101JAPAN新世界\n#101SHINSEKAI"),
        ]),
    ]),
    ("# OC（オープンチャット）", [
        ("## 投票リマインド", [
            ("OC投票リマインド（詳細版）",
             "🗳️⚡️⚡️投票のお願い⚡️⚡️🗳️\n\n本日分の投票はお済みですか？\n\nどうか毎日2️⃣票🔥🔥お忘れなく🔥🔥\n投票と呼びかけをよろしくお願いします🙇\n\n【JAYBIRDS全員】の投票・布教で\nジェイくんを応援しましょう💙🪶\n\n🗳️ 公式で投票👇\n🔗 https://vote.produce101.jp\n📺 レミノで投票👇\n📱 Leminoアプリから投票を！\n\n🗳️ 投票の流れはこちら👇\n🔗 https://x.gd/63FPj\n📱 投票方法の動画👇\n🔗 https://vt.tiktok.com/ZSuw3yp3V/"),
        ]),
    ]),
]


def get_credentials():
    key_json = os.environ.get("GA4_SERVICE_ACCOUNT_KEY")
    if not key_json:
        print("ERROR: 環境変数 GA4_SERVICE_ACCOUNT_KEY が設定されていません。", file=sys.stderr)
        sys.exit(1)
    try:
        key_data = json.loads(key_json)
    except json.JSONDecodeError as e:
        print(f"ERROR: GA4_SERVICE_ACCOUNT_KEY のJSONが不正です: {e}", file=sys.stderr)
        sys.exit(1)
    return service_account.Credentials.from_service_account_info(key_data, scopes=SCOPES)


def build_document_text():
    """全セクション・テンプレートのテキストブロックを構築して返す"""
    lines = []
    total_posts = 0

    for section_title, subsections in DOCUMENT_DATA:
        lines.append(section_title)
        lines.append("")

        for subsection_title, posts in subsections:
            if subsection_title:
                lines.append(subsection_title)
                lines.append("")

            for title, body in posts:
                lines.append(SEP)
                lines.append(f"📌 {title}")
                lines.append(SEP)
                lines.append(body)
                lines.append("")
                lines.append("---")
                lines.append("")
                total_posts += 1

        lines.append("")

    return "\n".join(lines), total_posts


def main():
    creds = get_credentials()
    service = build("docs", "v1", credentials=creds)

    print("テキストを構築中...")
    text, total_posts = build_document_text()

    print(f"Googleドキュメントに書き込み中... ({total_posts}件)")
    service.documents().batchUpdate(
        documentId=DOCUMENT_ID,
        body={
            "requests": [
                {
                    "insertText": {
                        "location": {"index": 1},
                        "text": text,
                    }
                }
            ]
        },
    ).execute()

    print(f"✅ {total_posts}件の書き込み完了！")
    print(f"https://docs.google.com/document/d/{DOCUMENT_ID}/edit")


if __name__ == "__main__":
    main()
