# DCグライドパス最適化：ICA2026再現コード

本リポジトリは、確定拠出年金（DC）の制約付き動的平均--分散最適化に関するICA2026論文の再現コード、主要な中間結果、および図表生成用データを公開するものです。

## 対象モデル

- 事前コミットメント平均--分散（PCMV）
- 動学的最適平均--分散（DOMV）
- 定数リスク回避の時間整合的平均--分散（cTCMV）
- 総年金富依存の時間整合的平均--分散（dTCMV）
- 平均--分散--歪度（MVS）拡張
- 厳密制約解と無制約クリップ近似の比較

すべての主要計算は、空売りおよび将来拠出を担保とする借入を認めない制約

```text
0 <= risky investment <= current DC balance
```

の下で実行します。

## 推奨環境

- Python 3.11 または 3.12
- NumPy, pandas, Matplotlib, SciPy, Numba, Pillow

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

日本語図を再生成する場合は、Noto Sans CJK JPをOSへインストールか、`fonts/NotoSansCJKjp-Regular.otf`へ配置してください。

## 四つのMV解概念の検証（付録A.3）

van Staden, Dang and Forsyth (2021) Table 5.1にはPCMV、DOMV、cTCMV、dTCMVの数値例が掲載されているため、四解概念すべてを外部再現の対象とします。本稿固有の制約付き月次実装については、独立前進分布、確率質量、境界量および入れ子格子を別途監査します。

```bash
python validation/external_validation_vanstaden2021_all_mv.py
python validation/run_all_validations.py
```

検証結果は `results/validation/` に保存されます。現行参照版では次の全項目が通過しています。

- PCMV：外部58項目 + 内部7項目 = 65/65
- DOMV：外部58項目 + 内部7項目 = 65/65
- cTCMV：外部58項目 + 内部7項目 = 65/65
- dTCMV：外部52項目 + 内部15項目 = 67/67

PCMVはreflected lognormal閉形式、DOMVとcTCMVは正規終端分布の閉形式からTable 5.1を再計算します。dTCMVは未公表の時変係数経路を再現したとはせず、公表平均・標準偏差から対数正規終端分布を同定して残りの分布指標を再計算する、分布レベルの外部検証としています。詳細は [validation/README.md](validation/README.md) を参照してください。

## 主な実行順序

完全な月次再計算は計算負荷が高いため、まず同梱済み配列から図を再生成する方法を推奨します。

```bash
python scripts/05_figures/localize_paper_figures_ja_20260717.py
```

主要な再計算は次の順序です。

```bash
python scripts/01_solvers/pcmv_domv_solver_20260713.py
python scripts/03_rolling/recompute_d0_rolling.py
python scripts/04_sensitivity/add_all_clip_overlays_20260721.py --output-dir d0_sensitivity_outputs
python scripts/04_sensitivity/numerical_diagnostics_20260718.py
python validation/run_all_validations.py
python scripts/01_solvers/dtcmv_mvs_solver_20260713.py
python scripts/02_calibration/run_mvs_refined_calibration.py
python scripts/05_figures/make_dtcmv_mvs_fixed_gamma_terminal_distribution.py
```

番号は作業の大まかな流れを表します。全スクリプトの役割と実行区分は [scripts/README.md](scripts/README.md) および [CODEBOOK_JA.md](CODEBOOK_JA.md) を参照してください。

## 四解概念の厳密制約解とクリップ近似

年80分割の感応度分析では、PCMV、DOMV、cTCMV、dTCMVの全解概念について、制約付き問題を直接解いたフィードバックと、対応する無制約解析解を事後的に `0 <= pi <= x` へ射影したクリップ近似を比較します。

- 実線：厳密制約フィードバック
- 同色の点線：無制約解のクリップ近似
- 両方策は、それぞれが生成する残高分布の下で独立に前進伝播

![期待収益率感応度における全解概念の厳密解とクリップ解](supplementary/figures/fig_mu_sensitivity_glidepaths_N80.svg)

PCMVは固定ターゲット型の無制約解、DOMVは各時点再最適化型の無制約解、cTCMVは定数リスク回避型の解析解、dTCMVはVolterra方程式から得る時変係数を用いています。計算式と実装は [`add_all_clip_overlays_20260721.py`](scripts/04_sensitivity/add_all_clip_overlays_20260721.py)、全5図は [補足図ページ](supplementary/figures/README.md)、差分集計は [`all_strategies_strict_vs_clip_sensitivity_summary.csv`](results/sensitivity/all_strategies_strict_vs_clip_sensitivity_summary.csv) を参照してください。

比較の結果、基準パラメータで差が小さい解概念があっても、パラメータ変更後に同様に近いとは限りません。特にPCMVおよびdTCMVでは、シナリオによって直接制約解とクリップ近似の差が大きくなります。

## dTCMV--MVS固定係数グライドパスの終端分布

補足図Figure 6の各グライドパスが生成する終端退職資産分布です。分散回避係数は `gamma0=2.5` に固定され、`eta0=0` がMV基準、正の `eta0` がMVSです。これは共通平均比較ではありません。

![Figure 6の固定係数グライドパスに対応する終端分布](supplementary/figures/fig_dtcmv_mvs_fixed_gamma_terminal_distribution.svg)

上段は終端資産の密度、下段はq05--q95区間とMedian（丸印）・Mean（菱形）です。色はFigure 6のグライドパスと対応しています。

| Strategy | eta0 | Mean | SD | Skewness | q05 | Median | q95 | Lower-tail mean (bottom 5%) | Upper-tail mean (top 5%) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| MV | 0.0 | 70.34 | 22.97 | 0.91 | 39.14 | 67.41 | 111.93 | 33.44 | 129.08 |
| MVS | 0.5 | 73.37 | 25.03 | 0.94 | 39.14 | 71.11 | 118.64 | 33.34 | 137.74 |
| MVS | 1.0 | 84.28 | 33.71 | 1.05 | 39.14 | 78.71 | 146.90 | 32.74 | 172.95 |
| MVS | 2.0 | 97.66 | 46.72 | 0.99 | 39.14 | 88.62 | 187.99 | 30.70 | 218.74 |

`eta0`を高めると平均・中央値・上方裾が大きく上昇する一方、標準偏差も22.97から46.72へ拡大します。保存済みq05は、CDFが5%へ到達する最初の状態格子点を返すため、4ケースとも同じ格子区間37.66--39.14に入り、39.14と記録されています。格子間を線形補間したq05は順に38.04、38.40、38.92、37.69であり、実際には一致しません。さらに補間q01は29.29から24.98へ、下方5%平均は33.44から30.70へ低下します。したがって、係数の上昇は上方参加を強めますが、分散と極端な下方リスクを同時に悪化させ得ます。丸め前の集計値は [`dtcmv_mvs_fixed_gamma_distribution_table.csv`](results/dtcmv_mvs_fixed_gamma_distribution_table.csv) に収録しています。

## 最終稿で追加した診断

Table 10のdTCMV U字型成因分解と、付録A.4の理論的射影領域・直接探索領域の一致診断は、`diagnostics/`で再計算できます。

```bash
python diagnostics/additional_diagnostics.py
python diagnostics/unconstrained_dtcmv_theta.py
python diagnostics/recompute_crosscheck.py
python diagnostics/pcmv_crosscheck.py
```

実行順序と出力CSVの説明は [diagnostics/README.md](diagnostics/README.md) を参照してください。

## ディレクトリ

- `results/`: 論文の主要表、較正値、ローリング評価および方策配列
- `results/validation/`: 四つのMV解概念の自動判定結果
- `results/sensitivity/`: 全解概念の厳密解・クリップ近似の感応度差分
- `validation/`: 付録A.3に対応する外部・内部妥当性検証
- `diagnostics/`: Table 10のU字型分解および付録A.4の自由境界クロスチェック
- `figs/`: 論文掲載図の日本語版と再生成に必要な原図
- `supplementary/figures/`: 本文未掲載の補足図と各図の解説
- `scripts/01_solvers/`: PCMV・DOMV・dTCMV--MVSの中核ソルバー
- `scripts/02_calibration/`: 共通平均・MVS係数の較正
- `scripts/03_rolling/`: ローリング条件付き評価と関連図
- `scripts/04_sensitivity/`: 感応度分析と再集計
- `scripts/05_figures/`: 論文図の再生成・日本語化
- `scripts/90_workers/`: 分割実行用の補助ワーカー（通常は直接実行しません）

## 本文未掲載の補足図

感応度分析、制約診断、ローリング評価およびMVS詳細図を、[補足図ページ](supplementary/figures/README.md) にまとめています。各図の直下に日本語の説明を掲載しています。

## 再現性上の注意

- `monthly_D0_policy_arrays.npz`は、40年・月次（480期）の基準計算から得た方策・分布配列です。
- 感応度図は年80分割のスクリーニング計算です。実線と点線は同一状態分布上の単純比較ではなく、各方策の自己生成分布に基づくグライドパスです。
- `numerical_diagnostics_20260718.py`は、正規化前質量、上下端超過量、後退・前進モーメント整合性、およびdTCMV上端格子感応度を再計算します。
- 基準格子 `x_max=300` のdTCMVは右裾統計に上端感応度があるため、尾部の妥当性は `x_max=900` 以上の入れ子格子で判定します。
- MVSの正の歪度係数に関する結果は、非凹性と離散化依存性を伴う探索的結果です。
- 付属配列からの作図は高速ですが、ソルバーからの完全再計算にはCPU時間とメモリを要します。
- 論文中の数値は、対応するCSV/NPZを正本として照合してください。

## Citation

このコードを利用する場合は、公開後のICA2026論文と本リポジトリのリリースを引用してください。書誌情報は採択・公開後に更新します。

## License

MIT License。詳細は [LICENSE](LICENSE) を参照してください。
