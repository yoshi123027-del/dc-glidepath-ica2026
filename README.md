# ICA2026 DC運用論文・日本語版

**最新版はv14_7です。** v14_6の文章・主要数値を維持し、同一保存方策をMGH前進計算と独立100万経路Euler–Monte Carloに通した終端分布・平均グライドパスの検証をAppendix E.3へ追加しました。

- [最新版PDF](paper/v14_7/ICA2026_Japanese_revised_v14_7.pdf)
- [TeX・図](paper/v14_7/) / [変更記録](paper/v14_7/REVISION_V14_7_JA.md)
- [評価器比較の定義・実行方法](recalibration/EVALUATOR_COMPARISON.md)
- [従来v11](paper/v11/ICA2026_Japanese_revised_v11.pdf)も維持しています。

方策・係数・較正目標84.78は変更していません。MGHは離散確率質量伝播、MCは上端切詰めのない100万Euler経路です。両評価器に同じ方策を入力し、終端CDFと状態分布で加重した平均グライドパスを比較します。この検証は連続時間解の厳密性を証明するものではありません。

## 資料の入口

| 目的 | 場所 |
|---|---|
| 最新原稿と組版方法 | [paper/README.md](paper/README.md) |
| v5の原稿・原図・元の計算 | [archive/legacy_v5/](archive/legacy_v5/) |
| 訂正・再較正の方策と独立評価 | [results/recalibration_v8/fine/](results/recalibration_v8/fine/) |
| 再較正コードと条件 | [recalibration/README.md](recalibration/README.md) |
| 不採用データ、探索計算、旧版 | [archive/README.md](archive/README.md) |
| ファイルの役割 | [CODEBOOK_JA.md](CODEBOOK_JA.md) |
| v11時点のファイルハッシュ | [manifest_v11.json](manifest_v11.json) |

v5の151点格子の数値は原計算として保存しています。上端切詰めのない月次過程の精密な推定値とは区別してください。dTCMVの旧クリップは係数の符号訂正前の記録です。再較正した比較値は最新版の本文表5、評価器比較は付録E.3で確認できます。

旧ファイルは削除せず分類して保存しています。[移動一覧](archive/inventory.csv)に旧パス・新パス・SHA-256を記録しました。コード利用時は論文と使用コミットを引用してください。ライセンスは[MIT](LICENSE)です。
