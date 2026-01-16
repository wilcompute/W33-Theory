#!/usr/bin/env python3
"""Search transport commutators over full Cayley-graph automorphism group."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
from sage.all import Graph  # type: ignore


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "05_symmetry"

COIN_NPZ = DATA / "_toe" / "projector_recon_20260110" / (
    "N12_58_sector_coin_C24_K4_by_k_sparse_20260109T205353Z.npz"
)
H_TRANSPORT = DATA / "_toe" / "projector_recon_20260110" / (
    "N12_58_orbit0_H_transport_59x24_sparse_20260109T205353Z.npz"
)


def load_csr_npz(path: Path) -> sp.csr_matrix:
    z = np.load(path, allow_pickle=True)
    return sp.csr_matrix((z["data"], z["indices"], z["indptr"]), shape=tuple(z["shape"]))


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
    return Graph(edges)


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
    G = load_coin_graph()
    aut = G.automorphism_group()
    order = aut.order()

    # Enumerate a manageable subset: identity, generators, and random samples.
    sample = []
    sample.append(aut.identity())
    sample.extend(list(aut.gens()))
    rng_elems = 200
    for _ in range(rng_elems):
        sample.append(aut.random_element())

    H = load_csr_npz(H_TRANSPORT)
    rows = []
    for idx, g in enumerate(sample):
        perm_coin = [int(g(i)) for i in range(24)]
        perm = perm_full(perm_coin)
        rows.append(
            {
                "aut_index": idx,
                "perm": g.cycle_string(),
                "comm_norm": comm_norm_by_perm(H, perm),
            }
        )

    df = pd.DataFrame(rows).sort_values("comm_norm")
    df.to_csv(OUT_DIR / "transport_cayley_autgroup_commutators.csv", index=False)

    exact = df[df["comm_norm"] == 0.0]
    summary_path = OUT_DIR / "transport_cayley_autgroup_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# Transport commutators over Cayley-graph automorphisms\n\n")
        f.write(f"Automorphism group order: {order}\n\n")
        f.write(f"Sample size: {len(sample)} (identity + generators + random)\n\n")
        f.write("Exact symmetries (comm_norm=0):\n\n")
        if exact.empty:
            f.write("- none\n\n")
        else:
            f.write(exact[["aut_index", "perm"]].to_markdown(index=False))
            f.write("\n\n")
        f.write("Top 8 smallest commutators:\n\n")
        f.write(df.head(8).to_markdown(index=False))


if __name__ == "__main__":
    main()
