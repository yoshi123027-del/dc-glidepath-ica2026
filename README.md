# ICA2026 DC運用論文・日本語版

**最新版はv11（40ページ）です。** v5の内容・数値・図を基準に、本文の主張を絞り、理論導出・背景・MVS等をAppendixへ配置しました。原計算の誤りや精度上の制約は明示しています。

- [最新版PDF](paper/v11/ICA2026_Japanese_revised_v11.pdf)
- [TeX・原図](paper/v11/) / [変更内容とレビュワー対応](paper/v11/REVISION_V11_JA.md)
- [v9・39ページ保存版](archive/v9/paper/v9/ICA2026_Japanese_revised_v9.pdf)

**比較を主たる貢献、クリップ評価をその分析、三層運用を実務上の含意**として、要旨・序論・本文・結論を統一しました。新たな数値最適化・妥当性検証は行っていません。

以前お渡しした[v10・42ページ稿](archive/v10/paper/ICA2026_Japanese_v5_restructured_v10_current.pdf)も保存しています。

## 資料の入口

| 目的 | 場所 |
|---|---|
| 最新原稿と組版方法 | [paper/README.md](paper/README.md) |
| v5の原稿・原図・元の計算 | [archive/legacy_v5/](archive/legacy_v5/) |
| 訂正・再較正の方策と独立評価 | [results/recalibration_v8/fine/](results/recalibration_v8/fine/) |
| 再較正コードと条件 | [recalibration/README.md](recalibration/README.md) |
| 不採用データ、探索計算、旧版 | [archive/README.md](archive/README.md) |
| ファイルの役割 | [CODEBOOK_JA.md](CODEBOOK_JA.md) |
| 現在のファイルハッシュ | [manifest_v11.json](manifest_v11.json) |

v5の151点格子の数値は原計算として保存しています。上端切詰めのない月次過程の精密な推定値とは区別してください。dTCMVの旧クリップは係数の符号訂正前の記録です。再較正した比較値はv11付録Fで確認できます。

旧ファイルは削除せず分類して保存しています。[移動一覧](archive/inventory.csv)に旧パス・新パス・SHA-256を記録しました。コード利用時は論文と使用コミットを引用してください。ライセンスは[MIT](LICENSE)です。
