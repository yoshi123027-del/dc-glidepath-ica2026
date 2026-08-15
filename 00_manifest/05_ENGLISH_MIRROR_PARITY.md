# 英語版とのミラー対応

## 目的

この日本語版リポジトリは、英語版の分析内容を日本語で検算するための照合用ミラーです。

対応する英語版:

- repository: `yoshi123027-del/dc-glidepath-ica2026-en`
- source main commit: `4f2535f343c05b6d2e6cef01782fde3b50b5ca0a`

## 同一に保つもの

以下は英語版と同一です。

- 元手法の数値計算アルゴリズム
- 最終較正パラメータ
- 共通平均 `70.34483966999646`
- 基準ケースの5戦略要約
- MVS `gamma0=2.5` の要約
- strict vs clip の基準要約
- 図1〜図6の計算定義
- 感応度分析・数値診断の前提

## 日本語版でのみ変えるもの

- README
- ステータス・再現性説明
- コードブックの説明文
- 図中の自然言語ラベル
- GitHub Actions の表示名・説明

数値・式・コードロジックを「日本語版向け」に独自変更することは禁止します。

## 照合方法

1. 英語版と日本語版の `02_adopted_analysis/02_final_parameters/final_parameters.json` を比較する。
2. `03_adopted_results/01_baseline_summary.csv`、`02_mvs_fixed_gamma_summary.csv`、`03_strict_vs_clip_summary.csv` が一致することを確認する。
3. 日本語版の再現ワークフローを実行し、同じ基準値が再現されることを確認する。
4. 数値が一致した状態で、日本語の本文・図説明を使って英語版の論理展開を確認する。

## 例外

`90_rejected/` は各リポジトリ固有の履歴を監査用に残す場所です。現行採用分析の同一性判定には使用しません。
