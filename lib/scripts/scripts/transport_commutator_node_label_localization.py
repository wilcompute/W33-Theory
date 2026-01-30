#!/usr/bin/env python3
"""Localize 2T commutator norms by node and edge label."""

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
EDGES_PATH = (
    DATA
    / "_toe"
    / "projector_recon_20260110"
    / "N12_58_orbit0_edges_with_2T_connection_20260109T043900Z.csv"
)
H_TRANSPORT = (
    DATA
    / "_toe"
    / "projector_recon_20260110"
    / ("N12_58_orbit0_H_transport_59x24_sparse_20260109T205353Z.npz")
)

SELECTED = ["e*", "(0 1 2)", "(0 2 1)"]


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


def load_edge_labels():
    df = pd.read_csv(EDGES_PATH)
    label_map = {}
    for _, row in df.iterrows():
        u = int(row["u"])
        v = int(row["v"])
        key = (u, v) if u < v else (v, u)
        label_map[key] = str(row["edge_elem_2T"])
    return label_map


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


def reorder_indices(group_to_coin, nodes=59):
    perm_full = np.zeros(nodes * 24, dtype=int)
    for node in range(nodes):
        base = node * 24
        for g_idx in range(24):
            perm_full[base + g_idx] = base + group_to_coin[g_idx]
    return perm_full


def comm_row_norms(H, perm):
    H_perm = H[perm][:, perm]
    diff = H_perm - H
    row_sumsq = np.zeros(diff.shape[0], dtype=float)
    for i, v in zip(diff.nonzero()[0], diff.data):
        row_sumsq[i] += v * v
    return np.sqrt(row_sumsq)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    elems, table = load_table()
    coin_to_elem, elem_to_coin = load_mapping()
    label_map = load_edge_labels()

    coin_to_group = np.array(
        [elems.index(coin_to_elem[i]) for i in range(24)], dtype=int
    )
    group_to_coin = np.zeros_like(coin_to_group)
    for coin_idx, g_idx in enumerate(coin_to_group):
        group_to_coin[g_idx] = coin_idx

    H = load_csr_npz(H_TRANSPORT)

    # Label-decompose transport in aligned basis.
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

    perm_full_align = reorder_indices(group_to_coin)
    H_labels_aligned = {
        lab: mat.tocsr()[perm_full_align][:, perm_full_align]
        for lab, mat in H_labels.items()
    }

    rows_out = []
    for g in SELECTED:
        if g not in elems:
            continue
        perm_coin = perm_coin_for_left_action(
            elems, table, coin_to_elem, elem_to_coin, g
        )
        perm = perm_full(perm_coin)
        for lab, mat in H_labels_aligned.items():
            row_norms = comm_row_norms(mat, perm)
            for node in range(59):
                r = row_norms[node * 24 : (node + 1) * 24]
                rows_out.append(
                    {
                        "element": g,
                        "label": lab,
                        "node": node,
                        "row_norm": float(np.linalg.norm(r)),
                    }
                )

    df = pd.DataFrame(rows_out)
    df.to_csv(OUT_DIR / "transport_commutator_node_label_localization.csv", index=False)

    agg = (
        df.groupby(["label", "node"])["row_norm"]
        .mean()
        .reset_index()
        .sort_values(["label", "row_norm"], ascending=[True, False])
    )
    agg.to_csv(
        OUT_DIR / "transport_commutator_node_label_localization_summary.csv",
        index=False,
    )

    md_path = OUT_DIR / "transport_commutator_node_label_localization_summary.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Transport commutator localization by node and label\n\n")
        f.write(f"Inputs:\n- {H_TRANSPORT}\n- {EDGES_PATH}\n- {MAP_PATH}\n\n")
        for lab in labels:
            top = agg[agg["label"] == lab].head(8)
            f.write(f"## Label: {lab}\n\n")
            f.write(top.to_markdown(index=False))
            f.write("\n\n")


if __name__ == "__main__":
    main()
