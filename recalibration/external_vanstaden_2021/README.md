# External MGH benchmark: van Staden, Dang and Forsyth (2021)

This is an actual numerical backward-policy / forward-distribution calculation,
not merely recalculation of a published table from closed-form formulas. The
source manuscript is **v14_7**; its successor for this task is **v8**.
Read [the source specification](BENCHMARK_SPECIFICATION.md) first.

## Scope and common engine

The conditional-moment loop of `recalibration/finite_model.py` is extracted into
`interpolated_moments`. The existing constrained DC solver and the unconstrained
external adapter both call this kernel, with the same normalized GH generator.
`regression.py` compares the original pinned DC solver with the extracted version:
policies, means and second moments are bitwise identical in the three regression
cases. No DC policy, calibration coefficient, contribution, target 84.78, or
published main-table result is changed.

The adapter supplies the external SDE, signed/unconstrained controls, lattice,
objective and numerical control optimizer. The backward recursion exploits the
translation/scaling symmetry of the lattice: future moment values at neighboring
nodes are computed from recursively obtained coefficients, and the shared engine
interpolates and integrates those values. `audit.py` verifies this reduction
against direct interpolation of full moment arrays at 54 interior points.
This validates a shared-kernel specialization of the MGH architecture, **not an
unchanged invocation of all constrained DC code branches**. Forward deposition
is the nonnegative adjoint of the same linear interpolation on a finite domain.
The first step starts from the exact off-grid initial state; consistency checks
use its actual interpolated conditional moments, not a polynomial extension.

PCMV solves the embedded quadratic loss numerically. DOMV numerically optimizes
the scalarization over the family of translated remaining-horizon PCMV problems
and connects the first controls. cTCMV/dTCMV optimize each one-step equilibrium
against future recursively obtained moments. No analytical optimal control is
supplied to `engine.py`. The scalar optimizer scans the entire finite range and
refines the five best neighborhoods; this is not a proof of global optimality.

The state is discounted to terminal dollars, Y=exp(r(T-t))*W. PCMV uses a signed
geometric surplus lattice; DOMV/cTCMV use a uniform lattice. dTCMV uses the positive
proportional branch and exact frozen-proportion GBM transitions. It therefore
does not use a clipped Euler transition or reproduce the DC mapping unchanged.
The finite control and state domains, their expansions, and all runs are reported.

## dTCMV: independent calculation, unresolved source discrepancy

Original eq. (2.10) uses rho/(2w). With terminal moments m=a*w and Q=c*w²,
the continuous equilibrium first-order condition gives

    theta = b/(rho*sigma²) * [a/c + rho*(a²/c - 1)].

Consequently a/c=exp(-integral(r+b*theta+sigma²*theta²)). The printed eq. (3.5)
has a minus sign before sigma²*theta² inside that integral. We do not silently
amend the source: `dtcmv_printed_equation_diagnostic.csv` retains both versions.
The independent benchmark branch derives its ODE from the objective, with zero
initial integrals in reverse time. Rho is determined from the specified target
mean (eq.4.5); published SD, median and rounded rho are never inputs. The MGH
backward recursion independently optimizes the objective and does not import
that ODE's control path. The ODE is used for parameter calibration and as a
separate continuous-time policy/distribution reference.

For target250, literal eq.3.5 yields SD204.478, the objective-derived equilibrium
SD446.751, and Table5.1 reports444. This unresolved gap is explicitly retained.
Thus dTCMV is an independent equilibrium computation but **partial external
source validation**, not complete reproduction of the printed equation and table.
The old mean/SD-based distribution reconstruction elsewhere in the repository is
historical and is not evidence for this MGH validation.

## Reproduce

Python with NumPy, SciPy, Numba and Matplotlib is required; exact installed
versions and source hashes are recorded in `run_metadata.json`.

```bash
python recalibration/external_vanstaden_2021/run.py --suite all
python recalibration/external_vanstaden_2021/audit.py
python recalibration/external_vanstaden_2021/regression.py
python recalibration/external_vanstaden_2021/report.py
```

Run from the repository root. `--strategy PCMV` (or DOMV/cTCMV/dTCMV) partitions
independent calculations. The script checkpoints complete run pairs; remove the
corresponding generated run files to recompute after changing solver code.
There are 72 configurations: 8 baseline, 48 one-factor variants at target250,
and 16 additional coupled space/time refinements at both targets. No matching
configuration is selected after seeing results. The final table always uses the
predeclared finest coupled setting, including its non-monotonic or remaining
errors. Time-only refinement at fixed spatial spacing need not converge because
interpolation errors accumulate; the coupled path is a separate consistency
check, not a substitute for the one-factor attribution study.

## Output files

All outputs are in `results/validation/van_staden_2021/`.

- `benchmark_parameters.json`, `model_parameters.json`: unrounded input parameters.
- `published_vs_mgh.csv`: all Table5.1 outputs, absolute and relative errors.
  Rounded calibration parameters are flagged separately. Relative errors at zero
  published values are blank; absolute errors remain reported. No pass thresholds.
- `final_summary.csv`: final distribution statistics, CDF gap, policy errors.
- `convergence.csv`: every setting with mean, SD, q05, q95 and CDF gap.
- `policy_comparison.csv`: initial/middle/final decision dates, wealth50/100/250.
- `cdf_comparison.csv.gz`: every final grid node, unsmoothed mass, both CDFs.
- `boundary_control_diagnostics.csv`: mass conservation/nonnegativity, boundary
  occupation and cumulative first-exit probability, moment losses, control bounds,
  and fixed-policy backward/forward moment consistency.
- `external_cdf_comparison.*`, `external_convergence.*`: publication figures.
- `*_runs.zip`: all per-run NPZ arrays, JSON metadata and policy CSVs, grouped by
  strategy. Extract into the output directory before reporting without rerunning.
  NPZ `audit` columns are: step, total mass, minimum mass, lower/upper endpoint mass,
  lower/upper out-of-domain transition mass, cumulative first-exit probability,
  signed first-moment clipping loss, second-moment clipping loss.
  NPZ controls are surplus-normalized for PCMV, terminal-dollar amounts for
  DOMV/cTCMV, and wealth fractions for dTCMV; physical dollar policies are in CSV.
- `run_metadata.json`: source commit, execution dates, package versions, code hashes.

Discrete quantiles use the left inverse CDF. Lower-tail means split the boundary
atom to use exactly the requested probability. D_CDF checks both sides of every
MGH jump against the continuous reference; no smoothing is used. q95 and CDFs are
**theory comparisons**, not values claimed to appear in Table5.1. Large relative
errors near zero or against integer-rounded published values should be read
alongside absolute errors. Higher moments are retained, not omitted as inconvenient.

## Three distinct validation layers

1. Same finite model: backward/forward moment consistency and mass conservation.
2. DC baseline: the same saved policy under MGH versus independent 1-million-path
   Euler MC, terminal distributions and mean glide paths (Appendix E unchanged).
3. External benchmark: shared MGH kernel applied to a different unconstrained
   mean-variance problem, compared with analytical and published outputs.

These are numerical evidence, not a proof of continuous-time optimality, general
convergence, all-state optimal controls, or validity of exploratory MVS.
