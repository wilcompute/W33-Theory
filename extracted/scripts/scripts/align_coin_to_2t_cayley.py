#!/usr/bin/env python3
"""Align C24 coin ordering to a 2T Cayley graph (searching for a labeling)."""

from __future__ import annotations

import csv
import itertools
from pathlib import Path

import numpy as np
import scipy.sparse as sp

from sage.all import Graph  # type: ignore


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "05_symmetry"

COIN_NPZ = DATA / "_toe" / "projector_recon_20260110" / (
    "N12_58_sector_coin_C24_K4_by_k_sparse_20260109T205353Z.npz"
)
TABLE_PATH = DATA / "_toe" / "projector_recon_20260110" / "binary_tetrahedral_2T_multiplication_table.csv"
ORDERS_PATH = DATA / "_toe" / "projector_recon_20260110" / "binary_tetrahedral_2T_element_orders.csv"


def load_coin_graph():
    z = np.load(COIN_NPZ, allow_pickle=True)
    C = sp.csr_matrix((z["data"], z["indices"], z["indptr"]), shape=tuple(z["shape"]))
    edges = []
    for i in range(C.shape[0]):
        start = C.indptr[i]
        end = C.indptr[i + 1]
        for k in range(start, end):
            j = int(C.indices[k])
            if i < j:
                edges.append((i, j))
    return Graph(edges), C


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


def cayley_graph(elems, table, S, side: str):
    idx = {e: i for i, e in enumerate(elems)}
    edges = set()
    for e in elems:
        for s in S:
            prod = table[(e, s)] if side == "right" else table[(s, e)]
            u = idx[e]
            v = idx[prod]
            if u != v:
                edges.add((min(u, v), max(u, v)))
    return Graph(list(edges))


def left_perm(elems, table, gen):
    idx = {e: i for i, e in enumerate(elems)}
    perm = np.zeros(len(elems), dtype=int)
    for i, e in enumerate(elems):
        prod = table[(gen, e)]
        perm[i] = idx[prod]
    return perm


def right_perm(elems, table, gen):
    idx = {e: i for i, e in enumerate(elems)}
    perm = np.zeros(len(elems), dtype=int)
    for i, e in enumerate(elems):
        prod = table[(e, gen)]
        perm[i] = idx[prod]
    return perm


def perm_matrix(perm):
    n = len(perm)
    rows = np.arange(n)
    cols = perm
    data = np.ones(n)
    return sp.csr_matrix((data, (rows, cols)), shape=(n, n))


def comm_norm(C, perm):
    P = perm_matrix(perm)
    comm = P.dot(C) - C.dot(P)
    if comm.nnz == 0:
        return 0.0
    return float(np.linalg.norm(comm.data))


def search_alignment():
    coin_g, coin_C = load_coin_graph()
    elems, table = load_table()
    orders = load_orders()

    order4 = [e for e in elems if orders.get(e) == 4]
    all_elems = [e for e in elems if e != "e"]

    def try_sets(candidates, side):
        for S in candidates:
            G = cayley_graph(elems, table, S, side)
            iso, mapping = coin_g.is_isomorphic(G, certificate=True)
            if iso:
                return S, mapping
        return None, None

    # Prefer order-4 triples (K4-like), then fall back to all triples.
    for side in ("right", "left"):
        S, mapping = try_sets(itertools.combinations(order4, 3), side)
        if S is not None:
            return side, S, mapping, elems, table, coin_C
        S, mapping = try_sets(itertools.combinations(all_elems, 3), side)
        if S is not None:
            return side, S, mapping, elems, table, coin_C
    return None, None, None, None, None, None


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    side, S, mapping, elems, table, coin_C = search_alignment()
    if side is None:
        raise RuntimeError("No Cayley alignment found.")

    # mapping: coin_index -> group_index
    n = len(elems)
    coin_to_group = np.zeros(n, dtype=int)
    for coin_idx, group_idx in mapping.items():
        coin_to_group[coin_idx] = group_idx
    group_to_coin = np.zeros_like(coin_to_group)
    for coin_idx, group_idx in enumerate(coin_to_group):
        group_to_coin[group_idx] = coin_idx

    # Reorder coin to group order (group index -> coin index).
    Cg = coin_C[group_to_coin][:, group_to_coin]

    # Check commutators for left/right generators.
    g1 = "(0 1)(2 3)"
    g2 = "(0 1 2)"
    if side == "right":
        perm1 = left_perm(elems, table, g1)
        perm2 = left_perm(elems, table, g2)
    else:
        perm1 = right_perm(elems, table, g1)
        perm2 = right_perm(elems, table, g2)

    comm1 = comm_norm(Cg, perm1)
    comm2 = comm_norm(Cg, perm2)

    # Write mapping.
    map_path = OUT_DIR / "coin_c24_2t_alignment_mapping.csv"
    with map_path.open("w", encoding="utf-8") as f:
        f.write("coin_index,element_label\n")
        for i in range(n):
            f.write(f"{i},{elems[coin_to_group[i]]}\n")

    summary_path = OUT_DIR / "coin_c24_2t_alignment_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# C24 coin alignment to 2T Cayley graph\n\n")
        f.write("Alignment search:\n")
        f.write(f"- side: {side}\n")
        f.write(f"- generator set S: {', '.join(S)}\n\n")
        f.write("Equivariance checks after alignment:\n")
        f.write(f"- commutator norm ({g1}): {comm1:.6e}\n")
        f.write(f"- commutator norm ({g2}): {comm2:.6e}\n")

    comm_path = OUT_DIR / "coin_c24_2t_alignment_commutators.csv"
    with comm_path.open("w", encoding="utf-8") as f:
        f.write("generator,commutator_frobenius\n")
        f.write(f"{g1},{comm1:.6e}\n")
        f.write(f"{g2},{comm2:.6e}\n")


if __name__ == "__main__":
    main()
