# コード・データの案内

| パス | 役割 |
|---|---|
| `paper/v11/` | v5を基準に再構成した保存版、TeX、図、変更記録 |
| `archive/legacy_v5/paper/` | 添付v5原PDF・TeX |
| `archive/legacy_v5/results/` | 原計算・探索的な数値と診断 |
| `archive/legacy_v5/scripts/` | 旧計算のソルバー・図表生成 |
| `recalibration/` | 既存の再最適化・共通期待終価較正と独立評価コード |
| `results/recalibration_v8/fine/` | 訂正・再較正の最終データ。現行本文表5の出典 |
| `archive/v8/base/` | 最終採用しなかった粗格子データ |
| `archive/v9/` | v9の原稿、追加分析、図・コード |

[最新版の組版](paper/README.md)、[再較正](recalibration/README.md)、[保存資料](archive/README.md)を参照してください。

`archive/v10/` は以前お渡しした42ページ稿と対応ソースです。

## 追加検証

| パス | 役割 |
|---|---|
| `paper/v14_7/` | v14_6を正本とする最新版。既存主要値を維持し評価器比較を追記 |
| `recalibration/evaluator_comparison.py` | 方策固定の前進・独立MC比較 |
| `results/recalibration_v8/fine/evaluator_*` | 分布・グライドパスの比較値、監査、再現性記録 |

詳細は [評価器比較の実行方法](recalibration/EVALUATOR_COMPARISON.md) を参照してください。


## 外部MGHベンチマーク（v14_7からv8）

`recalibration/external_vanstaden_2021/`に一次資料の仕様書、共通MGH核を使う後退・前進コード、独立理論参照、監査・報告コードを収録しました。`results/validation/van_staden_2021/`に全72設定の結果を保存しています。方策別ZIPには全NPZ・設定JSON・方策CSVが入り、展開後そのまま報告コードを実行できます。集計CSV、CDFデータ、図、環境・ソースハッシュもあります。

これは公表表から分布を逆算する旧検証と異なります。dTCMVは目的関数から独立計算していますが、掲載式との不整合が未解決のため部分的外部検証です。本文DC結果、既存の保存方策・再較正値、付録Eの評価器比較を変更していません。
