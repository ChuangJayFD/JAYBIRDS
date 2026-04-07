JAYBIRDSサイトのHTMLページがデザインシステムと品質基準に準拠しているか確認する。
対象ファイル: $ARGUMENTS（未指定の場合はルートの全HTMLファイル）

## チェック項目

### デザイン違反
- CSS変数（var(--）の使用 → hardcoded hexに修正
- 紫・ピンク系の色（#8B5CF6、#EC4899等）→ gold/navyに修正
- color-scheme: dark の欠如
- background-colorのhardcoded hex指定なし

### OGP・SEO漏れ
- og:title / og:description / og:image / og:url のうち欠けているもの
- twitter:card メタタグの欠如
- JSON-LD構造化データの欠如
- canonical / hreflang（ja/en/zh-TW/ko）の欠如
- OGP画像URLに ?v= キャッシュバストがない

### トラッキング
- GA4（G-EXHV880LX0）未設置

### フォント
- Cormorant Garamond / Noto Sans JP 未使用

## 出力形式
問題があれば「ファイル名：問題点：修正案」の形式で列挙して、
そのまま修正してよいか確認する。
問題なければ「✅ すべてのチェック項目をパスしました」と報告する。
