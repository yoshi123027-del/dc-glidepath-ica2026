# MGH forward vs independent Euler-MC evaluator comparison

This is an **evaluation-only** experiment. The same five saved risky-dollar
feedback arrays (`PCMV`, `DOMV`, `cTCMV`, `dTCMV`, `CP`) are input to both
evaluators. No optimisation, coefficient recalibration, market change, action
search or seed selection is performed. The common-mean target remains 84.78.

## Provenance and manuscript

- Base repository commit: `c058ac7` (default branch `main`). Its manuscript was
  v11, but its active recalibration data remain the source of the current paper.
- Manuscript base: `ICA2026_Japanese_revised_v14_6.tex`, the latest Japanese
  wording revision delivered to the author (the requested "v6").
- Updated manuscript: `paper/v14_7/ICA2026_Japanese_revised_v14_7.tex` and PDF.
- Inputs: `results/recalibration_v8/fine/{PCMV,DOMV,cTCMV,dTCMV,CP}.{npz,json}`,
  `config.json`, `independent_mc.{npz,csv}`. These original files are unchanged.
- Every input's SHA-256 and the actual runtime versions are recorded in
  `evaluator_validation.json`. No archive/legacy policy is loaded.
- The existing CSV reproduces every mean, SD, q05, median, q95 and lower-5%-mean
  in current manuscript Table 5 at its printed precision.

## What is held fixed

40 years, 480 monthly steps, r=0.015, excess drift=0.04, volatility=0.18,
annual contributions=1, initial wealth=1/12, terminal background payment=0.
Policies: cap=600, 6001 nodes, spacing=0.1, 129 candidate controls, GH7.
The saved coefficients and policy arrays are never rewritten.
The finer **calibration evaluator** (spacing=0.025, GH31) is not the MGH
forward evaluator in this experiment.

MGH uses GH7 shocks and nonnegative linear mass deposition with lower/upper
clamps at 0/600. The very first transition starts at exact wealth=1/12 with
interpolated risky dollars, as specified by current Appendix B. From month 1
onwards the existing finite-model transition formula is used at all nodes.
The old `checks.py` initialises mass on two nodes; therefore its previously
saved moment checks differ slightly. They are retained, not overwritten.
This initialisation distinction is reported in Appendix E.3.

MC uses the already saved 1,000,000 terminal outcomes and all 480 monthly mean
allocations from `independent_mc.npz`. Its implementation is `validate.py`:
100 RNG blocks; seed=20260912; block seed=seed+1009*block; common normal shocks
across policies; risky-dollar interpolation; no upper wealth cap; continuation
at the endpoint risky fraction above 600; negative steps floored at zero.
`--rerun-mc` re-evaluates the same policies with these exact settings and checks
against all saved paths, without overwriting the original file. Cross-runtime
floating-point deviations are reported (not claimed to be bitwise identical).
The tolerances are 1e-7 wealth units per path and 1e-11 for mean allocations.

## Definitions

- MGH CDF: unsmoothed discrete probability mass, normalised only for
  floating-point mass roundoff. Raw total mass is audited at every month.
- MGH quantile: smallest support node whose cumulative mass reaches p.
- MGH lower/upper 5% mean: accumulate exactly 0.05 mass, fractionally allocating
  the boundary atom. MC retains NumPy's default empirical quantile and the
  arithmetic mean of the lowest/highest 50,000 sorted draws.
- MGH SD is a probability-distribution SD. MC SD uses ddof=1, unchanged.
- KS-type distance is the exact supremum across left/right limits at every
  MGH and MC support point. No p-value from a continuous-null KS test is used.
- Mean glide paths are means of **ratios**, not ratios of mean risky dollars to
  mean wealth. At month 0 the exact initial state is used. At later months
  g=0 at wealth=0 follows the existing summation over positive nodes. All
  computed lower-boundary masses are zero. There is no terminal control.
- Differences are MGH minus MC. Glide errors in the summary CSV are percentage
  points: an allocation fraction difference of 0.01 equals 1 pp.
- The saved policy function is identical. Differences in mean glide paths
  reflect different induced state distributions, not different optimal policies.
- No continuous-time exactness, global continuous-control optimality, or
  uniform discretisation-error bound is certified by this experiment.

## Run from repository root

```bash
python -m pip install -r requirements.txt
python recalibration/evaluator_comparison.py --rerun-mc
python recalibration/plot_evaluator_comparison.py
```

Without `--rerun-mc`, the first command reuses the existing million paths and
monthly allocations. Both modes run MGH forward propagation and backward
**evaluation of the fixed policy** (no Bellman max/optimisation).
It checks all monthly mass totals, nonnegativity, boundaries, first/second
moment identities including deposition variance, and the constant CP glide.
The seed is fixed; failed equality checks must not trigger seed changes.

## Outputs under results/recalibration_v8/fine

| File | Contents |
|---|---|
| evaluator_comparison.npz | names, grid, all five terminal MGH masses, MGH/MC monthly mean glide paths, original MC source reference, seed, exact initial wealth |
| evaluator_distribution_comparison.csv | both evaluators' mean, SD, q01/q05/median/q95, lower/upper 5% means, skewness |
| evaluator_comparison.csv | exact KS-type distance and all signed statistic differences |
| evaluator_glidepath_comparison.csv | maximum absolute gap, MAE, RMSE (pp), time of maximum |
| evaluator_glidepaths.csv | all 480 monthly mean allocations and signed gaps per strategy |
| evaluator_mass_audit.csv | monthly mass total/minimum/boundaries, crossing mass, moments, deposition variance and identity residuals |
| evaluator_validation.json | source hashes, invariance/reproduction checks, settings and runtime |
| fig_evaluator_cdf_comparison.png / .pdf | five-panel raw CDF overlay; PCMV upper-CDF inset |
| fig_evaluator_glidepath_comparison.png / .pdf | five-panel mean allocation overlay |

MC terminal outcomes are already stored in `independent_mc.npz` and are not
duplicated. Full intermediate MGH masses can be regenerated by `forward()`;
monthly audit summaries are saved. CDF plots show wealth 0–200 for readability;
statistics and distances use the full support. Curves are not density estimates
and are not smoothed. The original data are never silently replaced.
