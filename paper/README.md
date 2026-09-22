# 日本語論文

本検証の次版は[v8](v8/ICA2026_Japanese_revised_v8.pdf)です。ユーザー指定のv14_7を正本とし、Appendix F.5だけを外部MGH検証へ更新しました。v14_7を上書きしていません。本文主要数値とAppendix Eは維持しています。

[変更記録](v8/REVISION_V8_JA.md)、[数値検証と再現方法](../recalibration/external_vanstaden_2021/README.md)を参照してください。

## 組版

XeLaTeX、Latin Modern、Harano Ajiフォント、xeCJKを使用します。TeX Live環境で以下を3回実行します。

```bash
cd paper/v8
xelatex -interaction=nonstopmode -halt-on-error ICA2026_Japanese_revised_v8.tex
```

図は同梱の`figs/`を使用します。数値計算の再実行は不要です。Noto CJKが`../../tmp/fonts/`にある場合は原稿既存のフォールバック設定を使用します。
