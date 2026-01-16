#!/usr/bin/env python3
"""Decompose transport symmetry breaking by edge label under 2T left action."""

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
EDGES_PATH = DATA / "_toe" / "projector_recon_20260110" / "N12_58_orbit0_edges_with_2T_connection_20260109T043900Z.csv"
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
    elem_to_coin = {v: k for k, v in coin_to_elem.items()}
    return coin_to_elem, elem_to_coin


def load_csr_npz(path: Path) -> sp.csr_matrix:
    z = np.load(path, allow_pickle=True)
    return sp.csr_matrix((z["data"], z["indices"], z["indptr"]), shape=tuple(z["shape"]))


def load_edge_labels():
    df = pd.read_csv(EDGES_PATH)
    label_map = {}
    for _, row in df.iterrows():
        u = int(row["u"])
        v = int(row["v"])
        key = (u, v) if u < v else (v, u)
        label_map[key] = str(row["edge_elem_2T"])
    return label_map


def reorder_indices(group_to_coin, nodes=59):
    perm_full = np.zeros(nodes * 24, dtype=int)
    for node in range(nodes):
        base = node * 24
        for g_idx in range(24):
            perm_full[base + g_idx] = base + group_to_coin[g_idx]
    return perm_full


def left_perm_group(elems, table, g):
    idx = {e: i for i, e in enumerate(elems)}
    perm = np.zeros(len(elems), dtype=int)
    for i, e in enumerate(elems):
        perm[i] = idx[table[(g, e)]]
    return perm


def perm_full_from_group(perm_group, nodes=59):
    perm = np.zeros(nodes * len(perm_group), dtype=int)
    for node in range(nodes):
        base = node * len(perm_group)
        for i, j in enumerate(perm_group):
            perm[base + i] = base + j
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
    label_map = load_edge_labels()

    coin_to_group = np.array([elems.index(coin_to_elem[i]) for i in range(24)], dtype=int)
    group_to_coin = np.zeros_like(coin_to_group)
    for coin_idx, g_idx in enumerate(coin_to_group):
        group_to_coin[g_idx] = coin_idx

    H = load_csr_npz(H_TRANSPORT)

    # Build label-decomposed transport in current basis.
    labels = sorted(set(label_map.values()))
    H_labels = {lab: sp.dok_matrix(H.shape, dtype=float) for lab in labels}
    rows, cols = H.nonzero()
    for i, j, v in zip(rows, cols, H.data):
        u = i // 24
        v_node = j // 24
        if u == v_node:
            continue
        key = (u, v_node) if u < v_node else (v_node, u)
        label = label_map.get(key)
        if label is None:
            continue
        H_labels[label][i, j] = v

    # Reorder to group basis.
    perm_full = reorder_indices(group_to_coin)
    H_labels_aligned = {lab: mat.tocsr()[perm_full][:, perm_full] for lab, mat in H_labels.items()}
    H_total_aligned = sum(H_labels_aligned.values())

    # Commutator norms by label and element.
    rows = []
    for g in elems:
        perm_group = left_perm_group(elems, table, g)
        perm = perm_full_from_group(perm_group)
        total_norm = comm_norm_by_perm(H_total_aligned, perm)
        for lab, mat in H_labels_aligned.items():
            rows.append(
                {
                    "element": g,
                    "label": lab,
                    "comm_norm": comm_norm_by_perm(mat, perm),
                    "comm_norm_total": total_norm,
                }
            )

    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / "transport_symmetry_breaking_by_label.csv", index=False)

    # Aggregate by label (exclude identity).
    df_non_id = df[df["element"] != "e"]
    agg = (
        df_non_id.groupby("label")["comm_norm"]
        .agg(["mean", "median", "max"])
        .reset_index()
        .sort_values("mean", ascending=False)
    )
    agg.to_csv(OUT_DIR / "transport_symmetry_breaking_by_label_summary.csv", index=False)

    md_path = OUT_DIR / "transport_symmetry_breaking_by_label_summary.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Transport symmetry breaking by edge label\n\n")
        f.write(f"Inputs:\n- {H_TRANSPORT}\n- {EDGES_PATH}\n- {MAP_PATH}\n\n")
        f.write("Aggregate commutator norms (non-identity elements):\n\n")
        f.write(agg.to_markdown(index=False))


if __name__ == "__main__":
    main()
