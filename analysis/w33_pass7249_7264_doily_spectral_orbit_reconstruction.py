#!/usr/bin/env python3
"""Passes 7249--7264: spectral/intertwiner anatomy of the 36 doily slices.

This replay starts only from the canonical cubic-surface objects already built by
Pass4992 and the doily-slice incidence matrix of Pass7241.  It proves that the
36 double-six slices are simultaneously:

* a two-intersection tactical design on the 45 tritangents;
* a two-distance tight frame after centering;
* an exact rank-20 intertwiner between the primitive 20-spaces of the
  45-tritangent and 36-double-six strongly regular graphs;
* a single PSp(4,3)-orbit whose binary span reconstructs the full
  C_spread=[45,21,5]_2 code from one chosen doily slice.

Finite geometry/coding only.
"""
from __future__ import annotations

from collections import Counter, deque
from pathlib import Path
import json
import itertools
import numpy as np

from w33_pass4992_4999_common import build_base, build_group

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS7249_7264_DOILY_SPECTRAL_ORBIT_RECONSTRUCTION.json"


def gf2_rank_cols(cols):
    piv = {}
    for col in cols:
        x = 0
        for i, b in enumerate(col):
            if int(b) & 1:
                x |= 1 << i
        while x:
            p = x.bit_length() - 1
            if p in piv:
                x ^= piv[p]
            else:
                piv[p] = x
                break
    return len(piv)


def orbit_order(seed, gens):
    seen = {seed}
    order = [seed]
    q = deque([seed])
    while q:
        x = q.popleft()
        for g in gens:
            y = g[x]
            if y not in seen:
                seen.add(y)
                order.append(y)
                q.append(y)
    return order


def srg_common_neighbor_profile(A):
    n = A.shape[0]
    adj = Counter()
    non = Counter()
    for i, j in itertools.combinations(range(n), 2):
        c = int(np.dot(A[i], A[j]))
        (adj if A[i, j] else non)[c] += 1
    return adj, non


def main() -> int:
    base = build_base()
    T, DS = base["tritangents"], base["DS"]

    # N[t,D]=1 iff tritangent t is disjoint from double-six D.
    M = np.asarray(base["M"], dtype=np.int64)
    N = 1 - M
    assert N.shape == (45, 36)
    assert set(map(int, N.sum(axis=0))) == {15}
    assert set(map(int, N.sum(axis=1))) == {12}

    # H36 on double-sixes: adjacency means intersection in six cubic lines.
    A36 = np.zeros((36, 36), dtype=np.int64)
    for i, j in itertools.combinations(range(36), 2):
        if len(DS[i] & DS[j]) == 6:
            A36[i, j] = A36[j, i] = 1
    assert set(map(int, A36.sum(axis=1))) == {20}
    e36, n36 = srg_common_neighbor_profile(A36)
    assert e36 == Counter({10: 360})
    assert n36 == Counter({12: 270})

    # G45 on tritangents: adjacency means sharing one cubic-surface line.
    A45 = np.zeros((45, 45), dtype=np.int64)
    for i, j in itertools.combinations(range(45), 2):
        if set(T[i]) & set(T[j]):
            A45[i, j] = A45[j, i] = 1
    assert set(map(int, A45.sum(axis=1))) == {12}
    e45, n45 = srg_common_neighbor_profile(A45)
    assert e45 == Counter({3: 270})
    assert n45 == Counter({3: 720})

    I36, J36 = np.eye(36, dtype=np.int64), np.ones((36, 36), dtype=np.int64)
    I45, J45 = np.eye(45, dtype=np.int64), np.ones((45, 45), dtype=np.int64)

    # Exact two-sided Gram identities.
    assert np.array_equal(N.T @ N, 12 * I36 + 3 * J36 + 3 * A36)
    assert np.array_equal(N @ N.T, 9 * I45 + 3 * J45 + 3 * A45)

    # Integer centered intertwiner X3 = 3N-J; X=X3/3.
    X3 = 3 * N - np.ones((45, 36), dtype=np.int64)
    assert np.array_equal(2 * (A45 @ X3), 3 * (X3 @ A36))
    assert np.array_equal(X3.T @ X3, 108 * I36 - 18 * J36 + 27 * A36)
    assert np.array_equal(X3 @ X3.T, 81 * I45 - 9 * J45 + 27 * A45)
    assert np.linalg.matrix_rank(N.astype(float)) == 21
    assert np.linalg.matrix_rank(X3.astype(float)) == 20

    # The centered columns are a 36-vector two-distance tight frame in R^20.
    # X=N-J/3 has norm^2 10, with inner products 1 (H36 edge) and -2 (nonedge),
    # and all 20 nonzero Gram eigenvalues equal 18.
    centered_gram9 = X3.T @ X3
    evals_centered = Counter(round(float(x), 8) for x in np.linalg.eigvalsh(centered_gram9 / 9.0))
    assert evals_centered == Counter({0.0: 16, 18.0: 20})
    raw_evals = Counter(round(float(x), 8) for x in np.linalg.eigvalsh((N.T @ N).astype(float)))
    assert raw_evals == Counter({0.0: 15, 18.0: 20, 180.0: 1})

    # One chosen slice generates the whole binary code under PSp(4,3).
    grp = build_group(base)
    orbit = orbit_order(0, grp["DPp"])
    assert len(orbit) == 36
    ranks = [gf2_rank_cols([N[:, d] for d in orbit[:k]]) for k in range(1, 37)]
    assert ranks[-1] == 21
    first_full = next(k for k, r in enumerate(ranks, 1) if r == 21)

    # The overlap relation of the orbit columns reconstructs H36 itself.
    for i, j in itertools.combinations(range(36), 2):
        ov = int(np.dot(N[:, i], N[:, j]))
        assert ov == (6 if A36[i, j] else 3)

    out = {
        "schema": "w33.pass7249_7264.doily_spectral_orbit_reconstruction.v1",
        "status": "PASS",
        "passes": "7249-7264",
        "design": {
            "incidence_shape": [45, 36],
            "slice_size": 15,
            "slices_through_tritangent": 12,
            "double_six_graph": "SRG(36,20,10,12)",
            "tritangent_graph": "SRG(45,12,3,3)",
            "slice_intersection": {"H36_edge": 6, "H36_nonedge": 3},
        },
        "gram": {
            "N_transpose_N": "12 I_36 + 3 J_36 + 3 A_36",
            "N_N_transpose": "9 I_45 + 3 J_45 + 3 A_45",
            "spectrum_NtN": {"180": 1, "18": 20, "0": 15},
            "rank_N_Q": 21,
        },
        "centered_intertwiner": {
            "X3": "3N-J",
            "identity": "2 A_45 X3 = 3 X3 A_36",
            "rank": 20,
            "centered_column_norm_squared": 10,
            "centered_inner_products": {"H36_edge": 1, "H36_nonedge": -2},
            "nonzero_tight_frame_gram_eigenvalue": 18,
            "interpretation": "X/sqrt(18) is a partial isometry between the 20-dimensional primitive eigenspaces A36:eigenvalue2 and A45:eigenvalue3",
        },
        "single_slice_reconstruction": {
            "PSp_orbit_size": 36,
            "binary_orbit_span_dimension": 21,
            "first_full_rank_BFS_prefix": first_full,
            "reconstructs": "C_spread=[45,21,5]_2",
            "overlap_relation_recovers_H36": True,
        },
        "boundary": "Exact finite incidence/module statement only; no continuum or physical claim follows.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "rankN": 21, "rankX": 20, "orbit": 36, "first_full": first_full}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
