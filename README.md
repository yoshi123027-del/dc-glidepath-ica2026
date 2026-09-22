# ICA2026 DC運用論文・日本語版

**本検証の最新版はv8です。** 指定されたv14_7を正本とし、Appendix F.5をMGH後退・前進による外部ベンチマーク検証へ更新しました。版名v8は今回の指定に従います。

- [v8 PDF](paper/v8/ICA2026_Japanese_revised_v8.pdf) / [TeX・図](paper/v8/)
- [外部ベンチマークの仕様・実行方法](recalibration/external_vanstaden_2021/README.md)
- [全比較・収束・境界診断データ](results/validation/van_staden_2021/)
- [v14_7](paper/v14_7/) / [評価器比較の定義・実行方法](recalibration/EVALUATOR_COMPARISON.md)

DC保存方策・係数・較正目標84.78・本文主要数値・Appendix Eは維持しています。検証を①同じ有限モデル内の後退・前進整合性、②同一方策のMGH対独立100万Euler経路、③外部問題へのMGH適用、の三層に区別します。第三層は閉形式からの表の再計算だけではありません。ただしdTCMVは原論文の掲載式と均衡導出の不整合および残差があり、完全再現とはしていません。いずれも連続時間最適性の証明ではありません。

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
