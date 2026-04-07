# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

JAYBIRDS is a static fan support website for Chuang Jay (ジュアンジェイ), a contestant on PRODUCE 101 JAPAN 新世界. Hosted on GitHub Pages at `https://chuangjayfd.github.io/JAYBIRDS/`. All pages are standalone HTML files with inline CSS and JS — there is no build system, bundler, or package manager for the site itself.

## Site pages

| File | Purpose |
|---|---|
| `index.html` | Top page — news, voting links, tag guide |
| `vote.html` | Voting guide (Lemino / MNet+) |
| `guide.html` | General fan guide |
| `screenshot.html` | Random screenshot picker + X share |
| `simulator.html` | Vote-weight simulator (国民票 vs SEKAI票) |
| `schedule.html` | Event schedule |
| `tags.html` | Hashtag guide |
| `contribute.html` | How to contribute |
| `about.html` | About page |
| `analytics.html` | Internal analytics dashboard (noindex) |

## Screenshot pipeline

Screenshots are managed through an automated pipeline:

1. **Source:** Google Drive folder (`DRIVE_SCREENSHOTS_FOLDER_ID` secret) organized by episode sub-folders
2. **Sync:** `sync_screenshots.py` — downloads new images from Drive into `images/screenshots/ep{NN}/` and updates `screenshots_manifest.json`
3. **OGP generation:** `generate_ogp_pages.py` — reads `screenshots_manifest.json` and generates redirect pages in `screenshot/ep{NN}_{NNN}.html` (each page sets OGP tags for one image and instantly redirects to `screenshot.html`)
4. **Trigger:** GitHub Actions runs both scripts daily (02:00 UTC) via `sync-screenshots.yml`; OGP generation also fires on push to `images/screenshots/**` via `generate_ogp.yml`

To regenerate OGP pages locally after editing `screenshots_manifest.json`:
```bash
python generate_ogp_pages.py
```

To run the full sync locally (requires env vars):
```bash
GA4_SERVICE_ACCOUNT_KEY='...' DRIVE_SCREENSHOTS_FOLDER_ID='...' python sync_screenshots.py
python generate_ogp_pages.py
```

## Analytics pipeline

`fetch_analytics.js` fetches GA4 data (sessions, users, pageviews, daily trend, top countries, top pages, new vs returning) and writes `analytics_data.json`. This runs daily via `fetch-analytics.yml` using the `GA4_SERVICE_ACCOUNT_KEY` secret and hardcoded property ID `529950201`. The `analytics.html` page reads this JSON client-side using Chart.js.

To run locally:
```bash
npm install @google-analytics/data
GA4_SERVICE_ACCOUNT_KEY='...' GA4_PROPERTY_ID='529950201' node fetch_analytics.js
```

## Required GitHub Actions secrets

| Secret | Used by |
|---|---|
| `GA4_SERVICE_ACCOUNT_KEY` | Drive sync, GA4 fetch |
| `DRIVE_SCREENSHOTS_FOLDER_ID` | Drive sync |

## Design system

All pages share a consistent dark-mode design defined inline per-page:
- Background: `--navy: #080f20`
- Accent: `--gold: #c9a84c`
- Fonts: Cormorant Garamond (headings) + Noto Sans JP (body), loaded from Google Fonts
- The site is Japanese-primary with multilingual support (ja, en, zh-TW, ko) via `hreflang` alternates

When adding or modifying pages, follow the existing OGP/SEO meta tag pattern (og:*, twitter:*, JSON-LD, canonical, hreflang) present in every page's `<head>`.

## `cache-version.json`

Auto-updated every 6 hours by the `cache-refresh.yml` workflow. Contains a version timestamp and screenshot count. The `screenshot.html` page fetches this to bust its screenshot cache.

## デザインシステム補足（重要）

- カラーはCSS変数（`var(--navy)` 等）ではなく **hardcoded hex値** で書く（GitHub Pagesでのレンダリング不具合回避のため）
- `color-scheme: dark` と `background-color` を `body` に必ず明示する
- `.hero` の `border-bottom` は `.hero` に直接指定する（CSS stacking context問題）
- 紫・ピンク系の色は一切使わない

## 表記・ブランドルール

- アーティスト名：**ジュアンジェイ**（「チュアンジェイ」「Juan Jay」は不可）
- ブランド記号：💙🪶
- 多言語表記：Chuang Jay（英）/ 莊傑（中・繁体字）/ 장앙제이（韓）
- 番組名：PRODUCE 101 JAPAN 新世界 / 101SHINSEKAI

## ファンコミュニティ文脈

- 投票構造：国民票70%＋SEKAI票30%の正規化加重
- ターゲット：日本国内ファン中心（約83%）＋台湾・中国語圏
- チェンリッキーFDとの協力関係あり
- lurker（ROM専）多めのため、行動導線はシンプルに保つ

## 作業環境

- メイン作業：iPhone（GitHub Web）
- ローカル開発：Windows cmd + Claude Code
- ターミナル操作は可能だがシンプルな手順を優先する

## Lessons Learned

- CSS変数はGitHub Pagesで効かないことがある → hardcoded hex必須
- OGP画像は必ず `?v=N` のキャッシュバストをつける
- GitHub Actionsのシークレットは直接コードに書かない

## 短縮URL一覧（投稿時は必ずこれを使う）

### JAYBIRDSサイト
- トップ：https://x.gd/vja9F
- 投票ガイド：https://x.gd/63FPj
- ファンガイド：https://x.gd/4A61D
- ギャラリー：https://x.gd/RkLvF
- スクリーンショット：https://x.gd/FXiv3
- 投票シミュレーター：https://x.gd/w2a6z
- スミンパーティー：https://x.gd/O9hjUi
- ファンカムガイド：https://x.gd/23oAV
- TikTokガイド：https://x.gd/RWzPF
- タグイベガイド：https://x.gd/kO2i6

### 投票
- 公式投票：https://vote.produce101.jp
- Lemino（投票方法詳細）：https://x.gd/63FPj
- ※Leminoアプリへの直リンク不可。アプリから投票を促す一言を添える

### ワンタッチポスト
- 通常（JAY羽ばたく+日プ）：https://x.gd/537RC
- 通常（JAY羽ばたくのみ）：https://x.gd/QkdFa
- ジェイどこ：https://x.gd/i18ye
- スミンパーティー：https://x.gd/XqCId
