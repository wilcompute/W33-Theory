#!/usr/bin/env python3
"""Check full-H equivariance under 2T left action using coin->element mapping."""

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
TABLE_PATH = (
    DATA
    / "_toe"
    / "projector_recon_20260110"
    / "binary_tetrahedral_2T_multiplication_table.csv"
)
H_TOTAL = (
    DATA
    / "_toe"
    / "projector_recon_20260110"
    / ("TOE_H_total_transport_plus_lambda_coin_59x24_lam0.5_20260109T205353Z.npz")
)
H_TRANSPORT = (
    DATA
    / "_toe"
    / "projector_recon_20260110"
    / ("N12_58_orbit0_H_transport_59x24_sparse_20260109T205353Z.npz")
)
COIN_NPZ = (
    DATA
    / "_toe"
    / "projector_recon_20260110"
    / ("N12_58_sector_coin_C24_K4_by_k_sparse_20260109T205353Z.npz")
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
    elem_to_coin = {v: k for k, v in coin_to_elem.items()}
    return coin_to_elem, elem_to_coin


def load_csr_npz(path: Path) -> sp.csr_matrix:
    z = np.load(path, allow_pickle=True)
    return sp.csr_matrix(
        (z["data"], z["indices"], z["indptr"]), shape=tuple(z["shape"])
    )


def perm_coin_for_left_action(elems, table, coin_to_elem, elem_to_coin, g):
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
    coin_to_elem, elem_to_coin = load_mapping()

    H_total = load_csr_npz(H_TOTAL)
    H_transport = load_csr_npz(H_TRANSPORT)
    coin = load_csr_npz(COIN_NPZ)
    coin_block = sp.kron(sp.eye(59, format="csr"), coin, format="csr")

    rows = []
    for g in elems:
        perm_coin = perm_coin_for_left_action(
            elems, table, coin_to_elem, elem_to_coin, g
        )
        perm = perm_full(perm_coin)
        rows.append(
            {
                "element": g,
                "comm_norm_coin": comm_norm_by_perm(coin_block, perm),
                "comm_norm_transport": comm_norm_by_perm(H_transport, perm),
                "comm_norm_total": comm_norm_by_perm(H_total, perm),
            }
        )

    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / "coin_c24_2t_fullH_equivariance.csv", index=False)

    zero_rows = df[df["comm_norm_total"] == 0.0]
    summary_path = OUT_DIR / "coin_c24_2t_fullH_equivariance_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# Full-H equivariance under 2T (left action)\n\n")
        f.write(
            f"Inputs:\n- {H_TOTAL}\n- {H_TRANSPORT}\n- {COIN_NPZ}\n- {MAP_PATH}\n\n"
        )
        f.write("Elements with zero commutator (full H):\n\n")
        if zero_rows.empty:
            f.write("- none\n")
        else:
            f.write(zero_rows[["element"]].to_markdown(index=False))
        f.write("\n\nTop 6 smallest commutators (full H):\n\n")
        f.write(df.sort_values("comm_norm_total").head(6).to_markdown(index=False))


if __name__ == "__main__":
    main()
