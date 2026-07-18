from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = RESULTS / "validation"


def one_row(frame: pd.DataFrame, model: str) -> pd.Series:
    rows = frame.loc[frame["strategy"] == model]
    if len(rows) != 1:
        raise ValueError(f"expected one row for {model}")
    return rows.iloc[0]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    moments = pd.read_csv(RESULTS / "moment_consistency_D0_N480.csv")
    mass = pd.read_csv(RESULTS / "mass_truncation_summary_D0_N480.csv")
    external = pd.read_csv(OUT / "vanstaden2021_pcmv_reproduction.csv")
    xmax = pd.read_csv(RESULTS / "xmax_sensitivity_dtcmv_D0_N480.csv")

    rows = []
    for model, upper_tol, boundary_tol in (
        ("PCMV", 1e-12, 1e-12),
        ("DOMV", 1e-5, 1e-6),
        ("cTCMV", 1e-8, 1e-10),
        ("dTCMV", None, None),
    ):
        m = one_row(moments, model)
        z = one_row(mass, model)
        checks = {
            "epsilon_M": m.epsilon_M <= 1e-8,
            "epsilon_Q": m.epsilon_Q <= 1e-6,
            "mass": z.max_raw_mass_error <= 1e-12,
            "lower": z.max_step_lower_excursion_mass <= 1e-12,
            "saved_pmf": z.max_l1_difference_from_saved_pmf <= 1e-12,
        }
        if upper_tol is not None:
            checks["upper"] = z.max_step_upper_excursion_mass <= upper_tol
            checks["boundary"] = z.terminal_upper_boundary_mass <= boundary_tol
        rows.append({
            "model": model,
            "validation": "baseline backward-forward and mass diagnostics",
            "checks_passed": sum(checks.values()),
            "checks_total": len(checks),
            "epsilon_M": m.epsilon_M,
            "epsilon_Q": m.epsilon_Q,
            "max_raw_mass_error": z.max_raw_mass_error,
            "overall_check": all(checks.values()),
        })

    pc_checks = external["overall_check"].astype(str).str.lower().isin({"true", "1"})
    rows.append({
        "model": "PCMV",
        "validation": "van Staden et al. (2021) Table 5.1 external reproduction",
        "checks_passed": int(pc_checks.sum()),
        "checks_total": len(pc_checks),
        "epsilon_M": float("nan"),
        "epsilon_Q": float("nan"),
        "max_raw_mass_error": float("nan"),
        "overall_check": bool(pc_checks.all()),
    })

    x = xmax.loc[xmax["x_max"] == 900.0].iloc[0]
    checks = {
        "epsilon_M": x.epsilon_M <= 1e-8,
        "epsilon_Q": x.epsilon_Q <= 1e-6,
        "mass": x.max_raw_mass_error <= 1e-12,
        "upper": x.max_step_upper_excursion_mass <= 1e-6,
        "mean": x.abs_diff_vs_xmax2100_mean <= 5e-4,
        "stdev": x.abs_diff_vs_xmax2100_stdev <= 1e-3,
        "q05": x.abs_diff_vs_xmax2100_q05 <= 1e-10,
        "q50": x.abs_diff_vs_xmax2100_q50 <= 1e-10,
        "q95": x.abs_diff_vs_xmax2100_q95 <= 1e-10,
        "tails_and_glide": max(x.abs_diff_vs_xmax2100_lcvar05, x.abs_diff_vs_xmax2100_ucvar95, x.abs_diff_vs_xmax2100_average_glide) <= 5e-4,
    }
    rows.append({
        "model": "dTCMV",
        "validation": "nested x_max=900 versus x_max=2100 stability",
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "epsilon_M": x.epsilon_M,
        "epsilon_Q": x.epsilon_Q,
        "max_raw_mass_error": x.max_raw_mass_error,
        "overall_check": all(checks.values()),
    })

    detailed = pd.DataFrame(rows)
    detailed.to_csv(OUT / "all_mv_validation_detailed.csv", index=False)
    summary = detailed.groupby("model", sort=False).agg(
        validation_rows=("validation", "count"),
        checks_passed=("checks_passed", "sum"),
        checks_total=("checks_total", "sum"),
        max_epsilon_M=("epsilon_M", "max"),
        max_epsilon_Q=("epsilon_Q", "max"),
        max_raw_mass_error=("max_raw_mass_error", "max"),
        overall_check=("overall_check", "all"),
    ).reset_index()
    summary.to_csv(OUT / "all_mv_validation_summary.csv", index=False)
    print(summary.to_string(index=False))
    if not bool(summary.overall_check.all()):
        raise RuntimeError("at least one MV validation failed")


if __name__ == "__main__":
    main()
