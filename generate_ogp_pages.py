"""
generate_ogp_pages.py
screenshots_manifest.json を読んでOGPページを生成する。
出力先: screenshot/ep01_001.html, screenshot/ep01_002.html ...
"""

import os, json

BASE_URL   = 'https://chuangjayfd.github.io/JAYBIRDS'
OUTPUT_DIR = 'screenshot'
MAIN_URL   = f'{BASE_URL}/screenshot.html'

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open('screenshots_manifest.json', encoding='utf-8') as f:
    manifest = json.load(f)

generated = 0

for ep in manifest.get('episodes', []):
    ep_num   = ep['number']
    ep_key   = f"ep{ep_num:02d}"
    ep_label = ep['label']  # "#1" など

    for idx, rel_path in enumerate(ep['images'], start=1):
        img_url  = f"{BASE_URL}/images/screenshots/{rel_path}"
        page_id  = f"{ep_key}_{idx:03d}"
        page_url = f"{BASE_URL}/screenshot/{page_id}.html"
        title    = f"Chuang Jay {ep_label} No.{idx:03d} | JAYBIRDS"
        desc     = f"ジュアンジェイ {ep_label} のスクショをシェアしよう！ #ジュアンジェイ #JAYどこ #FINDJAY"

        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title"        content="{title}">
<meta property="og:description"  content="{desc}">
<meta property="og:image"        content="{img_url}">
<meta property="og:image:width"  content="1280">
<meta property="og:image:height" content="720">
<meta property="og:url"          content="{page_url}">
<meta property="og:type"         content="website">
<meta property="og:site_name"    content="CHUANG JAY FD | JAYBIRDS">
<meta name="twitter:card"        content="summary_large_image">
<meta name="twitter:site"        content="@CHUANGJAY_FD">
<meta name="twitter:title"       content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image"       content="{img_url}">
<meta http-equiv="refresh" content="0;url={MAIN_URL}">
</head>
<body></body>
</html>
"""
        out_path = os.path.join(OUTPUT_DIR, f"{page_id}.html")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        generated += 1

print(f"Generated {generated} OGP pages")
