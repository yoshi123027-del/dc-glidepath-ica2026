from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d


ROOT = Path(__file__).resolve().parents[2]
ARRAYS = ROOT / "results" / "monthly_D0_policy_arrays.npz"
SUMMARY = ROOT / "results" / "monthly_baseline_D0_summary.csv"
DEFAULT_OUTPUT_DIR = ROOT / "supplementary" / "figures"
STEM = "fig_all_strategies_terminal_density_D0_N480"
STEM_WITHOUT_CP = "fig_four_strategies_terminal_density_D0_N480"

FIGURE_WIDTH_INCHES = 9.2
FIGURE_HEIGHT_INCHES = 5.6
PNG_DPI = 180
DENSITY_GRID = np.linspace(0.0, 220.0, 1000)
COLORS = {
    "PCMV": "#1F77B4",
    "DOMV": "#FF7F0E",
    "cTCMV": "#2CA02C",
    "dTCMV": "#D62728",
    "CP": "#9467BD",
}
SERIES = (
    ("PCMV", "xg_pc", "pcmv_pmf"),
    ("DOMV", "xg_pc", "domv_pmf"),
    ("cTCMV", "xg_tc", "ctcmv_pmf"),
    ("dTCMV", "xg_tc", "dtcmv_pmf"),
    ("CP", "xg_tc", "cp_pmf"),
)


def deposit_uniform(values: np.ndarray, probabilities: np.ndarray) -> np.ndarray:
    """Deposit discrete probability mass on the density grid by linear interpolation."""
    mass = np.zeros_like(DENSITY_GRID)
    spacing = DENSITY_GRID[1] - DENSITY_GRID[0]
    for value, probability in zip(values, probabilities):
        if probability <= 0.0:
            continue
        coordinate = (value - DENSITY_GRID[0]) / spacing
        if coordinate <= 0.0:
            mass[0] += probability
        elif coordinate >= len(DENSITY_GRID) - 1:
            mass[-1] += probability
        else:
            left = int(np.floor(coordinate))
            weight_right = coordinate - left
            mass[left] += probability * (1.0 - weight_right)
            mass[left + 1] += probability * weight_right
    return mass


def discrete_quantile(values: np.ndarray, probabilities: np.ndarray, q: float) -> float:
    normalized = probabilities / probabilities.sum()
    index = min(np.searchsorted(np.cumsum(normalized), q), len(values) - 1)
    return float(values[index])


def validate_summary(
    distributions: dict[str, tuple[np.ndarray, np.ndarray]],
    summary: pd.DataFrame,
) -> pd.DataFrame:
    expected_order = [item[0] for item in SERIES]
    indexed = summary.set_index("strategy").loc[expected_order]
    for strategy, (values, probabilities) in distributions.items():
        probabilities = probabilities / probabilities.sum()
        calculated = {
            "mean": float(probabilities @ values),
            "q05": discrete_quantile(values, probabilities, 0.05),
            "q50": discrete_quantile(values, probabilities, 0.50),
            "q95": discrete_quantile(values, probabilities, 0.95),
        }
        for statistic, value in calculated.items():
            if not np.isclose(value, indexed.loc[strategy, statistic], atol=5e-6):
                raise ValueError(
                    f"Recomputed {statistic} for {strategy} does not match {SUMMARY}."
                )
    return indexed


def load_inputs() -> tuple[dict[str, tuple[np.ndarray, np.ndarray]], pd.DataFrame]:
    with np.load(ARRAYS) as arrays:
        distributions = {
            strategy: (
                np.asarray(arrays[grid_key], dtype=float).copy(),
                np.asarray(arrays[pmf_key][-1], dtype=float).copy(),
            )
            for strategy, grid_key, pmf_key in SERIES
        }
    summary = validate_summary(distributions, pd.read_csv(SUMMARY))
    return distributions, summary


def make_figure(output_dir: Path, exclude_cp: bool = False) -> list[Path]:
    distributions, summary = load_inputs()
    output_dir.mkdir(parents=True, exist_ok=True)
    active_series = tuple(item for item in SERIES if not (exclude_cp and item[0] == "CP"))

    figure = plt.figure(figsize=(FIGURE_WIDTH_INCHES, FIGURE_HEIGHT_INCHES))
    layout = figure.add_gridspec(2, 1, height_ratios=[3.2, 1.25], hspace=0.12)
    density_axis = figure.add_subplot(layout[0])
    interval_axis = figure.add_subplot(layout[1], sharex=density_axis)

    for strategy, _, _ in active_series:
        values, probabilities = distributions[strategy]
        probabilities = probabilities / probabilities.sum()
        mass = deposit_uniform(values, probabilities)
        density = gaussian_filter1d(mass, sigma=5, mode="nearest") / (
            DENSITY_GRID[1] - DENSITY_GRID[0]
        )
        density_axis.plot(DENSITY_GRID, density, color=COLORS[strategy], label=strategy)

    density_axis.set_ylabel("Smoothed density")
    density_axis.set_xlim(0.0, 220.0)
    density_axis.set_ylim(bottom=0.0)
    density_axis.tick_params(axis="x", labelbottom=False)
    density_axis.grid(alpha=0.25)
    density_axis.legend(ncol=2 if exclude_cp else 3, loc="upper right")

    strategies = [item[0] for item in active_series]
    row_positions = np.arange(len(strategies))[::-1]
    for strategy, row_position in zip(strategies, row_positions):
        row = summary.loc[strategy]
        color = COLORS[strategy]
        interval_axis.hlines(
            row_position,
            row["q05"],
            row["q95"],
            color=color,
            linewidth=2.0,
        )
        interval_axis.plot(
            [row["q05"], row["q95"]],
            [row_position, row_position],
            linestyle="none",
            marker="|",
            markersize=7.0,
            markeredgewidth=1.1,
            color=color,
        )
        interval_axis.scatter(
            row["q50"],
            row_position,
            s=14,
            marker="o",
            color=color,
            zorder=4,
        )
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

    interval_axis.set_xlabel("Terminal DC wealth")
    interval_axis.set_yticks(row_positions)
    interval_axis.set_yticklabels(strategies)
    interval_axis.set_ylim(-0.65, len(strategies) - 0.35)
    interval_axis.set_xticks([0, 25, 50, 75, 100, 125, 150, 175, 200])
    interval_axis.grid(alpha=0.25)
    interval_axis.legend(
        handles=[
            Line2D(
                [],
                [],
                color="#4D5968",
                linewidth=2.0,
                marker="|",
                markersize=7.0,
                label="q05-q95",
            ),
            Line2D(
                [],
                [],
                color="#4D5968",
                marker="o",
                linestyle="none",
                markersize=4.0,
                label="Median",
            ),
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
        ],
        loc="upper right",
        frameon=True,
        ncol=3,
        handletextpad=0.35,
        columnspacing=0.8,
        borderaxespad=0.4,
    )
    figure.subplots_adjust(left=0.11, right=0.98, bottom=0.13, top=0.98, hspace=0.08)

    output_stem = STEM_WITHOUT_CP if exclude_cp else STEM
    outputs = [output_dir / f"{output_stem}.png", output_dir / f"{output_stem}.svg"]
    figure.savefig(outputs[0], dpi=PNG_DPI, facecolor="white")
    figure.savefig(outputs[1], facecolor="white")
    plt.close(figure)

    svg_text = outputs[1].read_text(encoding="utf-8")
    outputs[1].write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )

    print("Validated distribution statistics against:", SUMMARY)
    for output in outputs:
        print(output)
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot baseline terminal densities and distribution statistics for all strategies."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for PNG and SVG output (default: supplementary/figures).",
    )
    parser.add_argument(
        "--exclude-cp",
        action="store_true",
        help="Create a presentation version containing PCMV, DOMV, cTCMV, and dTCMV only.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    make_figure(arguments.output_dir.resolve(), exclude_cp=arguments.exclude_cp)
