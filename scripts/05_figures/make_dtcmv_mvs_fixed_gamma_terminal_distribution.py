from __future__ import annotations

import argparse
import sys
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
SOLVER_DIR = ROOT / "scripts" / "01_solvers"
sys.path.insert(0, str(SOLVER_DIR))
import dtcmv_mvs_solver_20260713 as solver


SUMMARY = ROOT / "results" / "dtcmv_mvs_fixed_gamma_summary.csv"
DEFAULT_OUTPUT_DIR = ROOT / "supplementary" / "figures"
STEM = "fig_dtcmv_mvs_fixed_gamma_terminal_distribution"

FIGURE_WIDTH_CM = 13.0
FIGURE_HEIGHT_CM = 7.0
ETA_GRID = np.array([0.0, 0.5, 1.0, 2.0])
COLORS = {
    0.0: "#1F77B4",
    0.5: "#FF7F0E",
    1.0: "#2CA02C",
    2.0: "#D62728",
}
NOMINAL_MONTE_CARLO_SIZE = 100_000


def weighted_quantile(values: np.ndarray, weights: np.ndarray, q: float) -> float:
    order = np.argsort(values)
    values = values[order]
    weights = weights[order]
    cumulative = np.cumsum(weights) / weights.sum()
    return float(np.interp(q, cumulative, values))


def silverman_density(
    values: np.ndarray,
    weights: np.ndarray,
    evaluation_grid: np.ndarray,
) -> tuple[np.ndarray, float]:
    """Weighted Gaussian KDE with a floor tied to the state-grid resolution."""
    weights = np.asarray(weights, dtype=float)
    weights = weights / weights.sum()
    mean = float(np.sum(weights * values))
    variance = float(np.sum(weights * (values - mean) ** 2))
    standard_deviation = np.sqrt(max(variance, 0.0))
    q25 = weighted_quantile(values, weights, 0.25)
    q75 = weighted_quantile(values, weights, 0.75)
    robust_scale = min(standard_deviation, (q75 - q25) / 1.34)
    if robust_scale <= 0.0:
        robust_scale = max(standard_deviation, 1.0)
    bandwidth = 0.9 * robust_scale * NOMINAL_MONTE_CARLO_SIZE ** (-0.2)
    bandwidth = max(bandwidth, 1.75 * np.median(np.diff(values)))

    standardized = (evaluation_grid[:, None] - values[None, :]) / bandwidth
    kernel = np.exp(-0.5 * standardized**2) / np.sqrt(2.0 * np.pi)
    density = kernel @ weights / bandwidth
    return density, float(bandwidth)


def solve_fixed_gamma_cases() -> list[dict[str, object]]:
    base_config = solver.Config(gamma0=2.5, eta0=0.0)
    baseline = solver.solve_case(base_config)
    transition_maps = baseline["maps"]
    results = [baseline]
    for eta0 in ETA_GRID[1:]:
        config = replace(base_config, eta0=float(eta0))
        results.append(solver.solve_case(config, maps=transition_maps))
    return results


def validate_results(results: list[dict[str, object]], summary: pd.DataFrame) -> None:
    if not np.allclose(summary["eta0"], ETA_GRID):
        raise ValueError("The fixed-gamma summary does not contain the expected eta grid.")
    if not np.allclose(summary["gamma0"], 2.5):
        raise ValueError("The fixed-gamma summary does not use gamma0=2.5.")

    columns = ["mean", "stdev", "skewness", "q05", "q50", "q95", "cvar05", "ucvar95"]
    for index, result in enumerate(results):
        statistics = result["stats"]
        for column in columns:
            if not np.isclose(statistics[column], summary.loc[index, column], atol=5e-6):
                raise ValueError(
                    f"Recomputed {column} for eta0={ETA_GRID[index]:g} does not match the saved summary."
                )


def make_figure(output_dir: Path) -> list[Path]:
    summary = pd.read_csv(SUMMARY)
    results = solve_fixed_gamma_cases()
    validate_results(results, summary)
    output_dir.mkdir(parents=True, exist_ok=True)

    density_grid = np.linspace(0.0, 260.0, 1600)
    densities: list[np.ndarray] = []
    bandwidths: list[float] = []
    for result in results:
        wealth_grid = np.asarray(result["x_grid"], dtype=float) + result["cfg"].D
        terminal_mass = np.asarray(result["pmf"][-1], dtype=float)
        density, bandwidth = silverman_density(wealth_grid, terminal_mass, density_grid)
        densities.append(density)
        bandwidths.append(bandwidth)

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 6.8,
            "axes.titlesize": 7.6,
            "axes.labelsize": 7.2,
            "xtick.labelsize": 6.2,
            "ytick.labelsize": 6.2,
            "legend.fontsize": 6.0,
            "axes.linewidth": 0.65,
        }
    )
    figure = plt.figure(figsize=(FIGURE_WIDTH_CM / 2.54, FIGURE_HEIGHT_CM / 2.54))
    grid = figure.add_gridspec(
        2,
        1,
        height_ratios=[3.2, 1.3],
        left=0.12,
        right=0.985,
        bottom=0.18,
        top=0.72,
        hspace=0.40,
    )
    density_axis = figure.add_subplot(grid[0])
    interval_axis = figure.add_subplot(grid[1], sharex=density_axis)

    curve_handles: list[Line2D] = []
    curve_labels: list[str] = []
    for index, eta0 in enumerate(ETA_GRID):
        color = COLORS[float(eta0)]
        line_width = 1.65 if eta0 == 0.0 else 1.4
        handle, = density_axis.plot(
            density_grid,
            densities[index],
            color=color,
            linewidth=line_width,
            solid_capstyle="round",
        )
        curve_handles.append(handle)
        model = "MV" if eta0 == 0.0 else "MVS"
        curve_labels.append(rf"{model}  ($\eta_0={eta0:g}$)")

    density_axis.set_title("A. Terminal retirement-wealth density", loc="left", pad=4.5, fontweight="bold")
    density_axis.set_ylabel("Density")
    density_axis.set_xlim(0.0, 260.0)
    density_axis.set_ylim(bottom=0.0)
    density_axis.tick_params(axis="x", labelbottom=False)
    density_axis.grid(axis="y", color="#D9DEE7", linewidth=0.55)
    density_axis.spines["top"].set_visible(False)
    density_axis.spines["right"].set_visible(False)

    row_positions = np.arange(ETA_GRID.size)[::-1]
    row_labels: list[str] = []
    for index, (eta0, row_position) in enumerate(zip(ETA_GRID, row_positions)):
        color = COLORS[float(eta0)]
        row = summary.iloc[index]
        interval_axis.hlines(row_position, row["q05"], row["q95"], color=color, linewidth=2.0)
        interval_axis.plot(
            [row["q05"], row["q95"]],
            [row_position, row_position],
            linestyle="none",
            marker="|",
            markersize=7.0,
            markeredgewidth=1.1,
            color=color,
        )
        interval_axis.scatter(row["q50"], row_position, s=14, marker="o", color=color, zorder=4)
        interval_axis.scatter(
            row["mean"],
            row_position,
            s=17,
            marker="D",
            facecolor="white",
            edgecolor=color,
            linewidth=0.9,
            zorder=5,
        )
        model = "MV" if eta0 == 0.0 else "MVS"
        row_labels.append(rf"{model}  $\eta_0={eta0:g}$")

    interval_axis.set_title("B. Central 90% range and location", loc="left", pad=3.5, fontweight="bold")
    interval_axis.set_xlabel("Terminal DC wealth")
    interval_axis.set_yticks(row_positions)
    interval_axis.set_yticklabels(row_labels)
    interval_axis.set_ylim(-0.65, 3.65)
    interval_axis.set_xticks([0, 50, 100, 150, 200, 250])
    interval_axis.grid(axis="x", color="#E4E7EC", linewidth=0.5)
    interval_axis.spines["top"].set_visible(False)
    interval_axis.spines["right"].set_visible(False)
    interval_axis.spines["left"].set_visible(False)
    interval_axis.tick_params(axis="y", length=0, pad=4)

    marker_handles = [
        Line2D([], [], color="#4D5968", marker="o", linestyle="none", markersize=4.0, label="Median"),
        Line2D(
            [],
            [],
            color="#4D5968",
            marker="D",
            markerfacecolor="white",
            linestyle="none",
            markersize=4.0,
            label="Mean",
        ),
    ]
    interval_axis.legend(
        handles=marker_handles,
        loc="lower right",
        frameon=False,
        ncol=2,
        handletextpad=0.35,
        columnspacing=0.8,
        borderaxespad=0.2,
    )

    figure.suptitle(
        "Fixed-variance-aversion MVS shifts and spreads retirement wealth",
        x=0.5,
        y=0.97,
        fontsize=9.0,
        fontweight="bold",
    )
    figure.text(
        0.5,
        0.88,
        r"dTCMV--MVS policies with $\gamma_0=2.5$; colors match the corresponding glidepaths",
        ha="center",
        va="center",
        fontsize=6.6,
        color="#4D5968",
    )
    figure.legend(
        curve_handles,
        curve_labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.835),
        ncol=4,
        frameon=False,
        handlelength=2.3,
        columnspacing=1.2,
    )
    figure.text(
        0.5,
        0.04,
        "Density: weighted Gaussian KDE with Silverman bandwidth and a state-grid resolution floor. Bars show q05--q95.",
        ha="center",
        va="center",
        fontsize=5.3,
        color="#66707D",
    )

    outputs = [output_dir / f"{STEM}.png", output_dir / f"{STEM}.svg"]
    figure.savefig(outputs[0], dpi=600, facecolor="white")
    figure.savefig(outputs[1], facecolor="white")
    plt.close(figure)

    svg_text = outputs[1].read_text(encoding="utf-8")
    cleaned_svg = "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n"
    outputs[1].write_text(cleaned_svg, encoding="utf-8")

    print("Validated fixed-gamma statistics against:", SUMMARY)
    print("KDE bandwidths:", ", ".join(f"{value:.3f}" for value in bandwidths))
    for output in outputs:
        print(output)
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot terminal distributions for the fixed-gamma dTCMV-MVS glidepaths."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for PNG and SVG output (default: supplementary/figures).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    make_figure(arguments.output_dir.resolve())
