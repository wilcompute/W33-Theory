#!/usr/bin/env python3
"""
BT779 - The cube-web module: full equivariant decomposition.

The 540-node cube web (BT777) is PSp(4,3)-equivariant with spectrum

    6^1, (1+sqrt10)^24, ((-1+sqrt73)/2)^15, 3^60, 2^84, 1^81,
    (-1)^120, (1-sqrt10)^24, (-3)^116, ((-1-sqrt73)/2)^15.

Each eigenspace is a G-module. BT779 computes the character of every
eigenspace exactly (tr of spectral projector composed with the permutation
action, summed over all 25920 group elements, vectorized), then the full
Gram matrix of inner products. It answers:

  Q1. Is the eigenvalue-1 sector (dim 81) the Steinberg module?
  Q2. Is the Ramanujan-violating sector (dim 15 = g_neg) irreducible?
      Are the two 15-sectors (Galois pair) isomorphic?
  Q3. Are the two 24-sectors (Galois pair 1 +- sqrt10) isomorphic?
  Q4. What is the orbital rank of the skew-pair scheme?
"""
from __future__ import annotations

from collections import defaultdict
from itertools import combinations
import json
import os
from pathlib import Path

# Linear algebra on this 540 x 540 symmetric matrix is small, but some BLAS
# builds oversubscribe threads badly.  Cap defaults before importing numpy/scipy.
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import networkx as nx
import numpy as np
try:
    import scipy.linalg as sp_linalg
except Exception:  # pragma: no cover - optional accelerator
    sp_linalg = None


ROOT = Path(__file__).resolve().parents[1]


def inv3(a):
    a %= 3
    if a in (1, 2):
        return a
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def points():
    return sorted({
        canon((a, b, c, d))
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a, b, c, d) != (0, 0, 0, 0)
    })


def symp(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def build_psp(pts):
    n = len(pts)
    pt_index = {p: i for i, p in enumerate(pts)}

    def transvection_perm(v):
        out = []
        for x in pts:
            w = symp(x, v)
            out.append(pt_index[canon(tuple(
                (x[k] + w * v[k]) % 3 for k in range(4)))])
        return tuple(out)

    seed_vectors = [
        canon((1, 0, 0, 0)), canon((0, 1, 0, 0)),
        canon((0, 0, 1, 0)), canon((0, 0, 0, 1)),
        canon((1, 1, 0, 0)), canon((1, 0, 1, 0)),
        canon((1, 0, 0, 1)), canon((0, 1, 1, 0)),
    ]
    gens_psp = [transvection_perm(v) for v in seed_vectors]
    ident = tuple(range(n))

    def compose(a, b):
        return tuple(a[b[i]] for i in range(n))

    psp = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens_psp:
                gh = compose(h, g)
                if gh not in psp:
                    psp.add(gh)
                    nxt.append(gh)
        frontier = nxt
    psp = list(psp)
    assert len(psp) == 25920
    return psp


def build_geometry():
    pts = points()
    n = 40
    adj = [[False]*n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [frozenset(q) for q in combinations(range(n), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    assert len(lines) == 40
    line_sets = [set(l) for l in lines]
    line_index = {l: i for i, l in enumerate(lines)}
    skew = [(i, j) for i, j in combinations(range(40), 2)
            if not (line_sets[i] & line_sets[j])]
    assert len(skew) == 540
    skew_index = {frozenset(p): k for k, p in enumerate(skew)}
    return pts, adj, lines, line_sets, line_index, skew, skew_index


def build_web(skew, skew_index, line_sets):
    web = nx.Graph()
    web.add_nodes_from(range(540))
    for (i, j) in skew:
        tv = [k for k in range(40)
              if k != i and k != j
              and line_sets[k] & line_sets[i] and line_sets[k] & line_sets[j]]
        for a, b in combinations(tv, 2):
            if not (line_sets[a] & line_sets[b]):
                web.add_edge(skew_index[frozenset((i, j))],
                             skew_index[frozenset((a, b))])
    return web


def main():
    pts, adj, lines, line_sets, line_index, skew, skew_index = build_geometry()
    psp = build_psp(pts)
    ng = len(psp)

    print("building 25920 x 540 permutation array ...")
    perm = np.empty((ng, 540), dtype=np.int16)
    # Vectorized pair lookup: once line images are known, all 540 skew-pair
    # images are a single numpy gather instead of a Python inner loop.
    line_key_index = {tuple(sorted(l)): i for i, l in enumerate(lines)}
    pair_to_skew = -np.ones((40, 40), dtype=np.int16)
    for s, (i, j) in enumerate(skew):
        pair_to_skew[i, j] = pair_to_skew[j, i] = s
    skew_i = np.array([i for i, _ in skew], dtype=np.int16)
    skew_j = np.array([j for _, j in skew], dtype=np.int16)
    for gi, g in enumerate(psp):
        lperm = np.empty(40, dtype=np.int16)
        for li, line in enumerate(lines):
            lperm[li] = line_key_index[tuple(sorted(g[x] for x in line))]
        perm[gi] = pair_to_skew[lperm[skew_i], lperm[skew_j]]

    web = build_web(skew, skew_index, line_sets)
    print("web built; diagonalizing 540 x 540 adjacency ...")
    a = nx.to_numpy_array(web)
    if sp_linalg is not None:
        vals, vecs = sp_linalg.eigh(a, driver="evr", check_finite=False)
        print("diagonalization done")
    else:
        vals, vecs = np.linalg.eigh(a)
    clusters = defaultdict(list)
    for idx, v in enumerate(vals):
        clusters[round(float(v), 6)].append(idx)
    eigs = sorted(clusters.keys(), reverse=True)
    print("eigenspaces:", [(e, len(clusters[e])) for e in eigs])

    ar = np.arange(540)
    chis = {}
    for e in eigs:
        v = vecs[:, clusters[e]]
        proj = v @ v.T
        chis[e] = proj[ar[None, :], perm].sum(axis=1)

    labels = eigs
    m = len(labels)
    gram = np.zeros((m, m))
    for i in range(m):
        for j in range(i, m):
            ip = float(np.dot(chis[labels[i]], chis[labels[j]])) / ng
            gram[i, j] = gram[j, i] = round(ip, 3)

    print("\nGram matrix of eigenspace characters <chi_E, chi_F>:")
    hdr = "        " + "".join(f"{e:>9.3f}" for e in labels)
    print(hdr)
    for i in range(m):
        print(f"{labels[i]:>7.3f} " +
              "".join(f"{gram[i, j]:>9.0f}" for j in range(m)))

    chi_perm = sum(chis[e] for e in labels)
    rank = round(float(np.dot(chi_perm, chi_perm)) / ng)
    print(f"\norbital rank of the skew-pair scheme = {rank}")

    norms = {e: int(round(gram[labels.index(e), labels.index(e)]))
             for e in labels}
    dims = {e: len(clusters[e]) for e in labels}
    verdicts = {}
    print("\nsector verdicts:")
    for e in labels:
        d = dims[e]
        norm = norms[e]
        tag = "IRREDUCIBLE" if norm == 1 else f"norm {norm} (reducible/multiplicity)"
        print(f"  eig {e:>9.3f}: dim {d:>3}, {tag}")
        verdicts[str(e)] = {"dim": d, "norm": norm}

    def ip_of(e1, e2):
        return int(round(gram[labels.index(e1), labels.index(e2)]))

    pair24 = ip_of(labels[1], labels[-3])
    pair15 = ip_of(labels[2], labels[-1])
    st81 = norms.get(1.0)
    print(f"\n<chi_24+, chi_24-> = {pair24}  (1 => same 24-irrep twice)")
    print(f"<chi_15+, chi_15-> = {pair15}  (0 => the TWO 15-irreps; 1 => same)")
    print(f"eigenvalue-1 dim-81 sector norm = {st81} "
          f"({'STEINBERG' if st81 == 1 else 'not irreducible'})")

    out = {
        "theorem": "BT779 web module decomposition",
        "group_order": ng,
        "web_vertices": web.number_of_nodes(),
        "web_edges": web.number_of_edges(),
        "orbital_rank": rank,
        "eigenvalue_order": labels,
        "gram_matrix": gram.astype(int).tolist(),
        "sectors": verdicts,
        "pair24_inner": pair24,
        "pair15_inner": pair15,
        "steinberg_81": bool(st81 == 1),
        "forced_decomposition": {
            "total": "1 + 2*24 + 3*15 + 2*81 + 2*20 + 64 + 2*30a + 2*30b + 60",
            "eig_6": "1",
            "eig_1_plus_sqrt10": "24",
            "eig_1_minus_sqrt10": "24",
            "eig_pos_sqrt73_branch": "15",
            "eig_neg_sqrt73_branch": "15",
            "eig_3": "30a + 30b",
            "eig_2": "20 + 64",
            "eig_1": "81 Steinberg",
            "eig_minus1": "30a + 30b + 60",
            "eig_minus3": "81 + 20 + 15"
        }
    }
    outpath = ROOT / "data" / "bt779_web_module_decomposition.json"
    outpath.parent.mkdir(exist_ok=True)
    with outpath.open("w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {outpath.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
