# 採用結果の検証表

ここに置くのは、すべての中間配列をGitへ保存するためではなく、再計算結果を確認するための**コンパクトな正本テーブル**です。

完全なパラメータのみ変更の計算は `02_adopted_analysis/` と番号付きGitHub Actionsワークフローから再現できます。大きな配列や完全な図一式は、改訂ごとに複製せず再生成してください。

正本となる検証項目:

- `01_baseline_summary.csv` — 最終共通平均較正における5戦略の月次基準結果
- `02_mvs_fixed_gamma_summary.csv` — 図6の固定 `gamma0=2.5` MVSケース
- `03_strict_vs_clip_summary.csv` — 再較正後の図4の方策比較
- `04_numerical_checks.md` — モーメント整合性と状態格子切断の診断

再計算結果がこれらの値と実質的に一致しない場合、差の原因を説明できるまで、その図を論文に使用しないでください。

CSV数値は英語版 `dc-glidepath-ica2026-en` main commit `4f2535f343c05b6d2e6cef01782fde3b50b5ca0a` と同一です。
