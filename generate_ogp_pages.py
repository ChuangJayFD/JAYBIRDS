#!/usr/bin/env python3
“””
generate_ogp_pages.py
JAYBIRDS - スクショ共有用OGPページ自動生成スクリプト

使い方:
python generate_ogp_pages.py

実行するとリポジトリ直下の screenshot/ フォルダに
1.html 〜 30.html が生成されます。

画像ファイルは images/screenshots/jay_01.jpg 〜 jay_30.jpg に
置いてあることを前提としています。ファイル名を変えたい場合は
IMAGE_NAMES リストを編集してください。
“””

import os

# ===== 設定 =====

TOTAL = 30
BASE_URL = “https://chuangjayfd.github.io/JAYBIRDS”
OUTPUT_DIR = “screenshot”  # リポジトリ直下に作成される
SITE_NAME = “JAYBIRDS Fan Support | Chuang Jay”
TWITTER_ACCOUNT = “@JAYBIRDS_FD”

# 画像ファイル名リスト（実際のファイル名に合わせて変更してください）

IMAGE_NAMES = [f”sshot_{str(i).zfill(2)}.png” for i in range(1, TOTAL + 1)]

# ===== OGP説明文（多言語） =====

DESCRIPTIONS = {
“ja”: “ジュアンジェイのスクショをシェアしよう！ #ジュアンジェイ #JAYどこ #FINDJAY #PRODUCE101JAPAN新世界”,
“en”: “Share Chuang Jay’s screenshot! #ChuangJay #JAYどこ #FINDJAY #PRODUCE101JAPAN新世界”,
“zh”: “分享莊傑的截圖！ #莊傑 #JAYどこ #FINDJAY #PRODUCE101JAPAN新世界”,
“ko”: “Chuang Jay의 스크린샷을 공유하세요! #ChuangJay #JAYどこ #FINDJAY #PRODUCE101JAPAN新世界”,
}

DEFAULT_DESC = DESCRIPTIONS[“ja”]

def generate_page(index: int) -> str:
“”“1枚分のOGPページHTMLを生成”””
img_filename = IMAGE_NAMES[index - 1]
img_url = f”{BASE_URL}/images/screenshots/{img_filename}”
page_url = f”{BASE_URL}/screenshot/{index}.html”
main_page_url = f”{BASE_URL}/screenshot.html”

```
title = f"Chuang Jay No.{str(index).zfill(2)} | JAYBIRDS"

return f"""<!DOCTYPE html>
```

<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>

  <!-- OGP -->

  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{DEFAULT_DESC}" />
  <meta property="og:image" content="{img_url}" />
  <meta property="og:image:width" content="1280" />
  <meta property="og:image:height" content="720" />
  <meta property="og:url" content="{page_url}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{SITE_NAME}" />

  <!-- Twitter Card -->

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="{TWITTER_ACCOUNT}" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{DEFAULT_DESC}" />
  <meta name="twitter:image" content="{img_url}" />

  <!-- 正規URL -->

  <link rel="canonical" href="{page_url}" />

  <!-- 3秒後にメインページへリダイレクト -->

  <meta http-equiv="refresh" content="3;url={main_page_url}" />

  <style>
    :root {{
      --navy: #0a1628;
      --gold: #c9a84c;
      --white: #f0ead8;
    }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--navy);
      color: var(--white);
      font-family: 'Noto Sans JP', sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 24px;
      text-align: center;
    }}
    .label {{
      font-size: 12px;
      letter-spacing: 0.3em;
      color: var(--gold);
      margin-bottom: 16px;
      text-transform: uppercase;
    }}
    .img-wrap {{
      width: 100%;
      max-width: 560px;
      aspect-ratio: 16/9;
      overflow: hidden;
      border: 1px solid rgba(201,168,76,0.3);
      border-radius: 4px;
      margin-bottom: 20px;
    }}
    img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .redirect-msg {{
      font-size: 13px;
      color: rgba(240,234,216,0.5);
      margin-bottom: 16px;
    }}
    a.btn {{
      display: inline-block;
      padding: 12px 28px;
      border: 1px solid var(--gold);
      color: var(--gold);
      text-decoration: none;
      font-size: 13px;
      letter-spacing: 0.15em;
      border-radius: 2px;
      transition: background 0.2s;
    }}
    a.btn:hover {{ background: rgba(201,168,76,0.15); }}
  </style>

</head>
<body>
  <div class="label">JAYBIRDS Fan Support</div>
  <div class="img-wrap">
    <img src="{img_url}" alt="Chuang Jay screenshot No.{str(index).zfill(2)}" />
  </div>
  <p class="redirect-msg">3秒後にメインページへ移動します...</p>
  <a class="btn" href="{main_page_url}">→ もっとシェアする</a>
</body>
</html>
"""

def main():
os.makedirs(OUTPUT_DIR, exist_ok=True)

for i in range(1, TOTAL + 1):
    filepath = os.path.join(OUTPUT_DIR, f"{i}.html")
    html = generate_page(i)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 生成: {filepath}")

print(f"\n🎉 完了！{TOTAL}枚のOGPページを {OUTPUT_DIR}/ に生成しました。")
print(f"   GitHubにpushすれば {BASE_URL}/screenshot/1.html 〜 {TOTAL}.html で公開されます。")

if **name** == “**main**”:
main()
