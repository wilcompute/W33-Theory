#!/usr/bin/env python3
"""BT997 — production stochastic heat estimator for K3_16 middle-degree L2.

Builds the real level-1 edgewise K3_16 middle Hodge Laplacian and estimates
Tr(exp(-t L_2)) by Hutchinson probes with scipy.sparse.linalg.expm_multiply.
This is the production path identified in BT994/BT995: sparse trace estimation,
not dense middle-degree eigensolve.
"""
from __future__ import annotations

from itertools import combinations, product
from pathlib import Path
import json
import sys

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import expm_multiply

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "exploration"))
from w33_explicit_curved_4d_complexes import k3_facets  # noqa: E402


def bary_vertices():
    return [tuple(c) for c in product(range(3), repeat=5) if sum(c) == 2]

BARY = bary_vertices()
BARY_INDEX = {v: i for i, v in enumerate(BARY)}

def original(i):
    v = [0] * 5; v[i] = 2; return BARY_INDEX[tuple(v)]

def midpoint(i, j):
    v = [0] * 5; v[i] = 1; v[j] = 1; return BARY_INDEX[tuple(v)]

def local_template():
    top = []
    for i in range(5):
        top.append(tuple(sorted([original(i)] + [midpoint(i, j) for j in range(5) if j != i])))
    pull = (0, 1); pull_idx = midpoint(*pull)
    def octahedron_tets(coord_zero):
        rem = [j for j in range(5) if j != coord_zero]
        p = tuple(rem[:2]); pidx = midpoint(*p); tets = []
        for j in rem:
            if j in p:
                tri_pairs = list(combinations([x for x in rem if x != j], 2))
            else:
                tri_pairs = [tuple(sorted((j, k))) for k in rem if k != j]
            tets.append(tuple(sorted([pidx] + [midpoint(*q) for q in tri_pairs])))
        return sorted(set(tets))
    for i in pull:
        for tet in octahedron_tets(i):
            top.append(tuple(sorted([pull_idx] + list(tet))))
    for i in range(5):
        if i not in pull:
            tet = [midpoint(*tuple(sorted((i, j)))) for j in range(5) if j != i]
            top.append(tuple(sorted([pull_idx] + tet)))
    return tuple(sorted(set(top)))

TEMPLATE = local_template()

def subdivide_facets(facets):
    out = []
    for facet in facets:
        local = list(facet)
        def map_vertex(local_bary_index):
            c = BARY[local_bary_index]
            nz = [i for i, x in enumerate(c) if x]
            if len(nz) == 1:
                return ("v", local[nz[0]])
            a, b = local[nz[0]], local[nz[1]]
            return ("m", min(a, b), max(a, b))
        for simplex in TEMPLATE:
            out.append(tuple(sorted((map_vertex(i) for i in simplex), key=str)))
    verts = sorted({v for s in out for v in s}, key=str)
    idx = {v: i for i, v in enumerate(verts)}
    return tuple(tuple(sorted(idx[v] for v in s)) for s in out)

def faces_by_dim(top):
    faces = [set() for _ in range(5)]
    for simplex in top:
        for r in range(1, 6):
            for face in combinations(simplex, r):
                faces[r - 1].add(tuple(sorted(face)))
    return [tuple(sorted(level)) for level in faces]

def boundary_sparse(high, low):
    low_index = {s: i for i, s in enumerate(low)}
    rows, cols, data = [], [], []
    for col, simplex in enumerate(high):
        for pos in range(len(simplex)):
            face = simplex[:pos] + simplex[pos + 1:]
            rows.append(low_index[face]); cols.append(col); data.append(-1.0 if pos % 2 else 1.0)
    return sp.coo_matrix((data, (rows, cols)), shape=(len(low), len(high))).tocsr()

def k3_middle_laplacian():
    top = subdivide_facets(k3_facets())
    faces = faces_by_dim(top)
    d2 = boundary_sparse(faces[2], faces[1])
    d3 = boundary_sparse(faces[3], faces[2])
    return (d2.T @ d2 + d3 @ d3.T).tocsr()

def estimate(A, t_values=(0.01, 0.05, 0.1, 1.0), probes=8, seed=997):
    rng = np.random.default_rng(seed)
    out = {}
    for t in t_values:
        samples = []
        for _ in range(probes):
            z = rng.choice([-1.0, 1.0], size=A.shape[0])
            y = expm_multiply((-t) * A, z)
            samples.append(float(z @ y))
        arr = np.array(samples)
        out[str(t)] = {
            "estimate": float(arr.mean()),
            "standard_error": float(arr.std(ddof=1) / np.sqrt(probes)),
            "probes": probes,
        }
    return out

def main():
    L2 = k3_middle_laplacian()
    out = {
        "theorem": "BT997 stochastic K3_16 middle-degree heat trace estimator",
        "laplacian": {"degree": 2, "shape": list(L2.shape), "nnz": int(L2.nnz)},
        "method": "Hutchinson Rademacher probes + scipy.sparse.linalg.expm_multiply",
        "estimates": estimate(L2),
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt997_k3_middle_heat_estimator.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
