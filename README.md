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
python scripts/04_sensitivity/numerical_diagnostics_20260718.py
python validation/run_all_validations.py
python scripts/01_solvers/dtcmv_mvs_solver_20260713.py
python scripts/02_calibration/run_mvs_refined_calibration.py
```

番号は作業の大まかな流れを表します。全スクリプトの役割と実行区分は [scripts/README.md](scripts/README.md) および [CODEBOOK_JA.md](CODEBOOK_JA.md) を参照してください。

## ディレクトリ

- `results/`: 論文の主要表、較正値、ローリング評価および方策配列
- `results/validation/`: 四つのMV解概念の自動判定結果
- `validation/`: 付録A.3に対応する外部・内部妥当性検証
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
- `numerical_diagnostics_20260718.py`は、正規化前質量、上下端超過量、後退・前進モーメント整合性、およびdTCMV上端格子感応度を再計算します。
- 基準格子 `x_max=300` のdTCMVは右裾統計に上端感応度があるため、尾部の妥当性は `x_max=900` 以上の入れ子格子で判定します。
- MVSの正の歪度係数に関する結果は、非凹性と離散化依存性を伴う探索的結果です。
- 付属配列からの作図は高速ですが、ソルバーからの完全再計算にはCPU時間とメモリを要します。
- 論文中の数値は、対応するCSV/NPZを正本として照合してください。

## Citation

このコードを利用する場合は、公開後のICA2026論文と本リポジトリのリリースを引用してください。書誌情報は採択・公開後に更新します。

## License

MIT License。詳細は [LICENSE](LICENSE) を参照してください。
