#!/usr/bin/env python3
"""Quantify completion/delta contextuality vs flux response on tomotope lines."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "05_symmetry"

FLUX_SUMMARY = (
    DATA / "_toe" / "flux_response_rankings_20260110" / "line_flux_response_summary.csv"
)
LINES_CSV = (
    DATA / "_is" / "incidence_autgroup_20260110" / "incidence_12points_15lines.csv"
)
ACTION_CSV = OUT_DIR / "D6_action_on_lines_with_completion_checks.csv"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    flux = pd.read_csv(FLUX_SUMMARY)
    flux = flux.set_index("line_id")

    lines = pd.read_csv(LINES_CSV)
    lines = lines.rename(columns={"w33_rainbow_line_id": "line_id"})
    lines = lines.set_index("line_id")

    action = pd.read_csv(ACTION_CSV)
    action = action.merge(
        flux[["mean_abs_delta"]], left_on="line_id_src", right_index=True
    )
    action = action.rename(columns={"mean_abs_delta": "mean_abs_src"})
    action = action.merge(
        flux[["mean_abs_delta"]], left_on="line_id_dst", right_index=True
    )
    action = action.rename(columns={"mean_abs_delta": "mean_abs_dst"})
    action["abs_diff"] = (action["mean_abs_dst"] - action["mean_abs_src"]).abs()

    delta_pairs = []
    summary_rows = []
    for auto_id, grp in action.groupby("auto_id"):
        pairs = {}
        for _, row in grp.iterrows():
            a = int(row["line_id_src"])
            b = int(row["line_id_dst"])
            key = tuple(sorted((a, b)))
            if key not in pairs:
                pairs[key] = row
        diffs = [float(r["abs_diff"]) for r in pairs.values()]
        summary_rows.append(
            {
                "auto_id": int(auto_id),
                "delta": int(grp["delta"].iloc[0]),
                "pair_count": len(diffs),
                "mean_abs_diff": sum(diffs) / len(diffs) if diffs else 0.0,
                "median_abs_diff": float(pd.Series(diffs).median()) if diffs else 0.0,
                "max_abs_diff": max(diffs) if diffs else 0.0,
            }
        )
        for (a, b), r in pairs.items():
            delta_pairs.append(
                {
                    "auto_id": int(auto_id),
                    "delta": int(r["delta"]),
                    "line_a": a,
                    "line_b": b,
                    "abs_diff_mean_abs_delta": float(r["abs_diff"]),
                }
            )

    summary_df = pd.DataFrame(summary_rows).sort_values(["delta", "auto_id"])
    pair_df = pd.DataFrame(delta_pairs).sort_values(
        ["delta", "abs_diff_mean_abs_delta"], ascending=[True, False]
    )
    summary_df.to_csv(OUT_DIR / "contextuality_delta_pair_summary.csv", index=False)
    pair_df.to_csv(OUT_DIR / "contextuality_delta_pair_differences.csv", index=False)

    # Missing-sector and completion stats on tomotope lines.
    meta = lines.join(flux, how="left")
    miss_stats = (
        meta.groupby("missing_sector")["mean_abs_delta"]
        .agg(["count", "mean", "median"])
        .reset_index()
    )
    comp_stats = (
        meta.groupby("completion_class")["mean_abs_delta"]
        .agg(["count", "mean", "median"])
        .reset_index()
    )
    miss_stats.to_csv(OUT_DIR / "contextuality_missing_sector_stats.csv", index=False)
    comp_stats.to_csv(OUT_DIR / "contextuality_completion_class_stats.csv", index=False)

    md_path = OUT_DIR / "contextuality_delta_completion_summary.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Contextuality: delta homomorphism vs completion decoration\n\n")
        f.write(f"Inputs:\n- {FLUX_SUMMARY}\n- {LINES_CSV}\n- {ACTION_CSV}\n\n")
        f.write("Delta-pair differences by automorphism:\n\n")
        f.write(summary_df.to_markdown(index=False))
        f.write("\n\nMissing-sector stats (tomotope lines):\n\n")
        f.write(miss_stats.to_markdown(index=False))
        f.write("\n\nCompletion-class stats (tomotope lines):\n\n")
        f.write(comp_stats.to_markdown(index=False))


if __name__ == "__main__":
    main()
