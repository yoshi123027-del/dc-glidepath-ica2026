# v8: re-optimisation and common-mean recalibration

This module replaces the historical saved-policy comparison with freshly
optimised finite-model policies. Target expected terminal wealth: **84.78**.
See `../results/recalibration_v8` for parameters, policies and validation data,
and `../archive/v8/paper/ICA2026_Japanese_revised_v8.pdf` for the updated Japanese paper.

## What is optimised

- PCMV: the fixed-target squared-loss Bellman problem. The target is recalibrated.
- DOMV: a family of fixed-target Bellman problems; each date/state selects the
  maximum embedding score over the entire target grid and uses its first action.
- cTCMV and dTCMV: backward induction of the finite-date one-step equilibrium,
  with constant gamma and gamma=rho/(x+H), respectively. Each coefficient trial
  repeats the equilibrium computation; it does not rescale a saved policy.
- CP: the constant fraction is calibrated with exact Euler moment recurrences.

The common Markov approximation has a wealth cap of 600, nonnegative linear
mass deposition and GH shocks. All finite controls are exhaustively compared.
Optimality is within this finite state/action model; continuous-time optimality
is not certified. Interpolated risky dollars are used in independent evaluation.
Neither interpolation error nor tail uncertainty is concealed by rounding means.

DOMV uses targets 0,2,...,650. For the calibrated gamma range [0.02,0.2], this
covers [0,L+1/gamma] since terminal wealth is bounded by L=600 in the finite model.
The embedding-value error from maximum target spacing delta is bounded by
gamma*delta^2/8. This is not a bound on realised rolling-DOMV terminal performance.

## Reproduction

Python 3.12, NumPy and Numba are sufficient for this module. Install the root
`requirements.txt` for the historical scripts as well. Run from repository root:

```bash
python recalibration/run.py family --out results_v8/base
python recalibration/run.py pc --eval-h .05 --eval-ng 9 --out results_v8/base
python recalibration/run.py tc --eval-h .05 --eval-ng 9 --out results_v8/base
python recalibration/run.py cp --out results_v8/base
python recalibration/run.py dom --out results_v8/base

python recalibration/run.py family --nx 6001 --nc 129 --ng 7 --out results_v8/fine
python recalibration/run.py pc --nx 6001 --nc 129 --ng 7 --out results_v8/fine
python recalibration/run.py tc --nx 6001 --nc 129 --ng 7 --out results_v8/fine
python recalibration/run.py cp --nx 6001 --nc 129 --ng 7 --out results_v8/fine
python recalibration/run.py dom --nx 6001 --nc 129 --ng 7 --out results_v8/fine

python recalibration/validate.py results_v8/fine --paths 1000000 --seed 20260912
python recalibration/checks.py results_v8/fine
python recalibration/sensitivity.py results_v8/fine --boundary --recalibrate-boundary
python recalibration/acceptance.py results_v8/fine
```

Target families are large scratch arrays (about 17 GB for both resolutions) and
are not committed. Generation may take tens of minutes or longer. Final policy
arrays, parameters and compact checks are committed. Independent terminal draws
are reproducible from the seed but are not required to execute the checks.

The stopping target in bisection is 0.002 wealth units; finite-control equilibrium
selection can be discontinuous in the coefficient. Always inspect the actual
reported mean error, not merely process exit status. Final acceptance also needs
independent common-random-number mean-difference intervals and mesh/quadrature
sensitivity. A zero difference in a rounded table is not an acceptance test.

## Validation scope

`checks.py` separately checks saved-policy reproduction, forward/backward moments,
probability mass, the CP analytical anchor and exact continuous-action breakpoint
search at explicitly listed dates/states. The latter is a sampled audit, not a
whole-state-space uniform error bound. `sensitivity.py` records re-optimisation
with a cap of 900 at the same coefficients, separately from re-calibration.

`validate.py` uses 100 independent RNG blocks and shared normal Euler shocks
across strategies, exact initial wealth, no wealth-grid mass deposition and no
upper wealth cap. It reports mean SEs, paired differences, lower-tail outcomes
and cap-crossing diagnostics. Changing the model (e.g. lognormal buy-and-hold)
requires its own re-optimisation and calibration.

The legacy figures/results elsewhere in the repository remain historical.
In particular, their equal-mean calibration and variance claims should not be
substituted for the v8 data. The unconstrained dTCMV diagnostic's variance sign
has been corrected separately; constrained equilibrium calculation here does
not depend on an unconstrained clipped formula.

The historical Japanese v11 manuscript is retained at `../paper/v11/ICA2026_Japanese_revised_v11.pdf`. The latest is `../paper/v14_7/ICA2026_Japanese_revised_v14_7.pdf`; its main Table 5 reports the unchanged recalibration results and Appendix E.3 adds fixed-policy evaluator validation. Coarse base results are preserved in `../archive/v8/base/`. No new optimisation was run for the v11 structural revision.

## Fixed-policy evaluator validation (v14_7)

See [EVALUATOR_COMPARISON.md](EVALUATOR_COMPARISON.md) for the MGH forward vs independent million-path Euler-MC comparison. Only the evaluator changes; the saved policies, coefficients and calibration target are fixed. The comparison covers full terminal CDFs and distribution-weighted mean glide paths. It does not prove continuous-time exactness.
