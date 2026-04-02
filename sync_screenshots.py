"""
sync_screenshots.py
Google Drive の各話フォルダから画像をダウンロードし
screenshots_manifest.json を更新する。
認証は GA4_SERVICE_ACCOUNT_KEY（Drive API も同一プロジェクトで有効化すること）。
親フォルダ ID は DRIVE_SCREENSHOTS_FOLDER_ID で指定。
"""

import os, io, json, re
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

KEY_JSON   = os.environ['GA4_SERVICE_ACCOUNT_KEY']
FOLDER_ID  = os.environ['DRIVE_SCREENSHOTS_FOLDER_ID']
BASE_URL   = 'https://chuangjayfd.github.io/JAYBIRDS'

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
creds  = service_account.Credentials.from_service_account_info(
    json.loads(KEY_JSON), scopes=SCOPES
)
drive = build('drive', 'v3', credentials=creds, cache_discovery=False)


def list_items(parent_id, mime_filter=None):
    """指定フォルダ直下のファイル／フォルダを列挙する"""
    q = f"'{parent_id}' in parents and trashed=false"
    if mime_filter:
        q += f" and mimeType='{mime_filter}'"
    result = drive.files().list(
        q=q,
        fields='files(id, name, mimeType)',
        orderBy='name',
        pageSize=1000
    ).execute()
    return result.get('files', [])


def download_file(file_id, dest_path):
    request = drive.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    dl  = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = dl.next_chunk()
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'wb') as f:
        f.write(buf.getvalue())


def episode_number(folder_name):
    """フォルダ名 '#1', '第1話', 'ep01' などから話数を取り出す"""
    m = re.search(r'\d+', folder_name)
    return int(m.group()) if m else None


def ext_from(filename, mime):
    """拡張子を判定する"""
    if filename:
        for e in ('.jpg', '.jpeg', '.png', '.webp', '.gif'):
            if filename.lower().endswith(e):
                return e.lstrip('.')
    if 'jpeg' in mime: return 'jpg'
    if 'png'  in mime: return 'png'
    if 'webp' in mime: return 'webp'
    return 'jpg'


# ── 既存マニフェストを読み込む（差分ダウンロード用）──────────────────
manifest_path = 'screenshots_manifest.json'
existing = {}
if os.path.exists(manifest_path):
    with open(manifest_path) as f:
        old = json.load(f)
    for ep in old.get('episodes', []):
        existing[ep['number']] = set(ep.get('images', []))

# ── 各話フォルダをスキャン ──────────────────────────────────────────
episode_folders = list_items(
    FOLDER_ID,
    mime_filter='application/vnd.google-apps.folder'
)
print(f"Found {len(episode_folders)} episode folders in Drive")

MIME_IMAGE = ('image/jpeg', 'image/png', 'image/webp', 'image/gif')
episodes = []

for folder in episode_folders:
    ep_num = episode_number(folder['name'])
    if ep_num is None:
        print(f"  Skipping folder (no number): {folder['name']}")
        continue

    ep_key    = f"ep{ep_num:02d}"
    dir_path  = f"images/screenshots/{ep_key}"
    os.makedirs(dir_path, exist_ok=True)

    raw_files = list_items(folder['id'])
    img_files = [f for f in raw_files if f['mimeType'] in MIME_IMAGE]
    img_files.sort(key=lambda x: x['name'])

    print(f"  Episode #{ep_num}: {len(img_files)} images")
    known = existing.get(ep_num, set())
    images = []

    for idx, img in enumerate(img_files, start=1):
        ext      = ext_from(img['name'], img['mimeType'])
        filename = f"{idx:03d}.{ext}"
        rel_path = f"{ep_key}/{filename}"
        dest     = f"images/screenshots/{rel_path}"

        if not os.path.exists(dest):
            print(f"    Downloading {rel_path} ...")
            download_file(img['id'], dest)
        images.append(rel_path)

    episodes.append({
        'number': ep_num,
        'label':  f'#{ep_num}',
        'count':  len(images),
        'images': images,
    })

episodes.sort(key=lambda x: x['number'])

manifest = {
    'updated':  datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    'episodes': episodes,
    'total':    sum(e['count'] for e in episodes),
}

with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"Manifest saved: {manifest['total']} images / {len(episodes)} episodes")
