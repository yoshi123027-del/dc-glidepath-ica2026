# 日本語論文

最新版は[v14_7](v14_7/ICA2026_Japanese_revised_v14_7.pdf)です。v14_6を正本とし、Appendix E.3に評価器比較を追加しました。従来v11は保存しています。[変更記録](v14_7/REVISION_V14_7_JA.md)と[検証の生成元](../recalibration/EVALUATOR_COMPARISON.md)を併せて参照してください。

## 組版

XeLaTeX、Latin Modern、Harano Ajiフォントを使用します。TeX Live環境で以下を3回実行します。

```text
cd paper/v14_7
xelatex -interaction=nonstopmode -halt-on-error ICA2026_Japanese_revised_v14_7.tex
```

図は同梱の `figs/` を使用します。数値計算を再実行する必要はありません。今朝のv9は[保存版](../archive/v9/paper/v9/ICA2026_Japanese_revised_v9.pdf)、v5の原稿は[原資料](../archive/legacy_v5/paper/)に保存しています。
