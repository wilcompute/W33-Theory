#!/usr/bin/env python3
"""Passes 7281--7296: q=9 local-section obstruction and blocker-frame signature.

The original proposed attack tried to push the 15-coordinate doily code directly onto
the q=9 partial-ovoid witness.  That is not canonical: the [15,5,6] doily carrier lives
on cubic-surface tritangents after an E6 transport, whereas the q=9 witness lives on
points of W(3,9).  This pass replaces that non-canonical step by two q=9-native tests:

1. embedded W(3,3) section inequalities: every intersection with a symplectic F3
   subgeometry is itself a partial ovoid of W(3,3), hence has size at most 7;
2. the blocker incidence frame of the frozen 51-set, whose exact second and third
   moments give a code-like finite signature for exchange searches.

A deterministic 20,000-section transvection scan is search evidence only, not an
exhaustive orbit theorem and not an upper bound for alpha(W(3,9)).
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path
import numpy as np

from w33_pass7107_q9_target_52 import ADD, MUL, NEG, INV, build, check_field

ROOT = Path(__file__).resolve().parents[1]
WITNESS = ROOT / "data" / "PART_W33_Q9_PARTIAL_OVOID_51.json"
OUT = ROOT / "data" / "PART_W33_PASS7281_7296_Q9_SECTION_BLOCKER_CODE.json"


def gf2_rank(A):
    piv = {}
    for row in A:
        x = 0
        for i, b in enumerate(row):
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


def main() -> int:
    check_field()
    P, adj, B = build()
    assert len(P) == 820 and {len(x) for x in adj} == {90}
    pindex = {p: i for i, p in enumerate(P)}

    w = json.loads(WITNESS.read_text(encoding="utf-8"))
    S = list(map(int, w["point_indices"]))
    Sset = set(S)
    assert len(S) == 51

    # Standard F3-fixed symplectic subgeometry.
    F3 = [i for i, p in enumerate(P) if all(x < 3 for x in p)]
    assert len(F3) == 40
    fixed_intersection = sorted(Sset & set(F3))
    assert len(fixed_intersection) == 4

    def canon(v):
        lead = next(x for x in v if x)
        iv = INV[lead]
        return tuple(MUL[x][iv] for x in v)

    # Eight distinct diagonal-torus translates of the standard W33 section.
    torus = set()
    F3pts = [P[i] for i in F3]
    for a in range(1, 9):
        ai = INV[a]
        for b in range(1, 9):
            bi = INV[b]
            X = frozenset(
                pindex[canon((MUL[a][p[0]], MUL[ai][p[1]], MUL[b][p[2]], MUL[bi][p[3]]))]
                for p in F3pts
            )
            torus.add(X)
    assert len(torus) == 8
    torus_hist = Counter(len(X & Sset) for X in torus)
    assert torus_hist == Counter({3: 3, 2: 2, 0: 1, 1: 1, 4: 1})

    # Deterministic non-F3 symplectic transvections: x -> x + B(x,v) v.
    def addv(u, v):
        return tuple(ADD[x][y] for x, y in zip(u, v))

    def scale(a, v):
        return tuple(MUL[a][x] for x in v)

    def tperm(v):
        out = []
        for x in P:
            y = addv(x, scale(B(x, v), v))
            out.append(pindex[canon(y)])
        assert len(set(out)) == 820
        return tuple(out)

    gen_vecs = [
        (1, 0, 3, 0), (1, 3, 0, 0), (1, 0, 0, 3),
        (0, 1, 3, 0), (3, 1, 0, 1), (1, 3, 1, 0),
    ]
    gens = [tperm(v) for v in gen_vecs]
    base = frozenset(F3)
    seen = {base}
    q = deque([base])
    cap = 20000
    while q and len(seen) < cap:
        X = q.popleft()
        for g in gens:
            Y = frozenset(g[i] for i in X)
            if Y not in seen:
                seen.add(Y)
                q.append(Y)
                if len(seen) >= cap:
                    break
    assert len(seen) == cap
    section_hist = Counter(len(X & Sset) for X in seen)
    expected_section_hist = Counter({2: 7343, 3: 7291, 1: 2453, 4: 2305, 5: 322, 0: 276, 6: 10})
    assert section_hist == expected_section_hist
    assert max(section_hist) == 6

    # Every sampled intersection is a partial ovoid inside its embedded W33 section.
    for X in seen:
        I = X & Sset
        assert all(b not in adj[a] for a, b in itertools.combinations(I, 2))

    # Blocker incidence: rows=769 outside points, columns=51 witness points.
    outside = [v for v in range(820) if v not in Sset]
    spos = {s: i for i, s in enumerate(S)}
    BI = np.zeros((len(outside), 51), dtype=np.int64)
    for r, v in enumerate(outside):
        for s in adj[v] & Sset:
            BI[r, spos[s]] = 1
    assert np.array_equal(BI.T @ BI, 80 * np.eye(51, dtype=np.int64) + 10 * np.ones((51, 51), dtype=np.int64))
    assert gf2_rank(BI) == 51

    # Integer-centered columns form an exact regular simplex in dimension 50.
    rowsums = BI.sum(axis=1)
    Y = 51 * BI - rowsums[:, None] * np.ones((1, 51), dtype=np.int64)
    assert np.array_equal(Y.T @ Y, 208080 * np.eye(51, dtype=np.int64) - 4080 * np.ones((51, 51), dtype=np.int64))
    assert np.linalg.matrix_rank(Y.astype(float)) == 50

    # Third moment / triad-center refinement of the frozen witness.
    tri = Counter()
    special = []
    for a, b, c in itertools.combinations(range(51), 3):
        z = len(adj[S[a]] & adj[S[b]] & adj[S[c]])
        tri[z] += 1
        if z == 10:
            special.append((a, b, c))
    assert tri == Counter({1: 20722, 10: 103})
    H3 = np.zeros((103, 51), dtype=np.uint8)
    deg = [0] * 51
    pairdeg = Counter()
    for r, e in enumerate(special):
        for i in e:
            H3[r, i] = 1
            deg[i] += 1
        for p in itertools.combinations(e, 2):
            pairdeg[p] += 1
    assert gf2_rank(H3) == 51
    assert Counter(deg) == Counter({5: 12, 6: 12, 7: 7, 3: 6, 8: 6, 4: 4, 11: 2, 12: 2})
    assert Counter(pairdeg.values()) == Counter({1: 285, 2: 12})

    out = {
        "schema": "w33.pass7281_7296.q9_section_blocker_code.v1",
        "status": "PASS",
        "passes": "7281-7296",
        "canonicality_correction": (
            "The 15-coordinate doily code is a tritangent/E6 carrier, not a canonical point-subset carrier of W(3,9). "
            "The q=9-native local obstruction is therefore intersection with embedded W(3,3) symplectic subgeometries."
        ),
        "standard_F3_section": {"points": 40, "witness_intersection": 4},
        "diagonal_torus_sections": {"distinct": 8, "intersection_histogram": {str(k): v for k, v in sorted(torus_hist.items())}},
        "deterministic_transvection_scan": {
            "sections": cap,
            "intersection_histogram": {str(k): v for k, v in sorted(section_hist.items())},
            "maximum_seen": 6,
            "theorem_cap_for_any_embedded_W33_section": 7,
            "boundary": "20,000-section scan is not exhaustive and is not an upper bound for the q=9 partial-ovoid problem",
        },
        "blocker_frame": {
            "shape": [769, 51],
            "gram": "B^T B = 80 I_51 + 10 J_51",
            "GF2_rank": 51,
            "centered_integer_gram": "Y^T Y = 208080 I_51 - 4080 J_51",
            "centered_rank": 50,
            "interpretation": "the 51 centered blocker columns form a regular simplex in a 50-dimensional real space",
        },
        "third_moment_signature": {
            "triad_center_counts": {"1": 20722, "10": 103},
            "ten_center_triad_hypergraph_edges": 103,
            "GF2_incidence_rank": 51,
            "vertex_degree_histogram": {str(k): v for k, v in sorted(Counter(deg).items())},
            "used_pairs_multiplicity": {"1": 285, "2": 12},
        },
        "boundary": "Exact finite/search signatures only. Nothing here proves alpha(W(3,9))=51 or rules out 52.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "sections": cap, "max_section_hit": 6, "special_triads": 103}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
