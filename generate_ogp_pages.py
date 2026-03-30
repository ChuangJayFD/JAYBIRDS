import os

TOTAL = 30
BASE_URL = "https://chuangjayfd.github.io/JAYBIRDS"
OUTPUT_DIR = "screenshot"
SITE_NAME = "JAYBIRDS Fan Support | Chuang Jay"
TWITTER_ACCOUNT = "@JAYBIRDS_FD"
IMAGE_NAMES = [f"sshot_{str(i).zfill(2)}.png" for i in range(1, TOTAL + 1)]
DEFAULT_DESC = "share Chuang Jay screenshots! #JAYdoko #FINDJAY"

def generate_page(index):
    img = IMAGE_NAMES[index - 1]
    img_url = f"{BASE_URL}/images/screenshots/{img}"
    page_url = f"{BASE_URL}/screenshot/{index}.html"
    main_url = f"{BASE_URL}/screenshot.html"
    title = f"Chuang Jay No.{str(index).zfill(2)} | JAYBIRDS"
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta property="og:title" content="{title}">
<meta property="og:image" content="{img_url}">
<meta property="og:url" content="{main_url}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{img_url}">
<meta http-equiv="refresh" content="0;url={main_url}">
</head>
<body></body>
</html>
"""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for i in range(1, TOTAL + 1):
        path = os.path.join(OUTPUT_DIR, f"{i}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(generate_page(i))

if __name__ == "__main__":
    main()
