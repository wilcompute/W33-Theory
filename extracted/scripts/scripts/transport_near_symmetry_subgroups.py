#!/usr/bin/env python3
"""Enumerate near-symmetry subgroups of 2T under transport commutator norms."""

from __future__ import annotations

import csv
import itertools
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "05_symmetry"

TABLE_PATH = DATA / "_toe" / "projector_recon_20260110" / "binary_tetrahedral_2T_multiplication_table.csv"
COMM_PATH = OUT_DIR / "coin_c24_2t_fullH_equivariance.csv"


def load_table():
    with TABLE_PATH.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        elems = [h.strip() for h in header[1:] if h.strip()]
        table = {}
        for row in reader:
            row_elem = row[0].strip()
            for col_elem, prod in zip(elems, row[1:]):
                table[(row_elem, col_elem)] = prod.strip()
    return elems, table


def inverse_map(elems, table):
    inv = {}
    for a in elems:
        for b in elems:
            if table[(a, b)] == "e":
                inv[a] = b
                break
    return inv


def subgroup_generated(gens, elems, table, inv):
    S = set(["e"])
    for g in gens:
        S.add(g)
        S.add(inv[g])
    changed = True
    while changed:
        changed = False
        for a in list(S):
            for b in list(S):
                c = table[(a, b)]
                if c not in S:
                    S.add(c)
                    changed = True
    return frozenset(S)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    elems, table = load_table()
    inv = inverse_map(elems, table)
    comm = pd.read_csv(COMM_PATH).set_index("element")
    comm_map = comm["comm_norm_transport"].to_dict()

    subgroups = {}
    for r in (1, 2):
        for gens in itertools.combinations(elems, r):
            S = subgroup_generated(gens, elems, table, inv)
            if S in subgroups:
                continue
            norms = [comm_map[g] for g in S]
            subgroups[S] = {
                "order": len(S),
                "generators": " ".join(gens),
                "max_comm": max(norms),
                "mean_comm": float(np.mean(norms)),
            }

    rows = []
    for S, info in subgroups.items():
        rows.append(
            {
                "order": info["order"],
                "generators": info["generators"],
                "max_comm": info["max_comm"],
                "mean_comm": info["mean_comm"],
                "elements": " ".join(sorted(S)),
            }
        )
    df = pd.DataFrame(rows).sort_values(["max_comm", "order"], ascending=[True, False])
    df.to_csv(OUT_DIR / "transport_near_symmetry_subgroups.csv", index=False)

    best = (
        df.sort_values(["order", "max_comm"], ascending=[False, True])
        .groupby("order")
        .head(1)
        .sort_values("order")
    )
    best.to_csv(OUT_DIR / "transport_near_symmetry_subgroups_best.csv", index=False)

    md_path = OUT_DIR / "transport_near_symmetry_subgroups_summary.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Near-symmetry subgroups under transport commutator norms\n\n")
        f.write(f"Inputs:\n- {COMM_PATH}\n- {TABLE_PATH}\n\n")
        f.write("Best subgroup per order (min max_comm):\n\n")
        f.write(best[["order", "generators", "max_comm", "mean_comm"]].to_markdown(index=False))
        f.write("\n\nTop 8 subgroups overall:\n\n")
        f.write(df.head(8)[["order", "generators", "max_comm", "mean_comm"]].to_markdown(index=False))


if __name__ == "__main__":
    main()
