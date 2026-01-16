#!/usr/bin/env python3
"""Structured automorphism search: Aut(2T,S) with left multiplications."""

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
ORDERS_PATH = DATA / "_toe" / "projector_recon_20260110" / "binary_tetrahedral_2T_element_orders.csv"
H_TRANSPORT = DATA / "_toe" / "projector_recon_20260110" / (
    "N12_58_orbit0_H_transport_59x24_sparse_20260109T205353Z.npz"
)

G1 = "(0 1)(2 3)"
G2 = "(0 1 2)"
S_SET = {"e*", "(0 1)(2 3)", "(0 1)(2 3)*"}


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


def load_orders():
    orders = {}
    with ORDERS_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            orders[row["element"]] = int(row["order"])
    return orders


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


def generate_mapping(elems, table, g1, g2, a, b):
    # Homomorphism from generators g1->a, g2->b
    f = {"e": "e", g1: a, g2: b}
    queue = ["e"]
    gens = [g1, g2]
    while queue:
        x = queue.pop(0)
        for g in gens:
            y = table[(x, g)]
            fx = f[x]
            fg = f[g]
            fy = table[(fx, fg)]
            if y in f:
                if f[y] != fy:
                    return None
            else:
                f[y] = fy
                queue.append(y)
    if len(f) != len(elems):
        return None
    # bijection check
    if len(set(f.values())) != len(elems):
        return None
    # homomorphism check
    for x in elems:
        for y in elems:
            if f[table[(x, y)]] != table[(f[x], f[y])]:
                return None
    return f


def automorphisms_preserving_S(elems, table, orders):
    order4 = [e for e in elems if orders[e] == 4]
    order6 = [e for e in elems if orders[e] == 6]
    autos = []
    for a in order4:
        for b in order6:
            f = generate_mapping(elems, table, G1, G2, a, b)
            if f is None:
                continue
            if {f[s] for s in S_SET} != S_SET:
                continue
            autos.append(f)
    if not autos:
        identity = {e: e for e in elems}
        if {identity[s] for s in S_SET} == S_SET:
            autos.append(identity)
    return autos


def perm_coin_from_mapping(f, coin_to_elem, elem_to_coin):
    perm = np.zeros(24, dtype=int)
    for i in range(24):
        perm[i] = elem_to_coin[f[coin_to_elem[i]]]
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
    orders = load_orders()
    coin_to_elem, elem_to_coin = load_mapping()
    autos = automorphisms_preserving_S(elems, table, orders)

    H = load_csr_npz(H_TRANSPORT)

    rows = []
    # automorphisms alone
    for idx, f in enumerate(autos):
        perm_coin = perm_coin_from_mapping(f, coin_to_elem, elem_to_coin)
        perm = perm_full(perm_coin)
        rows.append(
            {
                "kind": "auto",
                "auto_index": idx,
                "left_elem": "e",
                "comm_norm": comm_norm_by_perm(H, perm),
            }
        )
    # left multiplication combined with automorphisms
    for left in elems:
        for idx, f in enumerate(autos):
            perm_coin = np.zeros(24, dtype=int)
            for i in range(24):
                x = coin_to_elem[i]
                y = table[(left, f[x])]
                perm_coin[i] = elem_to_coin[y]
            perm = perm_full(perm_coin)
            rows.append(
                {
                    "kind": "left_auto",
                    "auto_index": idx,
                    "left_elem": left,
                    "comm_norm": comm_norm_by_perm(H, perm),
                }
            )

    if rows:
        df = pd.DataFrame(rows).sort_values("comm_norm")
    else:
        df = pd.DataFrame(columns=["kind", "auto_index", "left_elem", "comm_norm"])
    df.to_csv(OUT_DIR / "transport_structured_autgroup_commutators.csv", index=False)

    summary_path = OUT_DIR / "transport_structured_autgroup_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# Structured automorphisms (Aut(2T,S) with left multiplications)\n\n")
        f.write(f"Automorphisms preserving S: {len(autos)}\n\n")
        f.write("Top 10 smallest commutators:\n\n")
        if df.empty:
            f.write("- none\n")
        else:
            f.write(df.head(10).to_markdown(index=False))


if __name__ == "__main__":
    main()
