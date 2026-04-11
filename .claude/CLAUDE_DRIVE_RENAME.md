# Google Drive リネーム作業指示書

## 概要

JAYBIRDSファンサイト運営用のGoogle Driveフォルダ・ファイル名を、以下の命名規則に従って一括リネームする。
対象フォルダID: `1f-JTQOWUF3rXghBPuHQOaQnT0p5gk_t1`

---

## フォルダ構成ルール

### エピソードフォルダの構成

```
epNN_MMDD_タイトル/
  ├── src/
  │   ├── shared/       ← FD・個人どちらでも使える素材（動画＋スクショ）
  │   └── personal/     ← 個人アカウント専用素材（動画のみ）
  └── output/
      ├── FD/           ← JAYBIRDSアカウント投稿用完成品
      └── personal/     ← 個人アカウント投稿用完成品
```

### シーンフォルダ（src/shared・src/personal の中）

```
src/shared/
  └── sc01_シーン概要/
      ├── ep01_sc01_001.png
      ├── ep01_sc01_002.png
      └── ep01_sc01_raw.mp4

src/personal/
  └── sc02_シーン概要/
      └── ep01_sc02_raw.mp4
```

---

## 命名規則

### フォルダ名

| 種別 | 形式 | 例 |
|------|------|----|
| エピソード | `epNN_MMDD_タイトル` | `ep03_0409_新世界ステージ` |
| シーン | `scNN_シーン概要` | `sc01_entrance` |
| 管理フォルダ | `NN_name` | `00_ready_to_post` |

- `epNN`: エピソード番号2桁（ep01, ep02, ep03...）
- `scNN`: エピソード内のジェイ登場順の番号2桁（sc01, sc02...）
- シーン概要: 英語またはローマ字、アンダースコア区切り、スペース禁止

### ファイル名

| 種別 | 形式 | 例 |
|------|------|----|
| スクショ | `epNN_scNN_NNN.png` | `ep01_sc01_001.png` |
| 動画（未編集） | `epNN_scNN_raw.mp4` | `ep01_sc01_raw.mp4` |
| 動画（編集済み） | `epNN_scNN_vN.mp4` | `ep01_sc01_v1.mp4` |
| 完成品（FD用） | `epNN_scNN_FD_vN.mp4` | `ep01_sc01_FD_v1.mp4` |
| 完成品（個人用） | `epNN_scNN_personal_vN.mp4` | `ep01_sc01_personal_v1.mp4` |

- スクショの連番は3桁（001, 002, 003...）
- 拡張子はすべて小文字（.png / .jpg / .mp4 / .mov）

### 禁止事項

- スペース（半角・全角）→ `_` に置換
- コロン `:` チルダ `〜` 括弧 `（）()` → 削除またはアンダースコアに置換
- 拡張子の大文字（`.PNG` `.MOV` `.JPG`）→ 小文字に統一
- 重複ファイル名 → 連番（_002, _003）で区別

---

## リネームマッピング（具体的な変更内容）

**処理順序: 親フォルダから順に処理すること。**

### 【A】トップレベル管理フォルダ（01_動画 配下）

```
現在名                          → 変更後
────────────────────────────────────────
00_投稿用                       → 00_ready_to_post
01_未分類                       → 01_unsorted
02_全身・スタイル               → 02_full_body
03_遠景・ミッケ用               → 03_wide_shots
04_顔・ビジュアル               → 04_face_visual
05_ダンス                       → 05_dance
06_ストーリー系                 → 06_stories
07_公式動画別分量まとめ         → 07_official_by_episode
08_使用済                       → 08_archived
09_お気に入り                   → 09_favorites
```

### 【B】07_official_by_episode 配下

```
現在名                          → 変更後
────────────────────────────────────────
01_0307_101DAYS                 → ep00_0307_101days_event
0326 第1話                      → ep01_0326_101days_first
0402 第2話                      → ep02_0402_re_eval_stage
02_BEHIND                       → 02_behind
```

各エピソードフォルダ内に以下を新規作成:
```
src/shared/
src/personal/
output/FD/
output/personal/
```

### 【C】ep01_0326 配下のシーンフォルダ

既存のシーンフォルダを `src/shared/` 配下に移動しつつリネーム。
ジェイ登場順にsc番号を振る。

```
現在名                                  → 変更後（src/shared/ 配下）
────────────────────────────────────────────────────────
0:00:33〜39 プロフィール                → sc01_profile
0:53:59〜0:55:40 入場、コメント         → sc02_entrance
0:56:29〜0:56:33 着席コメント           → sc03_seated
1:04:29〜31 101PASS反応                 → sc04_101pass_reaction
1:05:13〜14 レベル分け前緊張           → sc05_levelsort_nervous
1:08:28〜29 FRESH-MEN反応               → sc06_freshmen_reaction
1:31:48〜49 博多美男反応                → sc07_hakata_reaction
1:49:37〜Atlantic Boys反応              → sc08_atlantic_boys
2:08:54〜　慶應Guys                     → sc09_keio_guys
2:27:10〜 Angels反応                    → sc10_angels_reaction
```

### 【D】ep02_0402 配下のシーンフォルダ

既存のシーンフォルダを `src/shared/` 配下に移動しつつリネーム。

```
現在名                          → 変更後（src/shared/ 配下）
────────────────────────────────────────
1．我的少年時代                 → sc01_wode_shaonian
2．ゆら達への反応コメント       → sc02_yura_reaction
3．Cクラス練習風景              → sc03_classC_practice
4．Amazing！                    → sc04_amazing
5．再評価後ステージ練           → sc05_re_eval_practice
6．新世界衣装合わせ             → sc06_shinsekai_costume
7．新世界ステージ後             → sc07_shinsekai_after
```

### 【E】各種管理フォルダ配下

```
05_dance 配下
  02_切り抜き候補               → 02_clip_candidates
  01_全体                       → 01_full_performance

04_face_visual 配下
  04_公式応援素材               → 04_official_material
  03_リアクション               → 03_reactions
  02_表情・笑顔                 → 02_expressions
  01_顔アップ                   → 01_face_closeup

03_wide_shots 配下
  04_多分ジュアンジェイ         → 04_probably_jay
  03_シルエット特定系           → 03_silhouette_id
  02_見切れ・端にいる           → 02_partially_visible
  01_集合・遠景                 → 01_group_wide

02_full_body 配下
  04_シルエット                 → 04_silhouette
  03_立ち絵                     → 03_standing
  02_歩き                       → 02_walking
  01_集合写真                   → 01_group_photo

06_stories 配下
  03_ケミ素材                   → 03_chemistry
  02_スペック紹介               → 02_profile_specs
  01_外国人・台湾関係           → 01_international_taiwan

01_unsorted 配下
  過去作成の短編動画            → past_shorts
```

---

## ファイルリネーム方針

**フォルダリネーム完了後に実行すること。**

### スクショ（PNG/JPG）

`IMG_XXXX.PNG` 形式のファイルは親フォルダのep・sc情報を使って連番リネーム。

処理ロジック:
1. 親フォルダ名から `epNN` `scNN` を取得
2. フォルダ内ファイルを作成日時順にソート
3. `epNN_scNN_NNN.png` 形式で連番付与

例（ep01/src/shared/sc02_entrance/ 内）:
```
IMG_0104.PNG → ep01_sc02_001.png
IMG_0105.PNG → ep01_sc02_002.png
IMG_0109.PNG → ep01_sc02_003.png
```

### 動画ファイル

内容がわかるものは意味を保持しつつ形式統一:
```
台南から来ました.mp4            → ep01_sc02_raw.mp4
我的少年時代フル.mp4            → ep02_sc01_raw.mp4
我的少年時代TikTokサイズ.mp4    → ep02_sc01_v1.mp4
Cクラス練習風景.mp4             → ep02_sc03_raw.mp4
amazing!.mp4                    → ep02_sc04_raw.mp4
新世界衣装合わせ.mp4            → ep02_sc06_raw.mp4
再評価後練習着ステージ錬.mp4   → ep02_sc05_raw.mp4
```

UUID形式ファイル:
```
copy_64FE41E2-....MOV           → unsorted_raw_001.mov
copy_C797535E-....MOV           → unsorted_raw_002.mov
```

拡張子の大文字を小文字に統一（全ファイル対象）:
```
.PNG → .png / .JPG → .jpg / .MOV → .mov / .MP4 → .mp4
```

---

## 実装（Apps Script）

```javascript
// メイン実行関数
function renameAll() {
  renameFolders();  // Step1: フォルダのリネーム
  createEpisodeFolders(); // Step2: src/output フォルダを新規作成
  renameFiles();    // Step3: ファイルのリネーム
  Logger.log('完了');
}

// フォルダリネーム
function renameFolders() {
  const ROOT_ID = '1f-JTQOWUF3rXghBPuHQOaQnT0p5gk_t1';
  const map = getFolderRenameMap();
  for (const [oldName, newName] of Object.entries(map)) {
    const results = searchByName(ROOT_ID, oldName, 'folder');
    results.forEach(f => {
      f.setName(newName);
      Logger.log(`[FOLDER] ${oldName} → ${newName}`);
    });
  }
}

// epNN フォルダ内に src/shared, src/personal, output/FD, output/personal を作成
function createEpisodeFolders() {
  const ROOT_ID = '1f-JTQOWUF3rXghBPuHQOaQnT0p5gk_t1';
  const root = DriveApp.getFolderById(ROOT_ID);
  const allFolders = root.getFolders();
  while (allFolders.hasNext()) {
    const f = allFolders.next();
    if (/^ep\d{2}_/.test(f.getName())) {
      const src = f.createFolder('src');
      src.createFolder('shared');
      src.createFolder('personal');
      const out = f.createFolder('output');
      out.createFolder('FD');
      out.createFolder('personal');
      Logger.log(`[CREATE] ${f.getName()} に src/output を作成`);
    }
  }
}

// ファイルリネーム（IMG_XXXX系を連番化）
function renameFiles() {
  const ROOT_ID = '1f-JTQOWUF3rXghBPuHQOaQnT0p5gk_t1';
  const root = DriveApp.getFolderById(ROOT_ID);
  traverseAndRename(root);
}

// 再帰的にフォルダを走査
function traverseAndRename(folder) {
  const folderName = folder.getName();
  const epMatch = folderName.match(/ep(\d{2})/);
  const scMatch = folderName.match(/sc(\d{2})/);

  if (epMatch && scMatch) {
    const ep = epMatch[1];
    const sc = scMatch[1];
    const files = folder.getFiles();
    const fileList = [];
    while (files.hasNext()) fileList.push(files.next());

    // 作成日時順にソート
    fileList.sort((a, b) => a.getDateCreated() - b.getDateCreated());

    let counter = 1;
    fileList.forEach(file => {
      const oldName = file.getName();
      const ext = oldName.split('.').pop().toLowerCase();
      let newName;
      if (['png', 'jpg', 'jpeg'].includes(ext)) {
        newName = `ep${ep}_sc${sc}_${String(counter).padStart(3, '0')}.${ext}`;
        counter++;
      } else if (['mp4', 'mov'].includes(ext)) {
        newName = `ep${ep}_sc${sc}_raw.${ext}`;
      } else {
        return;
      }
      file.setName(newName);
      Logger.log(`[FILE] ${oldName} → ${newName}`);
    });
  }

  // サブフォルダを再帰処理
  const subFolders = folder.getFolders();
  while (subFolders.hasNext()) traverseAndRename(subFolders.next());
}
```

---

## 実行手順

1. [Apps Script](https://script.google.com/create) を開く
2. Drive APIをサービスに追加（左メニュー「サービス」→「Drive API」）
3. 上記コードを貼り付け
4. まず `renameFolders()` だけ単体実行 → ログで確認
5. 問題なければ `createEpisodeFolders()` を実行
6. 最後に `renameFiles()` を実行
7. 完了後、`listFolderTree()` で新しいツリーを出力して確認

---

## 注意事項

- 同名フォルダが複数ある場合はログに件数が出る。意図しない変更がないか確認すること
- ファイルリネームは不可逆。不安な場合は実行前にDriveのフォルダを手元にメモしておく
- 既存シーンフォルダを `src/shared/` 配下に移動する処理は、スクリプト実行後に手動で行うか、`DriveApp.getFolderById().addFolder()` / `removeFolder()` を使って自動化する
