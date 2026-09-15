# 日本語論文

最新版は[v11](v11/ICA2026_Japanese_revised_v11.pdf)です。[変更記録](v11/REVISION_V11_JA.md)と[図の出典](v11/FIGURES_JA.md)を併せて参照してください。

## 組版

XeLaTeX、Latin Modern、Harano Ajiフォントを使用します。TeX Live環境で以下を3回実行します。

```text
cd paper/v11
xelatex -interaction=nonstopmode -halt-on-error ICA2026_Japanese_revised_v11.tex
```

図は同梱の `figs/` を使用します。数値計算を再実行する必要はありません。今朝のv9は[保存版](../archive/v9/paper/v9/ICA2026_Japanese_revised_v9.pdf)、v5の原稿は[原資料](../archive/legacy_v5/paper/)に保存しています。
