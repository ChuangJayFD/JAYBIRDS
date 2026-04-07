#!/usr/bin/env python3
"""
save_post.py — JAYBIRDS投稿ログをGoogleドキュメントの該当セクションに保存するスクリプト

必要なパッケージ:
  pip install google-auth google-api-python-client
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build

DOCUMENT_ID = "18joYd8QNFwzLUUz0VFbihK0_Ij1JwpA-n3Y0FbbpZl8"
SCOPES = ["https://www.googleapis.com/auth/documents"]
JST = timezone(timedelta(hours=9))

# ドキュメントのセクション構成（import_keep.py の見出し構造と一致させること）
SECTION_MAP = {
    "X": {
        "parent": "X投稿",
        "children": [
            "HPお知らせ",
            "応援素材配布",
            "アイコンフレーム配布",
            "公式投稿引用",
            "ジェイどこ動画",
            "スミンパーティー",
            "タグイベ",
            "投票",
            "放送用",
        ],
    },
    "TikTok": {
        "parent": "TikTok投稿",
        "children": [],
    },
    "OC": {
        "parent": "OC（オープンチャット）",
        "children": ["投票リマインド"],
    },
}


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


def get_paragraph_text(paragraph):
    """段落の全テキストを結合して返す（末尾改行・空白を除去）"""
    text = ""
    for elem in paragraph.get("elements", []):
        text += elem.get("textRun", {}).get("content", "")
    return text.rstrip("\n").strip()


def find_insert_index(body_content, media, kind):
    """
    挿入先のインデックスを返す。
    - 種別が指定されている場合：親セクション内の該当子見出し直後
    - 種別が未指定の場合：親見出し直後
    - 見つからない場合はドキュメント先頭（index=1）にフォールバック
    """
    media_info = SECTION_MAP.get(media)
    if not media_info:
        print(
            f"ERROR: 未知の媒体 '{media}'。X / TikTok / OC のいずれかを指定してください。",
            file=sys.stderr,
        )
        sys.exit(1)

    parent_text = media_info["parent"]
    children = media_info["children"]

    parent_found = False
    parent_end_index = None

    for element in body_content:
        para = element.get("paragraph")
        if not para:
            continue
        text = get_paragraph_text(para)
        end_index = element.get("endIndex", 1)

        # 親見出しを探す（"# テキスト" または "テキスト" そのまま）
        if not parent_found:
            if text == parent_text or text == f"# {parent_text}":
                parent_found = True
                parent_end_index = end_index
            continue

        # 親を見つけた後、次の親レベルに達したら探索終了
        if text.startswith("# ") and text[2:].strip() != parent_text:
            break

        # 子セクションを探す（種別が指定されている場合のみ）
        if kind and children:
            if text == kind or text == f"## {kind}":
                return end_index

    # 子セクションが見つからなかった → 親の直後に挿入
    if parent_end_index is not None:
        if kind and children:
            print(
                f"WARNING: サブセクション '{kind}' が見つかりませんでした。"
                f"親セクション '{parent_text}' 直後に追記します。",
                file=sys.stderr,
            )
        return parent_end_index

    # 親も見つからなかった → 先頭にフォールバック
    print(
        f"WARNING: セクション '{parent_text}' が見つかりませんでした。ドキュメント先頭に追記します。",
        file=sys.stderr,
    )
    return 1


def build_entry(kind, media, text):
    now = datetime.now(JST).strftime("%Y/%m/%d %H:%M")
    label = kind if kind else media
    sep = "━━━━━━━━━━━━━━━━━━━━━━"
    lines = [
        sep,
        f"📌 {label}｜{now}",
        sep,
        text,
        "",
        "---",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="JAYBIRDS投稿ログをGoogleドキュメントの該当セクションに保存する"
    )
    parser.add_argument("--媒体", required=True, help="X / TikTok / OC")
    parser.add_argument("--種別", default="", help="サブセクション名（例：投票、ジェイどこ動画）")
    parser.add_argument("--本文", required=True, help="保存する投稿本文")
    args = parser.parse_args()

    creds = get_credentials()
    service = build("docs", "v1", credentials=creds)

    doc = service.documents().get(documentId=DOCUMENT_ID).execute()
    body_content = doc.get("body", {}).get("content", [])

    insert_index = find_insert_index(body_content, args.媒体, args.種別)
    entry = build_entry(args.種別, args.媒体, args.本文)

    service.documents().batchUpdate(
        documentId=DOCUMENT_ID,
        body={
            "requests": [
                {
                    "insertText": {
                        "location": {"index": insert_index},
                        "text": entry,
                    }
                }
            ]
        },
    ).execute()

    print("✅ 保存完了！")
    print(f"https://docs.google.com/document/d/{DOCUMENT_ID}/edit")


if __name__ == "__main__":
    main()
