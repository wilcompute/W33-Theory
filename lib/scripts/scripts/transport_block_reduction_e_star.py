#!/usr/bin/env python3
"""Approximate block reduction of H_transport using e* (order-2) action."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh

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
H_TRANSPORT = (
    DATA
    / "_toe"
    / "projector_recon_20260110"
    / ("N12_58_orbit0_H_transport_59x24_sparse_20260109T205353Z.npz")
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


def e_star_pairs(table, coin_to_elem, elem_to_coin):
    pairs = []
    seen = set()
    for i in range(24):
        if i in seen:
            continue
        elem = coin_to_elem[i]
        prod = table[("e*", elem)]
        j = elem_to_coin[prod]
        if i == j:
            raise RuntimeError("Fixed point under e* action.")
        seen.add(i)
        seen.add(j)
        a, b = (i, j) if i < j else (j, i)
        pairs.append((a, b))
    pairs.sort()
    return pairs


def build_T_even_odd(pairs):
    n_pairs = len(pairs)
    rows_even = []
    cols_even = []
    data_even = []
    rows_odd = []
    cols_odd = []
    data_odd = []
    for k, (i, j) in enumerate(pairs):
        val = 1.0 / math.sqrt(2.0)
        # Even column k
        rows_even.extend([i, j])
        cols_even.extend([k, k])
        data_even.extend([val, val])
        # Odd column k
        rows_odd.extend([i, j])
        cols_odd.extend([k, k])
        data_odd.extend([val, -val])
    T_even = sp.csr_matrix((data_even, (rows_even, cols_even)), shape=(24, n_pairs))
    T_odd = sp.csr_matrix((data_odd, (rows_odd, cols_odd)), shape=(24, n_pairs))
    return T_even, T_odd


def fro_norm_sparse(m: sp.spmatrix) -> float:
    if m.nnz == 0:
        return 0.0
    return float(np.linalg.norm(m.data))


def top_eigs(mat: sp.spmatrix, k=10):
    k = min(k, mat.shape[0] - 2)
    vals = eigsh(mat, k=k, which="LM", return_eigenvectors=False)
    vals = np.sort(vals)[::-1]
    return vals


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    elems, table = load_table()
    coin_to_elem, elem_to_coin = load_mapping()
    pairs = e_star_pairs(table, coin_to_elem, elem_to_coin)
    T_even, T_odd = build_T_even_odd(pairs)

    H = load_csr_npz(H_TRANSPORT)
    I59 = sp.eye(59, format="csr")
    Ke = sp.kron(I59, T_even, format="csr")
    Ko = sp.kron(I59, T_odd, format="csr")

    H_even = Ke.T @ H @ Ke
    H_odd = Ko.T @ H @ Ko
    H_off = Ke.T @ H @ Ko

    off_ratio = (
        fro_norm_sparse(H_off) / fro_norm_sparse(H) if fro_norm_sparse(H) else 0.0
    )

    eig_full = top_eigs(H, k=10)
    eig_even = top_eigs(H_even, k=10)
    eig_odd = top_eigs(H_odd, k=10)

    eig_rows = []
    for name, vals in [("full", eig_full), ("even", eig_even), ("odd", eig_odd)]:
        for i, v in enumerate(vals):
            eig_rows.append({"block": name, "eig_index": i + 1, "eig_value": float(v)})

    eig_df = pd.DataFrame(eig_rows)
    eig_df.to_csv(OUT_DIR / "transport_e_star_block_eigs.csv", index=False)

    summary_path = OUT_DIR / "transport_e_star_block_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# Transport block reduction by e* action\n\n")
        f.write(f"Inputs:\n- {H_TRANSPORT}\n- {MAP_PATH}\n- {TABLE_PATH}\n\n")
        f.write(f"- off-block ratio: {off_ratio:.6e}\n\n")
        f.write("Top eigenvalues (k=10):\n\n")
        f.write(
            eig_df.pivot(
                index="eig_index", columns="block", values="eig_value"
            ).to_markdown()
        )


if __name__ == "__main__":
    main()
