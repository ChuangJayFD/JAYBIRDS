#!/usr/bin/env python3
"""
import_keep.py — JAYBIRDSドキュメントを全削除してから見出し構造＋全テンプレートを書き込む

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
# ドキュメントデータ
# 構造: [{"h1": str, "sections": [{"h2": str|None, "posts": [{...}]}, ...]}, ...]
# 各 post: {"title": str, "ja": str, "en": str, "zh": str, "ko": str}
# ──────────────────────────────────────────────────────────────────────────────
DOCUMENT_DATA = [

    # ════════════════════════════════════════════════════════════════════
    # X投稿
    # ════════════════════════════════════════════════════════════════════
    {
        "h1": "X投稿",
        "sections": [

            # ── ジェイどこ動画 ──────────────────────────────────────────
            {
                "h2": "ジェイどこ動画",
                "posts": [
                    {
                        "title": "ジェイどこ動画",
                        "ja": (
                            "┊✧ 🎥ジェイどこ？動画 公開 ✧┊\n"
                            "\n"
                            "一緒にジェイくんを\n"
                            "探してください🕵️˖ ࣪⊹\n"
                            "🔗\n"
                            "\n"
                            "番組でジェイくんを見つけたら🔍ˊ˗\n"
                            "\n"
                            "#ジェイどこ #FINDJAY #ジュアンジェイ\n"
                            "をつけてスクショを投稿💙🪶\n"
                            "\n"
                            "👇🏻ワンタッチポスト👇🏻\n"
                            "https://x.gd/i18ye"
                        ),
                        "en": (
                            '┊✧ 🎥 "Where\'s Jay?" Video — Now Live ✧┊\n'
                            "\n"
                            "Help us find Chuang Jay 🕵️˖ ࣪⊹\n"
                            "🔗\n"
                            "\n"
                            "Spot Jay in the show? 🔍ˊ˗\n"
                            "Post your screenshot with the tags 💙🪶\n"
                            "\n"
                            "#ジェイどこ #FINDJAY #ジュアンジェイ\n"
                            "\n"
                            "👇🏻 One-tap post 👇🏻\n"
                            "https://x.gd/i18ye"
                        ),
                        "zh": (
                            "┊✧ 🎥「JAY在哪裡？」影片 公開 ✧┊\n"
                            "\n"
                            "一起來找莊宗傑吧🕵️˖ ࣪⊹\n"
                            "🔗\n"
                            "\n"
                            "在節目中發現JAY嗎？🔍ˊ˗\n"
                            "加上標籤發布截圖💙🪶\n"
                            "\n"
                            "#ジェイどこ #FINDJAY #ジュアンジェイ\n"
                            "\n"
                            "👇🏻一鍵發文👇🏻\n"
                            "https://x.gd/i18ye"
                        ),
                        "ko": (
                            "┊✧ 🎥「제이 어디있어？」영상 공개 ✧┊\n"
                            "\n"
                            "함께 장앙제이를 찾아주세요🕵️˖ ࣪⊹\n"
                            "🔗\n"
                            "\n"
                            "방송에서 제이를 발견하면🔍ˊ˗\n"
                            "태그 달고 스크린샷 포스팅💙🪶\n"
                            "\n"
                            "#ジェイどこ #FINDJAY #ジュアンジェイ\n"
                            "\n"
                            "👇🏻원터치 포스트👇🏻\n"
                            "https://x.gd/i18ye"
                        ),
                    },
                ],
            },

            # ── 投票 ────────────────────────────────────────────────────
            {
                "h2": "投票",
                "posts": [
                    {
                        "title": "投票サイト開設",
                        "ja": (
                            "⋱ 💙投票サイト開設🪶 ⋰\n"
                            "\n"
                            "🚨dアカウントに事前ログインを！🚨\n"
                            "\n"
                            "国民投票にはdアカウントが必要です‼️\n"
                            "\n"
                            "開始直後はアクセスが集中しますので\n"
                            "番組開始前までにログイン完了しましょう✅\n"
                            "\n"
                            "詳しくはJAYBIRDS HPをチェック🔍ˊ˗\n"
                            "https://x.gd/63FPj\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "en": (
                            "⋱ 💙 Voting Site Open 🪶 ⋰\n"
                            "\n"
                            "🚨 Log in to your d-account in advance! 🚨\n"
                            "\n"
                            "A d-account is required to vote in the national poll‼️\n"
                            "\n"
                            "Traffic will spike at the start, so\n"
                            "complete your login before the show begins✅\n"
                            "\n"
                            "Check the JAYBIRDS site for details 🔍ˊ˗\n"
                            "https://x.gd/63FPj\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ"
                        ),
                        "zh": (
                            "⋱ 💙 投票網站開放 🪶 ⋰\n"
                            "\n"
                            "🚨 請提前登入d帳號！🚨\n"
                            "\n"
                            "國民票投票需要d帳號‼️\n"
                            "\n"
                            "開始時段流量集中，\n"
                            "請在節目開始前完成登入✅\n"
                            "\n"
                            "詳情請查看JAYBIRDS網站🔍ˊ˗\n"
                            "https://x.gd/63FPj\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ"
                        ),
                        "ko": (
                            "⋱ 💙 투표 사이트 오픈 🪶 ⋰\n"
                            "\n"
                            "🚨 d계정에 미리 로그인하세요! 🚨\n"
                            "\n"
                            "국민투표에는 d계정이 필요합니다‼️\n"
                            "\n"
                            "시작 직후 접속이 집중되므로\n"
                            "방송 시작 전까지 로그인을 완료하세요✅\n"
                            "\n"
                            "자세한 내용은 JAYBIRDS 사이트에서🔍ˊ˗\n"
                            "https://x.gd/63FPj\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ"
                        ),
                    },
                    {
                        "title": "投票リマインド（短縮版）",
                        "ja": (
                            "🗳️⚡️⚡️投票のお願い⚡️⚡️🗳️\n"
                            "\n"
                            "本日分の投票はお済みですか？\n"
                            "\n"
                            "どうか毎日2️⃣票🔥🔥お忘れなく🔥🔥\n"
                            "投票と呼びかけをよろしくお願いします🙇\n"
                            "\n"
                            "【JAYBIRDS全員】の投票・布教で\n"
                            "ジェイくんを応援しましょう💙🪶\n"
                            "\n"
                            "🗳️ 公式で投票👇\n"
                            "🔗 https://vote.produce101.jp\n"
                            "📱 Leminoアプリから投票を！"
                        ),
                        "en": (
                            "🗳️⚡️⚡️ Please Vote ⚡️⚡️🗳️\n"
                            "\n"
                            "Have you voted today?\n"
                            "\n"
                            "Don't forget your daily vote🔥\n"
                            "Please vote and spread the word🙇\n"
                            "\n"
                            "Let's support Chuang Jay with\n"
                            "every JAYBIRD's vote & fandom 💙🪶\n"
                            "\n"
                            "🗳️ Official vote👇\n"
                            "🔗 https://vote.produce101.jp\n"
                            "📱 Vote via the Mnet+ app!"
                        ),
                        "zh": (
                            "🗳️⚡️⚡️請投票⚡️⚡️🗳️\n"
                            "\n"
                            "你今天已經投票了嗎？\n"
                            "\n"
                            "別忘了每天1️⃣次投票🔥\n"
                            "請投票並幫忙擴散🙇\n"
                            "\n"
                            "讓我們用每一位JAYBIRD的投票與支持\n"
                            "一起為莊宗傑加油💙🪶\n"
                            "\n"
                            "🗳️ 官方投票👇\n"
                            "🔗 https://vote.produce101.jp\n"
                            "📱 請從Mnet+應用程式投票！"
                        ),
                        "ko": (
                            "🗳️⚡️⚡️ 투표 부탁드립니다 ⚡️⚡️🗳️\n"
                            "\n"
                            "오늘 투표는 하셨나요?\n"
                            "\n"
                            "매일 1️⃣표🔥를 잊지 마세요\n"
                            "투표와 홍보 부탁드립니다🙇\n"
                            "\n"
                            "【JAYBIRDS 모두】의 투표와 홍보로\n"
                            "장앙제이를 응원합시다 💙🪶\n"
                            "\n"
                            "🗳️ 공식 투표👇\n"
                            "🔗 https://vote.produce101.jp\n"
                            "📱 Mnet+ 앱에서 투표를!"
                        ),
                    },
                    {
                        "title": "投票リマインド（詳細版）",
                        "ja": (
                            "🗳️⚡️⚡️投票のお願い⚡️⚡️🗳️\n"
                            "\n"
                            "本日分の投票はお済みですか？\n"
                            "\n"
                            "どうか毎日2️⃣票🔥🔥お忘れなく🔥🔥\n"
                            "投票と呼びかけをよろしくお願いします🙇\n"
                            "\n"
                            "【JAYBIRDS全員】の投票・布教で\n"
                            "ジェイくんを応援しましょう💙🪶\n"
                            "\n"
                            "🗳️ 公式で投票👇\n"
                            "🔗 https://vote.produce101.jp\n"
                            "📱 Leminoアプリから投票を！\n"
                            "\n"
                            "🗳️ 投票の流れはこちら👇\n"
                            "🔗 https://x.gd/63FPj\n"
                            "📱 投票方法の動画👇\n"
                            "🔗 https://vt.tiktok.com/ZSuw3yp3V/"
                        ),
                        "en": (
                            "🗳️⚡️⚡️ Please Vote ⚡️⚡️🗳️\n"
                            "\n"
                            "Have you cast today's votes?\n"
                            "\n"
                            "Don't forget your daily vote🔥\n"
                            "Please vote and spread the word🙇\n"
                            "\n"
                            "Let's support Chuang Jay with\n"
                            "every JAYBIRD's vote & fandom 💙🪶\n"
                            "\n"
                            "🗳️ Official vote👇\n"
                            "🔗 https://vote.produce101.jp\n"
                            "📱 Vote via the Mnet+ app!\n"
                            "\n"
                            "🗳️ Step-by-step voting guide👇\n"
                            "🔗 https://x.gd/63FPj\n"
                            "📱 How-to video👇\n"
                            "🔗 https://vt.tiktok.com/ZSuw3yp3V/"
                        ),
                        "zh": (
                            "🗳️⚡️⚡️請投票⚡️⚡️🗳️\n"
                            "\n"
                            "今天的投票完成了嗎？\n"
                            "\n"
                            "別忘了每天1️⃣次投票🔥\n"
                            "請多多投票並幫忙宣傳🙇\n"
                            "\n"
                            "讓每一位JAYBIRD的投票與支持\n"
                            "一起為莊宗傑加油💙🪶\n"
                            "\n"
                            "🗳️ 官方投票👇\n"
                            "🔗 https://vote.produce101.jp\n"
                            "📱 請從Mnet+應用程式投票！\n"
                            "\n"
                            "🗳️ 詳細投票方法👇\n"
                            "🔗 https://x.gd/63FPj\n"
                            "📱 投票方法影片👇\n"
                            "🔗 https://vt.tiktok.com/ZSuw3yp3V/"
                        ),
                        "ko": (
                            "🗳️⚡️⚡️ 투표 부탁드립니다 ⚡️⚡️🗳️\n"
                            "\n"
                            "오늘 투표 완료하셨나요?\n"
                            "\n"
                            "매일 1️⃣표🔥를 잊지 마세요\n"
                            "투표와 홍보 부탁드립니다🙇\n"
                            "\n"
                            "【JAYBIRDS 모두】의 투표와 홍보로\n"
                            "장앙제이를 응원합시다 💙🪶\n"
                            "\n"
                            "🗳️ 공식 투표👇\n"
                            "🔗 https://vote.produce101.jp\n"
                            "📱 Mnet+ 앱에서 투표를!\n"
                            "\n"
                            "🗳️ 투표 방법 자세히 보기👇\n"
                            "🔗 https://x.gd/63FPj\n"
                            "📱 투표 방법 동영상👇\n"
                            "🔗 https://vt.tiktok.com/ZSuw3yp3V/"
                        ),
                    },
                ],
            },

            # ── 放送用 ──────────────────────────────────────────────────
            {
                "h2": "放送用",
                "posts": [
                    {
                        "title": "放送前リマインド（ワンタッチ）",
                        "ja": (
                            "⋱ 💙 間もなく放送開始!! 🪶 ⋰\n"
                            "\n"
                            "オンエアの際に使用するハッシュタグの\n"
                            "ワンタッチツイートです❣️\n"
                            "JAYBIRDSの皆さま、ぜひご活用ください✨\n"
                            "\n"
                            "👇🏻\n"
                            "🔗 https://x.gd/537RC"
                        ),
                        "en": (
                            "⋱ 💙 Broadcast Starting Soon!! 🪶 ⋰\n"
                            "\n"
                            "One-tap tweet with the hashtags\n"
                            "to use during the broadcast❣️\n"
                            "JAYBIRDS, please make full use of it✨\n"
                            "\n"
                            "👇🏻\n"
                            "🔗 https://x.gd/537RC"
                        ),
                        "zh": (
                            "⋱ 💙 即將開始放送！！ 🪶 ⋰\n"
                            "\n"
                            "直播期間使用的標籤\n"
                            "一鍵推文連結❣️\n"
                            "JAYBIRDS，請多加利用✨\n"
                            "\n"
                            "👇🏻\n"
                            "🔗 https://x.gd/537RC"
                        ),
                        "ko": (
                            "⋱ 💙 곧 방송 시작!! 🪶 ⋰\n"
                            "\n"
                            "방송 중에 사용할 해시태그\n"
                            "원터치 트윗입니다❣️\n"
                            "JAYBIRDS 여러분, 적극 활용해 주세요✨\n"
                            "\n"
                            "👇🏻\n"
                            "🔗 https://x.gd/537RC"
                        ),
                    },
                ],
            },

            # ── 公式投稿引用 ────────────────────────────────────────────
            {
                "h2": "公式投稿引用",
                "posts": [
                    {
                        "title": "TikTok更新",
                        "ja": (
                            "┊✧ 📹 TikTok up!! ✧┊\n"
                            "\n"
                            "公開🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "🎬 ジェイくんの新しいTikTok動画が\n"
                            "投稿されました💙🪶\n"
                            "\n"
                            "高評価 👍 コメント💬 再投稿🔄\n"
                            "Xでタグをつけてシェアしよう⸜💙⸝‍\n"
                            "#ジュアンジェイ #JAY羽ばたくじぇい\n"
                            "#PRODUCE101JAPAN新世界"
                        ),
                        "en": (
                            "┊✧ 📹 TikTok up!! ✧┊\n"
                            "\n"
                            "Now live 🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "🎬 A new TikTok from Chuang Jay\n"
                            "has just dropped💙🪶\n"
                            "\n"
                            "Like 👍 Comment💬 Repost🔄\n"
                            "Tag and share on X⸜💙⸝‍\n"
                            "#ジュアンジェイ #JAY羽ばたくじぇい\n"
                            "#PRODUCE101JAPAN新世界"
                        ),
                        "zh": (
                            "┊✧ 📹 TikTok up!! ✧┊\n"
                            "\n"
                            "公開🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "🎬 莊宗傑的新TikTok影片\n"
                            "已上傳💙🪶\n"
                            "\n"
                            "按讚 👍 留言💬 轉發🔄\n"
                            "加上標籤在X上分享⸜💙⸝‍\n"
                            "#ジュアンジェイ #JAY羽ばたくじぇい\n"
                            "#PRODUCE101JAPAN新世界"
                        ),
                        "ko": (
                            "┊✧ 📹 TikTok up!! ✧┊\n"
                            "\n"
                            "공개 🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "🎬 장앙제이의 새로운 TikTok 영상이\n"
                            "올라왔어요💙🪶\n"
                            "\n"
                            "좋아요 👍 댓글💬 리포스트🔄\n"
                            "X에서 태그 달고 공유해요⸜💙⸝‍\n"
                            "#ジュアンジェイ #JAY羽ばたくじぇい\n"
                            "#PRODUCE101JAPAN新世界"
                        ),
                    },
                    {
                        "title": "Xアップ",
                        "ja": (
                            "┊✧ 📸 X up!! ✧┊\n"
                            "\n"
                            "[内容] 公開🪶\n"
                            "\n"
                            "ジェイくんの[内容]が\n"
                            "投稿されました💙🪶\n"
                            "\n"
                            "高評価 👍 コメント💬 &\n"
                            "#ジュアンジェイ #JAY羽ばたくじぇい\n"
                            "のタグをつけてシェアしよう⸜💙⸝‍"
                        ),
                        "en": (
                            "┊✧ 📸 X up!! ✧┊\n"
                            "\n"
                            "[Content] — Now live 🪶\n"
                            "\n"
                            "Chuang Jay's [content]\n"
                            "has been posted💙🪶\n"
                            "\n"
                            "Like 👍 Comment💬 &\n"
                            "Share with the tags⸜💙⸝‍\n"
                            "#ジュアンジェイ #JAY羽ばたくじぇい"
                        ),
                        "zh": (
                            "┊✧ 📸 X up!! ✧┊\n"
                            "\n"
                            "[內容] 公開🪶\n"
                            "\n"
                            "莊宗傑的[內容]\n"
                            "已上傳💙🪶\n"
                            "\n"
                            "按讚 👍 留言💬 &\n"
                            "加標籤分享⸜💙⸝‍\n"
                            "#ジュアンジェイ #JAY羽ばたくじぇい"
                        ),
                        "ko": (
                            "┊✧ 📸 X up!! ✧┊\n"
                            "\n"
                            "[내용] 공개 🪶\n"
                            "\n"
                            "장앙제이의 [내용]이\n"
                            "올라왔어요💙🪶\n"
                            "\n"
                            "좋아요 👍 댓글💬 &\n"
                            "태그 달고 공유해요⸜💙⸝‍\n"
                            "#ジュアンジェイ #JAY羽ばたくじぇい"
                        ),
                    },
                    {
                        "title": "YouTubeアップ",
                        "ja": (
                            "┊✧ 📹 YouTube up!! ✧┊\n"
                            "\n"
                            "公開🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "🎬 ジェイくんの新しいショート動画が\n"
                            "投稿されました💙🪶\n"
                            "\n"
                            "高評価 👍 コメント💬 &\n"
                            "#ジュアンジェイ\n"
                            "のタグをつけてシェアしよう⸜💙⸝‍"
                        ),
                        "en": (
                            "┊✧ 📹 YouTube up!! ✧┊\n"
                            "\n"
                            "Now live 🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "🎬 A new YouTube Short featuring Chuang Jay\n"
                            "has just dropped💙🪶\n"
                            "\n"
                            "Like 👍 Comment💬 &\n"
                            "Tag and share⸜💙⸝‍\n"
                            "#ジュアンジェイ"
                        ),
                        "zh": (
                            "┊✧ 📹 YouTube up!! ✧┊\n"
                            "\n"
                            "公開🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "🎬 莊宗傑的新YouTube短影片\n"
                            "已上傳💙🪶\n"
                            "\n"
                            "按讚 👍 留言💬 &\n"
                            "加標籤分享⸜💙⸝‍\n"
                            "#ジュアンジェイ"
                        ),
                        "ko": (
                            "┊✧ 📹 YouTube up!! ✧┊\n"
                            "\n"
                            "공개 🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "🎬 장앙제이의 새로운 YouTube 쇼츠가\n"
                            "올라왔어요💙🪶\n"
                            "\n"
                            "좋아요 👍 댓글💬 &\n"
                            "태그 달고 공유해요⸜💙⸝‍\n"
                            "#ジュアンジェイ"
                        ),
                    },
                    {
                        "title": "YouTubeハイライトアップ",
                        "ja": (
                            "┊✧ 📹 YouTube up!! ✧┊\n"
                            "\n"
                            "公開🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "🎬 ジェイくんのハイライト動画が\n"
                            "投稿されました💙🪶\n"
                            "\n"
                            "高評価 👍 コメント💬 &\n"
                            "タグをつけてシェアしよう⸜💙⸝‍\n"
                            "\n"
                            "👇🏻ワンタッチポストはこちら\n"
                            "https://x.gd/537RC"
                        ),
                        "en": (
                            "┊✧ 📹 YouTube up!! ✧┊\n"
                            "\n"
                            "Now live 🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "🎬 A highlight video of Chuang Jay\n"
                            "has just been posted💙🪶\n"
                            "\n"
                            "Like 👍 Comment💬 &\n"
                            "Tag and share⸜💙⸝‍\n"
                            "\n"
                            "👇🏻 One-tap post\n"
                            "https://x.gd/537RC"
                        ),
                        "zh": (
                            "┊✧ 📹 YouTube up!! ✧┊\n"
                            "\n"
                            "公開🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "🎬 莊宗傑的精彩片段影片\n"
                            "已上傳💙🪶\n"
                            "\n"
                            "按讚 👍 留言💬 &\n"
                            "加標籤分享⸜💙⸝‍\n"
                            "\n"
                            "👇🏻一鍵發文\n"
                            "https://x.gd/537RC"
                        ),
                        "ko": (
                            "┊✧ 📹 YouTube up!! ✧┊\n"
                            "\n"
                            "공개 🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "🎬 장앙제이의 하이라이트 영상이\n"
                            "올라왔어요💙🪶\n"
                            "\n"
                            "좋아요 👍 댓글💬 &\n"
                            "태그 달고 공유해요⸜💙⸝‍\n"
                            "\n"
                            "👇🏻원터치 포스트\n"
                            "https://x.gd/537RC"
                        ),
                    },
                    {
                        "title": "インスタアップ",
                        "ja": (
                            "┊✧ 📸 Instagram up!! ✧┊\n"
                            "\n"
                            "公開🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "📸 ジェイくんの新しい投稿が\n"
                            "アップされました💙🪶\n"
                            "\n"
                            "高評価 👍 コメント💬 &\n"
                            "#ジュアンジェイ\n"
                            "のタグをつけてシェアしよう⸜💙⸝‍"
                        ),
                        "en": (
                            "┊✧ 📸 Instagram up!! ✧┊\n"
                            "\n"
                            "Now live 🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "📸 A new Instagram post from Chuang Jay\n"
                            "is now up💙🪶\n"
                            "\n"
                            "Like 👍 Comment💬 &\n"
                            "Tag and share⸜💙⸝‍\n"
                            "#ジュアンジェイ"
                        ),
                        "zh": (
                            "┊✧ 📸 Instagram up!! ✧┊\n"
                            "\n"
                            "公開🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "📸 莊宗傑的新Instagram貼文\n"
                            "已上傳💙🪶\n"
                            "\n"
                            "按讚 👍 留言💬 &\n"
                            "加標籤分享⸜💙⸝‍\n"
                            "#ジュアンジェイ"
                        ),
                        "ko": (
                            "┊✧ 📸 Instagram up!! ✧┊\n"
                            "\n"
                            "공개 🪶\n"
                            "\n"
                            "🔗\n"
                            "\n"
                            "📸 장앙제이의 새로운 Instagram 포스트가\n"
                            "올라왔어요💙🪶\n"
                            "\n"
                            "좋아요 👍 댓글💬 &\n"
                            "태그 달고 공유해요⸜💙⸝‍\n"
                            "#ジュアンジェイ"
                        ),
                    },
                ],
            },

            # ── スミンパーティー ────────────────────────────────────────
            {
                "h2": "スミンパーティー",
                "posts": [
                    {
                        "title": "スミンパーティーお知らせ",
                        "ja": (
                            "┊✧ 💙STREAMING PARTY🪶 ✧┊\n"
                            "\n"
                            "スミンパーティー開催のお知らせ📣\n"
                            "\n"
                            "📅 開催日時\n"
                            "　[日時]\n"
                            "🏷 タグ\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "詳細は画像とURLをチェック🔎ˊ˗\n"
                            "📘 https://x.gd/O9hjUi\n"
                            "\n"
                            "👇🏻ワンタッチポスト\n"
                            "https://x.gd/XqCId"
                        ),
                        "en": (
                            "┊✧ 💙STREAMING PARTY🪶 ✧┊\n"
                            "\n"
                            "📣 Sumin Party Announcement!\n"
                            "\n"
                            "📅 Date & Time\n"
                            "　[日時]\n"
                            "🏷 Tags\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "Check the image & URL for details 🔎ˊ˗\n"
                            "📘 https://x.gd/O9hjUi\n"
                            "\n"
                            "👇🏻 One-tap post\n"
                            "https://x.gd/XqCId"
                        ),
                        "zh": (
                            "┊✧ 💙串流派對舉辦通知🪶 ✧┊\n"
                            "\n"
                            "📣 Sumin派對舉辦通知！\n"
                            "\n"
                            "📅 日期與時間\n"
                            "　[日時]\n"
                            "🏷 標籤\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "請確認圖片與連結🔎ˊ˗\n"
                            "📘 https://x.gd/O9hjUi\n"
                            "\n"
                            "👇🏻一鍵發文\n"
                            "https://x.gd/XqCId"
                        ),
                        "ko": (
                            "┊✧ 💙스트리밍 파티 개최 안내🪶 ✧┊\n"
                            "\n"
                            "📣 Sumin 파티 개최 안내！\n"
                            "\n"
                            "📅 날짜 & 시간\n"
                            "　[日時]\n"
                            "🏷 태그\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "이미지 & URL 확인🔎ˊ˗\n"
                            "📘 https://x.gd/O9hjUi\n"
                            "\n"
                            "👇🏻원터치 포스트\n"
                            "https://x.gd/XqCId"
                        ),
                    },
                    {
                        "title": "スミンパーティースタート",
                        "ja": (
                            "▷▶︎▷ 💙STREAMING PARTY START🪶 ▷▶︎▷\n"
                            "\n"
                            "▶️[日時]💥\n"
                            "\n"
                            "👇🏻視聴完了後タグをつけて投稿‼️\n"
                            "\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "詳細は画像とURLをチェック🔎ˊ˗\n"
                            "📘 https://x.gd/O9hjUi\n"
                            "\n"
                            "👇🏻ワンタッチポスト\n"
                            "https://x.gd/XqCId"
                        ),
                        "en": (
                            "▷▶︎▷ 💙STREAMING PARTY START🪶 ▷▶︎▷\n"
                            "\n"
                            "▶️[日時]💥\n"
                            "\n"
                            "👇🏻 Post with the tag after watching‼️\n"
                            "\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "Check the image & URL 🔎ˊ˗\n"
                            "📘 https://x.gd/O9hjUi\n"
                            "\n"
                            "👇🏻 One-tap post\n"
                            "https://x.gd/XqCId"
                        ),
                        "zh": (
                            "▷▶︎▷ 💙串流派對開始🪶 ▷▶︎▷\n"
                            "\n"
                            "▶️[日時]💥\n"
                            "\n"
                            "👇🏻觀看完成後請加上標籤並發文‼️\n"
                            "\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "請確認圖片與URL🔎ˊ˗\n"
                            "📘 https://x.gd/O9hjUi\n"
                            "\n"
                            "👇🏻一鍵發文\n"
                            "https://x.gd/XqCId"
                        ),
                        "ko": (
                            "▷▶︎▷ 💙스트리밍 파티 시작🪶 ▷▶︎▷\n"
                            "\n"
                            "▶️[日時]💥\n"
                            "\n"
                            "👇🏻시청 후 태그 달아 포스팅‼️\n"
                            "\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "이미지 & URL 확인🔎ˊ˗\n"
                            "📘 https://x.gd/O9hjUi\n"
                            "\n"
                            "👇🏻원터치 포스트\n"
                            "https://x.gd/XqCId"
                        ),
                    },
                    {
                        "title": "スミンパーティーリマインド（1時間前）",
                        "ja": (
                            "┊✧ 💙開催まで1️⃣時間🪶 ✧┊\n"
                            "\n"
                            "スミンパーティーまで1時間となりました‼️\n"
                            "\n"
                            "🏷 タグ\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "詳細は引用元をチェック🔎ˊ˗\n"
                            "\n"
                            "👇🏻ワンタッチポスト\n"
                            "https://x.gd/XqCId"
                        ),
                        "en": (
                            "┊✧ 💙 1️⃣ HOUR TO GO 🪶 ✧┊\n"
                            "\n"
                            "Only 1 hour until the Sumin Party‼️\n"
                            "\n"
                            "🏷 Tags\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "Check the quoted post for details 🔎ˊ˗\n"
                            "\n"
                            "👇🏻 One-tap post\n"
                            "https://x.gd/XqCId"
                        ),
                        "zh": (
                            "┊✧ 💙距離開始還有1️⃣小時🪶 ✧┊\n"
                            "\n"
                            "距離Sumin派對開始還有1小時‼️\n"
                            "\n"
                            "🏷 標籤\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "請確認引用貼文的詳情🔎ˊ˗\n"
                            "\n"
                            "👇🏻一鍵發文\n"
                            "https://x.gd/XqCId"
                        ),
                        "ko": (
                            "┊✧ 💙1️⃣시간 전입니다🪶 ✧┊\n"
                            "\n"
                            "Sumin 파티까지 1시간 남았어요‼️\n"
                            "\n"
                            "🏷 태그\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "인용 포스트에서 자세한 내용 확인🔎ˊ˗\n"
                            "\n"
                            "👇🏻원터치 포스트\n"
                            "https://x.gd/XqCId"
                        ),
                    },
                    {
                        "title": "スミンパーティー終了",
                        "ja": (
                            "⋱ 💙STREAMING PARTY END🪶 ⋰\n"
                            "\n"
                            "ご参加ありがとうございました✨\n"
                            "次回も一緒に頑張っていきましょう！\n"
                            "\n"
                            "📮 視聴の感想はタグをつけて投稿\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "👇🏻ワンタッチポスト\n"
                            "https://x.gd/XqCId"
                        ),
                        "en": (
                            "⋱ 💙STREAMING PARTY END🪶 ⋰\n"
                            "\n"
                            "Thank you for joining us✨\n"
                            "Let's keep cheering together next time!\n"
                            "\n"
                            "📮 Share your thoughts with the tags\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "👇🏻 One-tap post\n"
                            "https://x.gd/XqCId"
                        ),
                        "zh": (
                            "⋱ 💙串流派對結束🪶 ⋰\n"
                            "\n"
                            "感謝您的參與✨\n"
                            "下次也一起加油吧！\n"
                            "\n"
                            "📮 請附上標籤分享您的觀看感想\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "👇🏻一鍵發文\n"
                            "https://x.gd/XqCId"
                        ),
                        "ko": (
                            "⋱ 💙스트리밍 파티 종료🪶 ⋰\n"
                            "\n"
                            "참여해 주셔서 감사합니다✨\n"
                            "다음에도 함께 열심히 해봐요！\n"
                            "\n"
                            "📮 시청 소감은 태그 달아서 포스팅\n"
                            "　#ジュアンジェイ_スミンパーティー\n"
                            "　#ジュアンジェイ\n"
                            "　#PRODUCE101JAPAN新世界\n"
                            "\n"
                            "👇🏻원터치 포스트\n"
                            "https://x.gd/XqCId"
                        ),
                    },
                ],
            },

            # ── タグイベ ────────────────────────────────────────────────
            {
                "h2": "タグイベ",
                "posts": [
                    {
                        "title": "タグイベお知らせ",
                        "ja": (
                            "┊✧ 💙HASHTAG EVENT!!🪶 ✧┊\n"
                            "\n"
                            "#ジュアンジェイ タグイベント\n"
                            "開催のお知らせ📣\n"
                            "\n"
                            "🔥 目指せトレンド入り🔥\n"
                            "\n"
                            "📅 開催日時\n"
                            "　[日時]\n"
                            "🏷 指定タグ\n"
                            "　#JustVoteJay\n"
                            "　#ジュアンジェイ\n"
                            "\n"
                            "詳細は画像とURLをチェック🔎ˊ˗\n"
                            "🔗 https://x.gd/kO2i6\n"
                            "\n"
                            "👇🏻ワンタッチポスト\n"
                            "https://x.gd/n2pLz"
                        ),
                        "en": (
                            "┊✧ 💙HASHTAG EVENT!!🪶 ✧┊\n"
                            "\n"
                            "Let's get him trending! 🔥\n"
                            "\n"
                            "📅 [日時] JST\n"
                            "\n"
                            "🏷 Tags\n"
                            "　#JustVoteJay\n"
                            "　#ジュアンジェイ\n"
                            "\n"
                            "Details in the image & link 🔎ˊ˗\n"
                            "🔗 https://x.gd/kO2i6\n"
                            "\n"
                            "👇🏻 One-tap post\n"
                            "https://x.gd/n2pLz"
                        ),
                        "zh": (
                            "┊✧ 💙HASHTAG EVENT!!🪶 ✧┊\n"
                            "\n"
                            "#ジュアンジェイ 標籤活動\n"
                            "舉辦通知📣\n"
                            "\n"
                            "🔥 目標衝上熱搜🔥\n"
                            "\n"
                            "📅 日期與時間\n"
                            "　[日時]\n"
                            "🏷 指定標籤\n"
                            "　#JustVoteJay\n"
                            "　#ジュアンジェイ\n"
                            "\n"
                            "詳情請確認圖片與連結🔎ˊ˗\n"
                            "🔗 https://x.gd/kO2i6\n"
                            "\n"
                            "👇🏻一鍵發文\n"
                            "https://x.gd/n2pLz"
                        ),
                        "ko": (
                            "┊✧ 💙HASHTAG EVENT!!🪶 ✧┊\n"
                            "\n"
                            "#ジュアンジェイ 태그 이벤트\n"
                            "개최 안내📣\n"
                            "\n"
                            "🔥 트렌드 진입을 목표로🔥\n"
                            "\n"
                            "📅 날짜 & 시간\n"
                            "　[日時]\n"
                            "🏷 지정 태그\n"
                            "　#JustVoteJay\n"
                            "　#ジュアンジェイ\n"
                            "\n"
                            "이미지 & URL 확인🔎ˊ˗\n"
                            "🔗 https://x.gd/kO2i6\n"
                            "\n"
                            "👇🏻원터치 포스트\n"
                            "https://x.gd/n2pLz"
                        ),
                    },
                    {
                        "title": "タグイベスタート",
                        "ja": (
                            "▷▶︎▷ 💙 HASHTAG EVENT START🪶 ▷▶︎▷\n"
                            "\n"
                            "▶️[日時]💥\n"
                            "\n"
                            "🏷️ タグをつけて投稿！\n"
                            "　#JustVoteJay\n"
                            "　#ジュアンジェイ\n"
                            "\n"
                            "詳細は画像とURLをチェック🔎ˊ˗\n"
                            "🔗 https://x.gd/kO2i6\n"
                            "\n"
                            "👇🏻ワンタッチポスト\n"
                            "https://x.gd/n2pLz"
                        ),
                        "en": (
                            "▷▶︎▷ 💙 HASHTAG EVENT START 🪶 ▷▶︎▷\n"
                            "\n"
                            "▶️ [日時] JST 💥\n"
                            "\n"
                            "🏷️ Post with the tags!\n"
                            "　#JustVoteJay\n"
                            "　#ジュアンジェイ\n"
                            "\n"
                            "Check the image & URL for details 🔎ˊ˗\n"
                            "🔗 https://x.gd/kO2i6\n"
                            "\n"
                            "👇🏻 One-tap post\n"
                            "https://x.gd/n2pLz"
                        ),
                        "zh": (
                            "▷▶︎▷ 💙 HASHTAG EVENT START 🪶 ▷▶︎▷\n"
                            "\n"
                            "▶️[日時]💥\n"
                            "\n"
                            "🏷️加上標籤發文！\n"
                            "　#JustVoteJay\n"
                            "　#ジュアンジェイ\n"
                            "\n"
                            "詳情請確認圖片與連結🔎ˊ˗\n"
                            "🔗 https://x.gd/kO2i6\n"
                            "\n"
                            "👇🏻一鍵發文\n"
                            "https://x.gd/n2pLz"
                        ),
                        "ko": (
                            "▷▶︎▷ 💙 HASHTAG EVENT START 🪶 ▷▶︎▷\n"
                            "\n"
                            "▶️[日時]💥\n"
                            "\n"
                            "🏷️태그 달고 포스팅！\n"
                            "　#JustVoteJay\n"
                            "　#ジュアンジェイ\n"
                            "\n"
                            "이미지 & URL 확인🔎ˊ˗\n"
                            "🔗 https://x.gd/kO2i6\n"
                            "\n"
                            "👇🏻원터치 포스트\n"
                            "https://x.gd/n2pLz"
                        ),
                    },
                    {
                        "title": "タグイベリマインド（1時間前）",
                        "ja": (
                            "┊✧ 💙開催まで1️⃣時間🪶 ✧┊\n"
                            "\n"
                            "タグイベまで1時間となりました‼️\n"
                            "\n"
                            "🏷 タグ\n"
                            "　#JustVoteJay\n"
                            "　#ジュアンジェイ\n"
                            "\n"
                            "詳細は引用元をチェック🔎ˊ˗\n"
                            "\n"
                            "👇🏻ワンタッチポスト\n"
                            "https://x.gd/n2pLz"
                        ),
                        "en": (
                            "┊✧ 💙 1 HOUR TO GO 🪶 ✧┊\n"
                            "\n"
                            "The tag event starts in 1 hour‼️\n"
                            "\n"
                            "🏷 Tags\n"
                            "　#JustVoteJay\n"
                            "　#ジュアンジェイ\n"
                            "\n"
                            "Check the quoted post for details 🔎ˊ˗\n"
                            "\n"
                            "👇🏻 One-tap post\n"
                            "https://x.gd/n2pLz"
                        ),
                        "zh": (
                            "┊✧ 💙距離開始還有1️⃣小時🪶 ✧┊\n"
                            "\n"
                            "距離標籤活動開始還有1小時‼️\n"
                            "\n"
                            "🏷 標籤\n"
                            "　#JustVoteJay\n"
                            "　#ジュアンジェイ\n"
                            "\n"
                            "請確認引用貼文的詳情🔎ˊ˗\n"
                            "\n"
                            "👇🏻一鍵發文\n"
                            "https://x.gd/n2pLz"
                        ),
                        "ko": (
                            "┊✧ 💙1️⃣시간 전입니다🪶 ✧┊\n"
                            "\n"
                            "태그 이벤트까지 1시간 남았어요‼️\n"
                            "\n"
                            "🏷 태그\n"
                            "　#JustVoteJay\n"
                            "　#ジュアンジェイ\n"
                            "\n"
                            "인용 포스트에서 자세한 내용 확인🔎ˊ˗\n"
                            "\n"
                            "👇🏻원터치 포스트\n"
                            "https://x.gd/n2pLz"
                        ),
                    },
                    {
                        "title": "タグイベ終了",
                        "ja": (
                            "⋱ 💙 HASHTAG EVENT END🪶 ⋰\n"
                            "\n"
                            "ご参加ありがとうございました✨\n"
                            "次回も一緒に頑張っていきましょう！\n"
                            "\n"
                            "ジェイくんの情報はこちらをチェック🔍ˊ˗\n"
                            "🔗 https://x.gd/4A61D"
                        ),
                        "en": (
                            "⋱ 💙 HASHTAG EVENT END 🪶 ⋰\n"
                            "\n"
                            "Thank you for joining us！✨\n"
                            "Let's keep cheering together next time!\n"
                            "\n"
                            "Check here for all things Chuang Jay 🔍ˊ˗\n"
                            "🔗 https://x.gd/4A61D"
                        ),
                        "zh": (
                            "⋱ 💙 HASHTAG EVENT END 🪶 ⋰\n"
                            "\n"
                            "感謝您的參與！✨\n"
                            "下次也一起加油吧！\n"
                            "\n"
                            "莊宗傑的相關資訊請點這裡🔍ˊ˗\n"
                            "🔗 https://x.gd/4A61D"
                        ),
                        "ko": (
                            "⋱ 💙 HASHTAG EVENT END 🪶 ⋰\n"
                            "\n"
                            "참여해 주셔서 감사합니다！✨\n"
                            "다음에도 함께 열심히 해봐요！\n"
                            "\n"
                            "장앙제이의 정보는 여기서 확인🔍ˊ˗\n"
                            "🔗 https://x.gd/4A61D"
                        ),
                    },
                ],
            },

            # ── HPお知らせ ──────────────────────────────────────────────
            {
                "h2": "HPお知らせ",
                "posts": [
                    {
                        "title": "HP開設",
                        "ja": (
                            "⋱ 💙JAYBIRDS HP公開🪶 ⋰\n"
                            "\n"
                            "JAYBIRDS HPを公開しました🎉\n"
                            "\n"
                            "✦ 応援情報\n"
                            "✦ 動画一覧\n"
                            "✦ 応援ガイド\n"
                            "✦ 布教素材\n"
                            "（随時更新予定）\n"
                            "\n"
                            "ぜひブックマークを📌💙\n"
                            "\n"
                            "🔗 https://x.gd/vja9F\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "en": (
                            "⋱ 💙 JAYBIRDS SITE IS LIVE 🪶 ⋰\n"
                            "\n"
                            "Your go-to hub for all Jay support is here！🎉\n"
                            "\n"
                            "✦ Updates\n"
                            "✦ Videos\n"
                            "✦ Fan Guide\n"
                            "✦ Promo Materials\n"
                            "（More coming soon）\n"
                            "\n"
                            "Bookmark it！📌💙\n"
                            "\n"
                            "🔗 https://x.gd/vja9F\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "zh": (
                            "⋱ 💙JAYBIRDS 官網上線🪶 ⋰\n"
                            "\n"
                            "JAYBIRDS官方網站正式上線🎉\n"
                            "\n"
                            "✦ 應援資訊\n"
                            "✦ 影片列表\n"
                            "✦ 應援指南\n"
                            "✦ 推廣素材\n"
                            "（持續更新中）\n"
                            "\n"
                            "請加入書籤📌💙\n"
                            "\n"
                            "🔗 https://x.gd/vja9F\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "ko": (
                            "⋱ 💙JAYBIRDS 홈페이지 오픈🪶 ⋰\n"
                            "\n"
                            "JAYBIRDS 공식 홈페이지를 공개했습니다🎉\n"
                            "\n"
                            "✦ 응원 정보\n"
                            "✦ 동영상 목록\n"
                            "✦ 팬 가이드\n"
                            "✦ 홍보 소재\n"
                            "（수시 업데이트 중）\n"
                            "\n"
                            "북마크 저장 필수📌💙\n"
                            "\n"
                            "🔗 https://x.gd/vja9F\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                    },
                    {
                        "title": "投票ガイド公開",
                        "ja": (
                            "⋱ 💙投票ガイドページ公開🪶 ⋰\n"
                            "\n"
                            "🗓️ 初日の1票を逃さないために\n"
                            "放送前に準備しましょう💪\n"
                            "\n"
                            "✦ dアカウント作成（SMS認証まで）\n"
                            "✦ Leminoアプリ DL＆ログイン\n"
                            "✦ 海外の方は MNet+アプリ\n"
                            "\n"
                            "詳細はこちら🔍ˊ˗\n"
                            "🔗 https://x.gd/63FPj\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "en": (
                            "⋱ 💙 Voting Guide Now Live 🪶 ⋰\n"
                            "\n"
                            "🗓️ Don't miss your first vote —\n"
                            "Get ready before the broadcast starts💪\n"
                            "\n"
                            "✦ Create a d-account（up to SMS verification）\n"
                            "✦ Download & log in to the Lemino app\n"
                            "✦ International fans: use the MNet+ app\n"
                            "\n"
                            "Full guide here🔍ˊ˗\n"
                            "🔗 https://x.gd/63FPj\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "zh": (
                            "⋱ 💙 投票指南現已公開 🪶 ⋰\n"
                            "\n"
                            "🗓️ 不要錯過第一天的首次投票 —\n"
                            "請在節目開始前做好準備💪\n"
                            "\n"
                            "✦ 下載並登入 MNet+ 應用程式\n"
                            "\n"
                            "🌐 建議使用自動翻譯！\n"
                            "查看指南請點這裡🔍ˊ˗\n"
                            "🔗 https://x.gd/63FPj\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "ko": (
                            "⋱ 💙 투표 가이드 공개 🪶 ⋰\n"
                            "\n"
                            "🗓️ 첫날 투표를 놓치지 않도록\n"
                            "방송 전에 준비해 두세요💪\n"
                            "\n"
                            "✦ MNet+ 앱을 다운로드 & 로그인\n"
                            "\n"
                            "자세한 가이드는 여기서🔍ˊ˗\n"
                            "🔗 https://x.gd/63FPj\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                    },
                    {
                        "title": "番組スケジュール公開",
                        "ja": (
                            "⋱ 💙ロードマップページ公開🪶 ⋰\n"
                            "\n"
                            "JAYBIRDSのHPに\n"
                            "番組スケジュールを追加⟡.*\n"
                            "\n"
                            "✦ そもそも日プって何？\n"
                            "✦ 今後どんな流れで進むの？\n"
                            "✦ 投票はいつ・何人選べるの？\n"
                            "\n"
                            "初めて見る方もこれで安心❣️\n"
                            "\n"
                            "🔗 https://x.gd/qN046\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "en": (
                            "⋱ 💙 Roadmap Page Now Live 🪶 ⋰\n"
                            "\n"
                            "The show schedule has been added\n"
                            "to the JAYBIRDS website⟡.*\n"
                            "\n"
                            "✦ What even is Nichi-Pu?\n"
                            "✦ How does the show progress?\n"
                            "✦ When & how many can we vote?\n"
                            "\n"
                            "Perfect for first-timers❣️\n"
                            "\n"
                            "🔗 https://x.gd/qN046\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "zh": (
                            "⋱ 💙 行程指南現已公開 🪶 ⋰\n"
                            "\n"
                            "第一次接觸節目嗎？從這裡開始⟡.*\n"
                            "\n"
                            "你需要知道的一切 — 全都整理在一頁中❣️\n"
                            "\n"
                            "🌐 建議使用自動翻譯！\n"
                            "🔗 https://x.gd/qN046\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "ko": (
                            "⋱ 💙 로드맵 페이지 공개 🪶 ⋰\n"
                            "\n"
                            "JAYBIRDS 홈페이지에\n"
                            "방송 일정 페이지를 추가했어요⟡.*\n"
                            "\n"
                            "✦ 그래서 일본 프듀가 뭔가요？\n"
                            "✦ 앞으로 어떻게 진행되나요？\n"
                            "✦ 투표는 언제, 몇 명을 뽑나요？\n"
                            "\n"
                            "처음 보시는 분도 이걸로 안심❣️\n"
                            "\n"
                            "🔗 https://x.gd/qN046\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                    },
                    {
                        "title": "投票ウェイト解説",
                        "ja": (
                            "📊 日プ新世界✦投票の仕組み\n"
                            "\n"
                            "‼️徹底検証 & 大解説‼️\n"
                            "\n"
                            "✅ 国民票とSEKAI票の違いは？\n"
                            "✅ 7:3の重みって実際どう効く？\n"
                            "✅ 1票の価値って何？\n"
                            "\n"
                            "👇🏻全部シミュレーターで確かめられます\n"
                            "https://x.gd/w2a6z\n"
                            "\n"
                            "全プロデューサー・FDに届け🔍\n"
                            "\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI #日プ新世界"
                        ),
                        "en": (
                            "📊 Nichi-Pu Shinsekai✦ How Voting Works\n"
                            "\n"
                            "‼️ Deep Dive & Full Breakdown ‼️\n"
                            "\n"
                            "✅ What's the difference between national & SEKAI votes?\n"
                            "✅ How does the 70:30 weight actually work?\n"
                            "✅ What is one vote really worth?\n"
                            "\n"
                            "👇🏻 Check it all in the simulator\n"
                            "https://x.gd/w2a6z\n"
                            "\n"
                            "Pass this on to all producers & FDs 🔍\n"
                            "\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                        "zh": (
                            "📊 101新世界✦投票機制\n"
                            "\n"
                            "‼️徹底解析 & 大解說‼️\n"
                            "\n"
                            "✅ 國民票與SEKAI票有什麼差別？\n"
                            "✅ 70:30的權重實際上如何影響？\n"
                            "✅ 1票的價值是什麼？\n"
                            "\n"
                            "👇🏻全部都可以用模擬器確認\n"
                            "https://x.gd/w2a6z\n"
                            "\n"
                            "傳達給所有製作人・FD🔍\n"
                            "\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                        "ko": (
                            "📊 일본 프듀 신세계✦ 투표 구조\n"
                            "\n"
                            "‼️철저 검증 & 대해설‼️\n"
                            "\n"
                            "✅ 국민票와 SEKAI票의 차이는？\n"
                            "✅ 70:30의 가중치는 실제로 어떻게 작동하나？\n"
                            "✅ 1票의 가치는 무엇인가？\n"
                            "\n"
                            "👇🏻 시뮬레이터로 직접 확인해보세요\n"
                            "https://x.gd/w2a6z\n"
                            "\n"
                            "모든 프로듀서・FD에게 전달🔍\n"
                            "\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                    },
                    {
                        "title": "スクショシェア企画",
                        "ja": (
                            "⋱ 📸 スクショシェア企画 💥⋰\n"
                            "\n"
                            "シェアがジェイくんの力になる‼️\n"
                            "サイトでスクショを引いてポスト🎲\n"
                            "\n"
                            "そして…運営だけではスクショが足りない💦\n"
                            "上手く撮れた方はぜひご提供ください\n"
                            "\n"
                            "#ジュアンジェイ #ジェイどこ #FINDJAY #PRODUCE101JAPAN新世界\n"
                            "\n"
                            "👇🏻まずは一度引いてみて\n"
                            "https://x.gd/FXiv3"
                        ),
                        "en": (
                            "⋱ 📸 Screenshot Share Project 💥⋰\n"
                            "\n"
                            "Spreading Jay's screenshots = direct support‼️\n"
                            "Draw a random screenshot & post it🎲\n"
                            "\n"
                            "We also need more screenshots from fans💦\n"
                            "If you've got good ones, please share them!\n"
                            "\n"
                            "#ジュアンジェイ #ジェイどこ #FINDJAY #PRODUCE101JAPAN新世界\n"
                            "\n"
                            "👇🏻 Give it a try!\n"
                            "https://x.gd/FXiv3"
                        ),
                        "zh": (
                            "⋱ 📸 擴散截圖企劃 💥⋰\n"
                            "\n"
                            "擴散莊宗傑截圖就是支持他的力量‼️\n"
                            "隨機抽截圖，一鍵發文到X🎲\n"
                            "\n"
                            "也歡迎提供截圖給我們🙇\n"
                            "\n"
                            "#ジュアンジェイ #ジェイどこ #FINDJAY #PRODUCE101JAPAN新世界\n"
                            "\n"
                            "👇🏻快來試試看！\n"
                            "https://x.gd/FXiv3"
                        ),
                        "ko": (
                            "⋱ 📸 스크린샷 공유 프로젝트 💥⋰\n"
                            "\n"
                            "공유가 장앙제이의 힘이 됩니다‼️\n"
                            "사이트에서 스크린샷을 뽑아서 포스팅🎲\n"
                            "\n"
                            "운영진만으로는 스크린샷이 부족해요💦\n"
                            "잘 찍으신 분들은 꼭 제공 부탁드려요\n"
                            "\n"
                            "#ジュアンジェイ #ジェイどこ #FINDJAY #PRODUCE101JAPAN新世界\n"
                            "\n"
                            "👇🏻일단 한 번 뽑아보세요\n"
                            "https://x.gd/FXiv3"
                        ),
                    },
                    {
                        "title": "スクショシェアアプデ",
                        "ja": (
                            "⋱ 📸 スクショシェア機能アップデート 💥⋰\n"
                            "\n"
                            "#ジュアンジェイ のスクショを\n"
                            "\n"
                            "🪶 各話毎\n"
                            "🪶 全話\n"
                            "\n"
                            "ランダムで受け取れるようになりました！\n"
                            "\n"
                            "保存・シェア自由です💙\n"
                            "みんなでジェイくんを盛り上げよう🔥\n"
                            "\n"
                            "👉 https://x.gd/FXiv3\n"
                            "#ジェイどこ #FINDJAY #PRODUCE101JAPAN新世界"
                        ),
                        "en": (
                            "📸✨ Screenshot Share feature updated!\n"
                            "\n"
                            "Get random screenshots of Chuang Jay —\n"
                            "🪶 by episode\n"
                            "🪶 or all episodes together!\n"
                            "\n"
                            "Free to save & share💙\n"
                            "Let's spread Jay's charm together🔥\n"
                            "\n"
                            "👉 https://x.gd/FXiv3\n"
                            "#ジェイどこ #FINDJAY #PRODUCE101JAPAN新世界"
                        ),
                        "zh": (
                            "📸✨ 截圖分享功能更新啦！\n"
                            "\n"
                            "可以隨機獲得莊宗傑的截圖💙\n"
                            "🪶 按集數選擇\n"
                            "🪶 或全集一起\n"
                            "\n"
                            "可以自由保存・分享🔥\n"
                            "一起為JAY加油吧！\n"
                            "\n"
                            "👉 https://x.gd/FXiv3\n"
                            "#ジェイどこ #FINDJAY #PRODUCE101JAPAN新世界"
                        ),
                        "ko": (
                            "📸✨ 스크린샷 공유 기능 업데이트！\n"
                            "\n"
                            "#ジュアンジェイ 스크린샷을\n"
                            "🪶 각 화별\n"
                            "🪶 전체 화\n"
                            "\n"
                            "무작위로 받을 수 있게 됐어요！\n"
                            "\n"
                            "저장・공유 자유💙\n"
                            "모두 함께 제이를 알립시다🔥\n"
                            "\n"
                            "👉 https://x.gd/FXiv3\n"
                            "#ジェイどこ #FINDJAY #PRODUCE101JAPAN新世界"
                        ),
                    },
                ],
            },

            # ── 応援素材配布 ────────────────────────────────────────────
            {
                "h2": "応援素材配布",
                "posts": [
                    {
                        "title": "応援素材配布（Galleryページ公開）",
                        "ja": (
                            "⋱ 💙応援素材ページ公開🪶 ⋰\n"
                            "\n"
                            "JAYBIRDSのホームページに\n"
                            "Galleryページを追加しました⟡.*\n"
                            "\n"
                            "✦ アイコンフレーム\n"
                            "✦ X布教画像\n"
                            "（随時更新予定）\n"
                            "\n"
                            "ご自由にお使いください❣️\n"
                            "\n"
                            "🔗 https://x.gd/RkLvF\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "en": (
                            "⋱ 💙 SUPPORT MATERIALS PAGE OPEN 🪶 ⋰\n"
                            "\n"
                            "A Gallery page has been added\n"
                            "to the JAYBIRDS website⟡.*\n"
                            "\n"
                            "✦ Icon Frames\n"
                            "✦ X Promotion Images\n"
                            "（More updates coming soon）\n"
                            "\n"
                            "All materials are free to use❣️\n"
                            "\n"
                            "🔗 https://x.gd/RkLvF\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "zh": (
                            "⋱ 💙應援素材頁面上線🪶 ⋰\n"
                            "\n"
                            "JAYBIRDS官網新增了\n"
                            "Gallery頁面⟡.*\n"
                            "\n"
                            "✦ 頭像框\n"
                            "✦ X宣傳圖片\n"
                            "（持續更新中）\n"
                            "\n"
                            "歡迎自由取用❣️\n"
                            "\n"
                            "🔗 https://x.gd/RkLvF\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "ko": (
                            "⋱ 💙응원 소재 페이지 공개🪶 ⋰\n"
                            "\n"
                            "JAYBIRDS 홈페이지에\n"
                            "Gallery 페이지를 추가했습니다⟡.*\n"
                            "\n"
                            "✦ 아이콘 프레임\n"
                            "✦ X 홍보 이미지\n"
                            "（수시 업데이트 중）\n"
                            "\n"
                            "자유롭게 사용해 주세요❣️\n"
                            "\n"
                            "🔗 https://x.gd/RkLvF\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                    },
                    {
                        "title": "素材シェア企画",
                        "ja": (
                            "⋱ 🎨素材シェア企画🪶 ⋰\n"
                            "\n"
                            "応援したいけど素材作りが苦手な方と\n"
                            "素材を作ってくださる方を\n"
                            "繋げる企画です💙⟡.*\n"
                            "\n"
                            "作った素材をギャラリーに掲載して\n"
                            "一緒にジェイくんを広めよう🪶✨\n"
                            "\n"
                            "詳しくはこちら👇\n"
                            "🔗 https://x.gd/RkLvF\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "en": (
                            "⋱ 🎨 Material Sharing Project 🪶 ⋰\n"
                            "\n"
                            "Connecting fans who want to support Jay\n"
                            "with those who can create materials💙⟡.*\n"
                            "\n"
                            "Share your designs in the gallery\n"
                            "and let's spread Jay's charm together🪶✨\n"
                            "\n"
                            "Details here👇\n"
                            "🔗 https://x.gd/RkLvF\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "zh": (
                            "⋱ 🎨素材分享企劃🪶 ⋰\n"
                            "\n"
                            "連結想應援莊宗傑卻不擅長製作素材的粉絲\n"
                            "與願意製作素材的創作者💙⟡.*\n"
                            "\n"
                            "將製作好的素材發布到Gallery\n"
                            "一起讓更多人認識JAY吧🪶✨\n"
                            "\n"
                            "詳情請點這裡👇\n"
                            "🔗 https://x.gd/RkLvF\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "ko": (
                            "⋱ 🎨 소재 공유 프로젝트 🪶 ⋰\n"
                            "\n"
                            "응원하고 싶지만 소재 제작이 어려운 팬과\n"
                            "소재를 만들어 주실 분을 연결하는 프로젝트💙⟡.*\n"
                            "\n"
                            "만든 소재를 갤러리에 올리고\n"
                            "함께 장앙제이를 알립시다🪶✨\n"
                            "\n"
                            "자세한 내용은 여기서👇\n"
                            "🔗 https://x.gd/RkLvF\n"
                            "\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                    },
                ],
            },

            # ── アイコンフレーム配布 ────────────────────────────────────
            {
                "h2": "アイコンフレーム配布",
                "posts": [
                    {
                        "title": "アイコンフレーム配布",
                        "ja": (
                            "⋱ 💙アイコンフレーム配布‼️🪶 ⋰\n"
                            "\n"
                            "JAYBIRDSの皆様、お待たせ致しました⟡.*\n"
                            "#ジュアンジェイ 応援アイコンフレーム\n"
                            "を配布いたします🎉\n"
                            "\n"
                            "下記リンクよりご自由にお使いください❣️\n"
                            "\n"
                            "🔗 https://icondecotter.jp/detail.php?id=107098\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "en": (
                            "⋱ 💙 Icon Frame Distribution!! 🪶 ⋰\n"
                            "\n"
                            "JAYBIRDS, thank you for your patience⟡.*\n"
                            "We're now distributing the\n"
                            "#ジュアンジェイ support icon frames🎉\n"
                            "\n"
                            "Download freely from the link below❣️\n"
                            "\n"
                            "🔗 https://icondecotter.jp/detail.php?id=107098\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "zh": (
                            "⋱ 💙 頭像框發放！！🪶 ⋰\n"
                            "\n"
                            "JAYBIRDS，感謝久等⟡.*\n"
                            "現在發放\n"
                            "#ジュアンジェイ 應援頭像框🎉\n"
                            "\n"
                            "請自由從以下連結下載使用❣️\n"
                            "\n"
                            "🔗 https://icondecotter.jp/detail.php?id=107098\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                        "ko": (
                            "⋱ 💙 아이콘 프레임 배포!! 🪶 ⋰\n"
                            "\n"
                            "JAYBIRDS 여러분, 기다려 주셔서 감사합니다⟡.*\n"
                            "#ジュアンジェイ 응원 아이콘 프레임을\n"
                            "배포합니다🎉\n"
                            "\n"
                            "아래 링크에서 자유롭게 사용하세요❣️\n"
                            "\n"
                            "🔗 https://icondecotter.jp/detail.php?id=107098\n"
                            "#JAY羽ばたくじぇい #ジュアンジェイ #PRODUCE101JAPAN新世界"
                        ),
                    },
                    {
                        "title": "布教フライヤー配布",
                        "ja": (
                            "🖼️ 布教フライヤー配布 🎨\n"
                            "\n"
                            "有志の方作成の布教フライヤーを配布しています‼️\n"
                            "SNSでの布教活動、印刷して掲示など\n"
                            "様々な場面でご活用いただけます🪶\n"
                            "\n"
                            "🔗 https://x.gd/RkLvF\n"
                            "\n"
                            "#JAY羽ばたくじぇい\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界"
                        ),
                        "en": (
                            "🖼️ Promo Flyer Distribution 🎨\n"
                            "\n"
                            "Fan-made promo flyers are now available‼️\n"
                            "Use them for SNS promotion, printing & display,\n"
                            "and more🪶\n"
                            "\n"
                            "🔗 https://x.gd/RkLvF\n"
                            "\n"
                            "#JAY羽ばたくじぇい\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界"
                        ),
                        "zh": (
                            "🖼️ 宣傳傳單發放 🎨\n"
                            "\n"
                            "由志願者製作的宣傳傳單現正提供下載‼️\n"
                            "可用於SNS宣傳活動，或列印後張貼等\n"
                            "適用於各種不同場景🪶\n"
                            "\n"
                            "🔗 https://x.gd/RkLvF\n"
                            "\n"
                            "#JAY羽ばたくじぇい\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界"
                        ),
                        "ko": (
                            "🖼️ 홍보 플라이어 배포 🎨\n"
                            "\n"
                            "팬이 제작한 홍보 플라이어를 배포합니다‼️\n"
                            "SNS 홍보 활동, 인쇄 후 게시 등\n"
                            "다양한 용도로 활용해 주세요🪶\n"
                            "\n"
                            "🔗 https://x.gd/RkLvF\n"
                            "\n"
                            "#JAY羽ばたくじぇい\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界"
                        ),
                    },
                ],
            },
        ],
    },

    # ════════════════════════════════════════════════════════════════════
    # TikTok投稿
    # ════════════════════════════════════════════════════════════════════
    {
        "h1": "TikTok投稿",
        "sections": [
            {
                "h2": None,
                "posts": [
                    {
                        "title": "TikTokタグ一覧",
                        "ja": (
                            "TikTok投稿時に使用するタグ\n"
                            "\n"
                            "#ジェイどこ\n"
                            "#FINDJAY\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                        "en": (
                            "Tags to use for TikTok posts\n"
                            "\n"
                            "#ジェイどこ\n"
                            "#FINDJAY\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                        "zh": (
                            "TikTok發文時使用的標籤\n"
                            "\n"
                            "#ジェイどこ\n"
                            "#FINDJAY\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                        "ko": (
                            "TikTok 포스팅 시 사용하는 태그\n"
                            "\n"
                            "#ジェイどこ\n"
                            "#FINDJAY\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                    },
                    {
                        "title": "ジェイどこ投稿（TikTok）",
                        "ja": (
                            "┊✧ 🎥ジェイどこ？ ✧┊\n"
                            "この動画の中にジェイくんが隠れています🕵️ˊ˗\n"
                            "あなたは見つけられますか？👀\n"
                            "見つけた方はぜひコメントで教えてください💙🪶\n"
                            "#ジェイどこ\n"
                            "#FINDJAY\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                        "en": (
                            "┊✧ 🎥 Where's Jay? ✧┊\n"
                            "Jay is hiding somewhere in this video🕵️ˊ˗\n"
                            "Can you find him?👀\n"
                            "Drop a comment if you spot him!💙🪶\n"
                            "#ジェイどこ\n"
                            "#FINDJAY\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                        "zh": (
                            "┊✧ 🎥 JAY在哪裡？ ✧┊\n"
                            "這支影片裡藏著莊宗傑🕵️ˊ˗\n"
                            "你找到了嗎？👀\n"
                            "找到的話請在留言告訴我們！💙🪶\n"
                            "#ジェイどこ\n"
                            "#FINDJAY\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                        "ko": (
                            "┊✧ 🎥 제이 어디있어？ ✧┊\n"
                            "이 영상 어딘가에 장앙제이가 숨어있어요🕵️ˊ˗\n"
                            "찾으셨나요？👀\n"
                            "찾으신 분은 댓글로 알려주세요！💙🪶\n"
                            "#ジェイどこ\n"
                            "#FINDJAY\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                    },
                    {
                        "title": "スクショ共有編（TikTok）",
                        "ja": (
                            "┊✧ 🎥ジェイどこ？ ✧┊\n"
                            "[話数]のジェイくんの出演場面を発見しました🕵️ˊ˗\n"
                            "あなたは見つけられましたか？👀\n"
                            "他にも見つけた方はぜひ\n"
                            "コメントで教えてください💙🪶\n"
                            "#ジェイどこ\n"
                            "#FINDJAY\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                        "en": (
                            "┊✧ 🎥 Where's Jay? ✧┊\n"
                            "I found Chuang Jay's appearances in [話数]🕵️ˊ˗\n"
                            "Did you spot him too?👀\n"
                            "Found other moments?\n"
                            "Drop them in the comments!💙🪶\n"
                            "#ジェイどこ\n"
                            "#FINDJAY\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                        "zh": (
                            "┊✧ 🎥 JAY在哪裡？ ✧┊\n"
                            "發現了莊宗傑在[話数]的出場場面🕵️ˊ˗\n"
                            "你也找到了嗎？👀\n"
                            "還有其他發現的場面嗎？\n"
                            "歡迎留言告訴我們！💙🪶\n"
                            "#ジェイどこ\n"
                            "#FINDJAY\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                        "ko": (
                            "┊✧ 🎥 제이 어디있어？ ✧┊\n"
                            "[話数]에서 장앙제이의 출연 장면을 발견했어요🕵️ˊ˗\n"
                            "찾으셨나요？👀\n"
                            "다른 장면도 발견하신 분은\n"
                            "댓글로 알려주세요！💙🪶\n"
                            "#ジェイどこ\n"
                            "#FINDJAY\n"
                            "#ジュアンジェイ\n"
                            "#PRODUCE101JAPAN新世界\n"
                            "#101SHINSEKAI"
                        ),
                    },
                ],
            },
        ],
    },

    # ════════════════════════════════════════════════════════════════════
    # OC（オープンチャット）
    # ════════════════════════════════════════════════════════════════════
    {
        "h1": "OC（オープンチャット）",
        "sections": [
            {
                "h2": "投票リマインド",
                "posts": [
                    {
                        "title": "OC投票リマインド（詳細版）",
                        "ja": (
                            "🗳️⚡️⚡️投票のお願い⚡️⚡️🗳️\n"
                            "\n"
                            "本日分の投票はお済みですか？\n"
                            "\n"
                            "どうか毎日2️⃣票🔥🔥お忘れなく🔥🔥\n"
                            "投票と呼びかけをよろしくお願いします🙇\n"
                            "\n"
                            "【JAYBIRDS全員】の投票・布教で\n"
                            "ジェイくんを応援しましょう💙🪶\n"
                            "\n"
                            "🗳️ 公式で投票👇\n"
                            "🔗 https://vote.produce101.jp\n"
                            "📱 Leminoアプリから投票を！\n"
                            "\n"
                            "🗳️ 投票の流れはこちら👇\n"
                            "🔗 https://x.gd/63FPj\n"
                            "📱 投票方法の動画👇\n"
                            "🔗 https://vt.tiktok.com/ZSuw3yp3V/"
                        ),
                        "en": (
                            "🗳️⚡️⚡️ Please Vote ⚡️⚡️🗳️\n"
                            "\n"
                            "Have you cast today's votes?\n"
                            "\n"
                            "Don't forget your daily vote🔥\n"
                            "Please vote and spread the word🙇\n"
                            "\n"
                            "Let's support Chuang Jay with\n"
                            "every JAYBIRD's vote & fandom💙🪶\n"
                            "\n"
                            "🗳️ Official vote👇\n"
                            "🔗 https://vote.produce101.jp\n"
                            "📱 Vote via the Mnet+ app!\n"
                            "\n"
                            "🗳️ Step-by-step voting guide👇\n"
                            "🔗 https://x.gd/63FPj\n"
                            "📱 How-to video👇\n"
                            "🔗 https://vt.tiktok.com/ZSuw3yp3V/"
                        ),
                        "zh": (
                            "🗳️⚡️⚡️請投票⚡️⚡️🗳️\n"
                            "\n"
                            "今天的投票完成了嗎？\n"
                            "\n"
                            "別忘了每天1️⃣次投票🔥\n"
                            "請多多投票並幫忙宣傳🙇\n"
                            "\n"
                            "讓每一位JAYBIRD的投票與支持\n"
                            "一起為莊宗傑加油💙🪶\n"
                            "\n"
                            "🗳️ 官方投票👇\n"
                            "🔗 https://vote.produce101.jp\n"
                            "📱 請從Mnet+應用程式投票！\n"
                            "\n"
                            "🗳️ 詳細投票方法👇\n"
                            "🔗 https://x.gd/63FPj\n"
                            "📱 投票方法影片👇\n"
                            "🔗 https://vt.tiktok.com/ZSuw3yp3V/"
                        ),
                        "ko": (
                            "🗳️⚡️⚡️ 투표 부탁드립니다 ⚡️⚡️🗳️\n"
                            "\n"
                            "오늘 투표 완료하셨나요?\n"
                            "\n"
                            "매일 1️⃣표🔥를 잊지 마세요\n"
                            "투표와 홍보 부탁드립니다🙇\n"
                            "\n"
                            "【JAYBIRDS 모두】의 투표와 홍보로\n"
                            "장앙제이를 응원합시다💙🪶\n"
                            "\n"
                            "🗳️ 공식 투표👇\n"
                            "🔗 https://vote.produce101.jp\n"
                            "📱 Mnet+ 앱에서 투표를!\n"
                            "\n"
                            "🗳️ 투표 방법 자세히 보기👇\n"
                            "🔗 https://x.gd/63FPj\n"
                            "📱 투표 방법 동영상👇\n"
                            "🔗 https://vt.tiktok.com/ZSuw3yp3V/"
                        ),
                    },
                ],
            },
        ],
    },
]


# ──────────────────────────────────────────────────────────────────────────────
# ユーティリティ
# ──────────────────────────────────────────────────────────────────────────────

def utf16_len(s: str) -> int:
    """Google Docs API は UTF-16 コードユニット数でインデックスを計算する。"""
    return sum(2 if ord(c) > 0xFFFF else 1 for c in s)


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


# ──────────────────────────────────────────────────────────────────────────────
# コンテンツ構築
# ──────────────────────────────────────────────────────────────────────────────

def build_segments():
    """全コンテンツをセグメントリストとして構築。
    Returns: (segments, total_posts)
    segments: [(text, style), ...]
      style: None | "HEADING_1" | "HEADING_2" | "BOLD"
    """
    segments = []
    total_posts = 0

    for section in DOCUMENT_DATA:
        # H1 見出し
        segments.append((section["h1"] + "\n", "HEADING_1"))
        segments.append(("\n", None))

        for sec in section.get("sections", []):
            # H2 見出し（None の場合はスキップ）
            if sec.get("h2"):
                segments.append((sec["h2"] + "\n", "HEADING_2"))
                segments.append(("\n", None))

            for post in sec.get("posts", []):
                # 区切り線 → タイトル（太字） → 区切り線 → 本文
                segments.append((SEP + "\n", None))
                segments.append(("📌 " + post["title"] + "\n", "BOLD"))
                segments.append((SEP + "\n", None))
                segments.append(("\n", None))
                segments.append(("【日本語】\n" + post["ja"] + "\n", None))
                segments.append(("\n", None))
                segments.append(("【English】\n" + post["en"] + "\n", None))
                segments.append(("\n", None))
                segments.append(("【繁体字中国語】\n" + post["zh"] + "\n", None))
                segments.append(("\n", None))
                segments.append(("【한국어】\n" + post["ko"] + "\n", None))
                segments.append(("\n", None))
                segments.append(("---\n", None))
                segments.append(("\n", None))
                total_posts += 1

        segments.append(("\n", None))

    return segments, total_posts


# ──────────────────────────────────────────────────────────────────────────────
# メイン処理
# ──────────────────────────────────────────────────────────────────────────────

def main():
    creds = get_credentials()
    service = build("docs", "v1", credentials=creds)

    # 現在のドキュメント末尾インデックスを取得
    print("ドキュメント情報を取得中...")
    doc = service.documents().get(documentId=DOCUMENT_ID).execute()
    body_content = doc.get("body", {}).get("content", [])
    doc_end_index = body_content[-1]["endIndex"] if body_content else 1

    print("テキストを構築中...")
    segments, total_posts = build_segments()
    full_text = "".join(s[0] for s in segments)

    # ── リクエスト構築 ────────────────────────────────────────────────
    requests_delete_insert = []

    # 1. 既存コンテンツを全削除
    if doc_end_index > 1:
        requests_delete_insert.append({
            "deleteContentRange": {
                "range": {
                    "startIndex": 1,
                    "endIndex": doc_end_index - 1,
                }
            }
        })

    # 2. 全テキストを一括挿入
    requests_delete_insert.append({
        "insertText": {
            "location": {"index": 1},
            "text": full_text,
        }
    })

    # 3. 見出し・太字スタイルリクエストを構築（UTF-16 位置を追跡）
    requests_style = []
    pos = 1
    for text, style in segments:
        text_len = utf16_len(text)
        if style in ("HEADING_1", "HEADING_2"):
            requests_style.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": pos, "endIndex": pos + text_len},
                    "paragraphStyle": {"namedStyleType": style},
                    "fields": "namedStyleType",
                }
            })
        elif style == "BOLD":
            # 末尾の \n を除いて太字にする
            requests_style.append({
                "updateTextStyle": {
                    "range": {"startIndex": pos, "endIndex": pos + text_len - 1},
                    "textStyle": {"bold": True},
                    "fields": "bold",
                }
            })
        pos += text_len

    # ── API 実行（削除＋挿入 → スタイル適用） ────────────────────────
    print(f"Googleドキュメントに書き込み中... ({total_posts}件)")

    service.documents().batchUpdate(
        documentId=DOCUMENT_ID,
        body={"requests": requests_delete_insert},
    ).execute()

    # スタイルリクエストをバッチサイズ 100 で分割実行
    BATCH_SIZE = 100
    for i in range(0, len(requests_style), BATCH_SIZE):
        service.documents().batchUpdate(
            documentId=DOCUMENT_ID,
            body={"requests": requests_style[i : i + BATCH_SIZE]},
        ).execute()

    print(f"✅ {total_posts}件の書き込み完了！")
    print(f"https://docs.google.com/document/d/{DOCUMENT_ID}/edit")


if __name__ == "__main__":
    main()
