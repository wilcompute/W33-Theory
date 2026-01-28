#!/usr/bin/env python3
"""Summarize holonomy localization of difference modes by cycles and nodes."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "04_measurement"

MODE_SUMMARY = (
    OUT_DIR
    / "sage_zip_continuation_20260111"
    / "keypoint_lam0p5_mu1p25_difference_modes_summary.csv"
)
CYCLE_CATALOG = (
    OUT_DIR
    / "sage_zip_continuation_20260111"
    / "nontrivial_holonomy_cycles_catalog.csv"
)
DEFECT_EDGES = (
    DATA / "_toe" / "geometric_reduction_20260110" / "orbit0_edges_Z2_cocycle.csv"
)
NODE_SIG = DATA / "_workbench" / "05_symmetry" / "orbit0_node_transport_signature.csv"


def parse_top_nodes(s: str):
    nodes = []
    for chunk in s.split(";"):
        if not chunk.strip():
            continue
        node_str, w_str = chunk.split(":")
        nodes.append((int(node_str), float(w_str)))
    return nodes


def load_defect_nodes():
    defect = set()
    with DEFECT_EDGES.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["is_defect"]) == 1:
                defect.add(int(row["u"]))
                defect.add(int(row["v"]))
    return defect


def load_degrees():
    df = pd.read_csv(NODE_SIG)
    return {int(r["node"]): int(r["degree"]) for _, r in df.iterrows()}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    modes = pd.read_csv(MODE_SUMMARY)
    cycles = pd.read_csv(CYCLE_CATALOG)
    cycle_meta = {
        int(r["cycle_id"]): (int(r["length"]), str(r["holonomy"]))
        for _, r in cycles.iterrows()
    }
    defect_nodes = load_defect_nodes()
    degrees = load_degrees()

    node_rows = []
    summary_rows = []
    for _, row in modes.iterrows():
        mode_k = int(row["mode_k"])
        top_nodes = parse_top_nodes(str(row["top_nodes"]))
        total_w = sum(w for _, w in top_nodes) or 1.0
        defect_w = sum(w for n, w in top_nodes if n in defect_nodes)
        avg_degree = sum(degrees.get(n, 0) * w for n, w in top_nodes) / total_w
        defect_frac = defect_w / total_w

        for n, w in top_nodes:
            node_rows.append(
                {
                    "mode_k": mode_k,
                    "node": n,
                    "weight": w,
                    "is_defect_adjacent": int(n in defect_nodes),
                    "degree": degrees.get(n, 0),
                }
            )

        top_cycle = int(row["top_cycle_id_by_mass"])
        second_cycle = int(row["second_cycle_id"])
        t_len, t_hol = cycle_meta.get(top_cycle, (None, None))
        s_len, s_hol = cycle_meta.get(second_cycle, (None, None))
        summary_rows.append(
            {
                "mode_k": mode_k,
                "top_cycle_id": top_cycle,
                "top_cycle_len": t_len,
                "top_cycle_holonomy": t_hol,
                "second_cycle_id": second_cycle,
                "second_cycle_len": s_len,
                "second_cycle_holonomy": s_hol,
                "defect_weight_frac_top_nodes": defect_frac,
                "weighted_avg_degree_top_nodes": avg_degree,
            }
        )

    node_df = pd.DataFrame(node_rows)
    node_df.to_csv(OUT_DIR / "holonomy_localization_node_weights.csv", index=False)

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUT_DIR / "holonomy_localization_summary.csv", index=False)

    md_path = OUT_DIR / "holonomy_localization_summary.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Holonomy localization (lambda=0.5, mu=1.25)\n\n")
        f.write(f"Inputs:\n- {MODE_SUMMARY}\n- {CYCLE_CATALOG}\n- {DEFECT_EDGES}\n\n")
        f.write(summary_df.to_markdown(index=False))


if __name__ == "__main__":
    main()
