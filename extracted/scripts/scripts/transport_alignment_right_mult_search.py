#!/usr/bin/env python3
"""Search right-multiplication relabelings to improve transport equivariance."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "05_symmetry"

MAP_PATH = OUT_DIR / "coin_c24_2t_alignment_mapping.csv"
TABLE_PATH = DATA / "_toe" / "projector_recon_20260110" / "binary_tetrahedral_2T_multiplication_table.csv"
H_TRANSPORT = DATA / "_toe" / "projector_recon_20260110" / (
    "N12_58_orbit0_H_transport_59x24_sparse_20260109T205353Z.npz"
)


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


def load_mapping():
    coin_to_elem = {}
    with MAP_PATH.open("r", encoding="utf-8") as f:
        next(f)
        for line in f:
            idx, label = line.strip().split(",")
            coin_to_elem[int(idx)] = label
    return coin_to_elem


def load_csr_npz(path: Path) -> sp.csr_matrix:
    z = np.load(path, allow_pickle=True)
    return sp.csr_matrix((z["data"], z["indices"], z["indptr"]), shape=tuple(z["shape"]))


def perm_coin_for_left_action(elems, table, coin_to_elem, g):
    elem_to_coin = {v: k for k, v in coin_to_elem.items()}
    perm = np.zeros(24, dtype=int)
    for i in range(24):
        elem = coin_to_elem[i]
        prod = table[(g, elem)]
        perm[i] = elem_to_coin[prod]
    return perm


def perm_full(perm_coin, nodes=59):
    perm = np.zeros(nodes * 24, dtype=int)
    for node in range(nodes):
        base = node * 24
        for i in range(24):
            perm[base + i] = base + perm_coin[i]
    return perm


def comm_norm_by_perm(H, perm):
    H_perm = H[perm][:, perm]
    diff = H_perm - H
    if diff.nnz == 0:
        return 0.0
    return float(np.linalg.norm(diff.data))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    elems, table = load_table()
    base_coin_to_elem = load_mapping()
    H = load_csr_npz(H_TRANSPORT)

    rows = []
    for h in elems:
        # Right-multiply mapping by h.
        coin_to_elem = {
            i: table[(base_coin_to_elem[i], h)] for i in range(24)
        }
        comms = {}
        for g in elems:
            perm_coin = perm_coin_for_left_action(elems, table, coin_to_elem, g)
            perm = perm_full(perm_coin)
            comms[g] = comm_norm_by_perm(H, perm)

        non_id = [v for k, v in comms.items() if k != "e"]
        rows.append(
            {
                "right_mult": h,
                "max_comm": max(non_id),
                "mean_comm": float(np.mean(non_id)),
                "comm_e_star": comms.get("e*", 0.0),
                "comm_012": comms.get("(0 1 2)", 0.0),
                "comm_021": comms.get("(0 2 1)", 0.0),
            }
        )

    df = pd.DataFrame(rows).sort_values(["max_comm", "mean_comm"])
    df.to_csv(OUT_DIR / "transport_alignment_right_mult_search.csv", index=False)

    best = df.head(6).copy()
    summary_path = OUT_DIR / "transport_alignment_right_mult_search_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# Right-multiplication alignment search (transport)\n\n")
        f.write(f"Inputs:\n- {H_TRANSPORT}\n- {MAP_PATH}\n- {TABLE_PATH}\n\n")
        f.write("Top 6 relabelings by max_comm:\n\n")
        f.write(best.to_markdown(index=False))


if __name__ == "__main__":
    main()
