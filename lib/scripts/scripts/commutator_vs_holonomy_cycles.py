#!/usr/bin/env python3
"""Relate commutator localization to holonomy cycle membership."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "05_symmetry"

COMM_NODE = OUT_DIR / "transport_commutator_node_localization_summary.csv"
CYCLES = DATA / "_workbench" / "04_measurement" / "sage_zip_continuation_20260111" / "nontrivial_holonomy_cycles_catalog.csv"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    comm = pd.read_csv(COMM_NODE)
    cycles = pd.read_csv(CYCLES)

    counts = {i: 0 for i in range(59)}
    lengths = {i: 0 for i in range(59)}
    for _, row in cycles.iterrows():
        nodes = [int(x) for x in str(row["cycle_nodes"]).split("-")]
        for n in nodes:
            counts[n] += 1
            lengths[n] += int(row["length"])

    comm["cycle_count"] = comm["node"].map(counts)
    comm["cycle_length_sum"] = comm["node"].map(lengths)

    corr_count = comm["mean"].corr(comm["cycle_count"])
    corr_len = comm["mean"].corr(comm["cycle_length_sum"])
    spearman_count = comm["mean"].corr(comm["cycle_count"], method="spearman")
    spearman_len = comm["mean"].corr(comm["cycle_length_sum"], method="spearman")

    comm.sort_values("mean", ascending=False).to_csv(
        OUT_DIR / "commutator_vs_holonomy_nodes.csv", index=False
    )

    summary_path = OUT_DIR / "commutator_vs_holonomy_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# Commutator localization vs holonomy cycles\n\n")
        f.write(f"Inputs:\n- {COMM_NODE}\n- {CYCLES}\n\n")
        f.write(f"- corr(mean, cycle_count): {corr_count:.6f}\n")
        f.write(f"- corr(mean, cycle_length_sum): {corr_len:.6f}\n")
        f.write(f"- spearman(mean, cycle_count): {spearman_count:.6f}\n")
        f.write(f"- spearman(mean, cycle_length_sum): {spearman_len:.6f}\n\n")
        f.write("Top 10 nodes by commutator mean:\n\n")
        f.write(comm.sort_values("mean", ascending=False).head(10).to_markdown(index=False))


if __name__ == "__main__":
    main()
