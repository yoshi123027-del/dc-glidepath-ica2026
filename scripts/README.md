# Pythonコード案内

Pythonコードは役割ごとに番号付きフォルダへ整理しています。番号は厳密な依存順ではなく、再現作業を読むときの大まかな順序です。コマンドはリポジトリのルートで実行してください。

## まず試す場合

同梱済みのCSV/NPZから論文図を再生成します。完全な月次最適化より短時間で確認できます。

```bash
python scripts/05_figures/localize_paper_figures_ja_20260717.py
```

## 01_solvers：中核ソルバー

| ファイル | 役割 |
| --- | --- |
| `pcmv_domv_solver_20260713.py` | PCMV・DOMVの制約付きソルバー |
| `dtcmv_mvs_solver_20260713.py` | dTCMV--MVSのモーメント後退計算 |

## 02_calibration：較正

| ファイル | 役割 |
| --- | --- |
| `equal_mean_calibration_20260713.py` | 共通平均比較用の較正値を整理 |
| `run_mvs_refined_calibration.py` | MVS係数の精緻較正 |

## 03_rolling：ローリング評価

| ファイル | 役割 |
| --- | --- |
| `recompute_d0_rolling.py` | 基準ケース、終端分布、ローリング評価を再計算 |
| `detailed_dtcmv_rolling_overlay_20260713.py` | 残高分位点別のローリング評価 |
| `make_common_state_rolling_figure_20260713.py` | 共通状態ローリング比較図を生成 |
| `rebuild_rolling_equal_mean.py` | 共通平均較正のローリング結果を再構築 |

## 04_sensitivity：感応度分析

| ファイル | 役割 |
| --- | --- |
| `low_balance_refined_sensitivity_20260714.py` | 低残高領域を精緻化した感応度分析 |
| `rebuild_baseline_sensitivity.py` | 基準ケースと感応度結果を再集計 |
| `numerical_diagnostics_20260718.py` | モーメント整合性、正規化前質量、境界超過量、dTCMV上端格子感応度を再計算 |

## 05_figures：出力・作図

| ファイル | 役割 |
| --- | --- |
| `rebuild_all_corrected_glide_outputs.py` | 修正済みグライドパス・分布出力を一括再構築 |
| `localize_paper_figures_ja_20260717.py` | 論文図を日本語で再生成 |

## 90_workers：補助ワーカー

`mvs_worker.py`と`sensitivity_worker.py`は分割実行用です。通常は直接実行しません。

## 主要な再計算順序

```bash
python scripts/01_solvers/pcmv_domv_solver_20260713.py
python scripts/03_rolling/recompute_d0_rolling.py
python scripts/04_sensitivity/numerical_diagnostics_20260718.py
python scripts/01_solvers/dtcmv_mvs_solver_20260713.py
python scripts/02_calibration/run_mvs_refined_calibration.py
```

各スクリプトは移動後も、リポジトリ直下の `results/` と `figs/` を参照します。
