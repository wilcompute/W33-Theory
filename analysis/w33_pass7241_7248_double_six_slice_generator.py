#!/usr/bin/env python3
"""Passes 7241--7248: the 36 double-six doily slices generate C_spread.

Let M be the canonical 45 x 36 cubic-surface incidence matrix from Pass4992:
M[t,D]=1 iff tritangent t meets double-six D in two lines.  For a double-six D,
let N[:,D] be the indicator of the 15 tritangents disjoint from D -- exactly the
doily/syntheme slice of Pass7225--7232.

For every (t,D), intersection size is 0 or 2, hence over F2

    N = J + M.

This replay proves:
  rank(M)=20,
  rank(N)=21,
  col(M)=the even subcode of C_spread,
  col(N)=C_spread=[45,21,5]_2.

It also records the 36-slice block design geometry:
  * every slice has 15 tritangents;
  * every tritangent lies in 12 slices;
  * two slices meet in 6 coordinates exactly when the corresponding
    double-sixes meet in 6 cubic lines (the H36 edge relation), otherwise in 3.

Thus the recent 1+V20 module decomposition has a direct incidence realization.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

from w33_pass4992_4999_common import build_base
from w33_pass7225_7232_spread_code_doily_puncture import (
    center_data,
    coordinate_isomorphism,
    gf2_basis,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS7241_7248_DOUBLE_SIX_SLICE_GENERATOR.json"


def in_span(x, basis):
    piv = {}
    for b0 in basis:
        b = int(b0)
        while b:
            p = b.bit_length() - 1
            if p in piv:
                b ^= piv[p]
            else:
                piv[p] = b
                break
    y = int(x)
    while y:
        p = y.bit_length() - 1
        if p not in piv:
            return False
        y ^= piv[p]
    return True


def col_masks(A):
    rows, cols = A.shape
    out = []
    for j in range(cols):
        m = 0
        for i in range(rows):
            if int(A[i, j]) & 1:
                m |= 1 << i
        out.append(m)
    return out


def main() -> int:
    base = build_base()
    T = base["tritangents"]
    DS = base["DS"]
    M = np.asarray(base["M"], dtype=np.uint8) % 2
    assert M.shape == (45, 36)

    # Reconstruct the current E8/D4 spread code in the canonical tritangent coordinates.
    supports, packs = center_data(base["W"])
    p_s_to_t = coordinate_isomorphism(supports, T)
    spread_masks = []
    for C in packs:
        m = 0
        for z in C:
            m |= 1 << p_s_to_t[z]
        spread_masks.append(m)
    Bspread = gf2_basis(spread_masks)
    assert len(Bspread) == 21

    # N is the incidence matrix of the 36 doily slices (tritangents disjoint from D).
    N = np.zeros((45, 36), dtype=np.uint8)
    intersection_values = set()
    for t, tri in enumerate(T):
        for d, D in enumerate(DS):
            k = len(set(tri) & set(D))
            intersection_values.add(k)
            if k == 0:
                N[t, d] = 1
    assert intersection_values == {0, 2}
    assert np.array_equal(N, (1 + M) % 2)
    assert set(map(int, N.sum(axis=0))) == {15}
    assert set(map(int, N.sum(axis=1))) == {12}

    Mcols = col_masks(M)
    Ncols = col_masks(N)
    BM = gf2_basis(Mcols)
    BN = gf2_basis(Ncols)
    assert len(BM) == 20
    assert len(BN) == 21

    # Exact span identity C_spread = col(N).
    assert all(in_span(x, BN) for x in spread_masks)
    assert all(in_span(x, Bspread) for x in Ncols)

    # The even subcode of C_spread is exactly col(M).
    odd = next(x for x in Bspread if x.bit_count() & 1)
    even_rows = []
    for x in Bspread:
        y = x if x.bit_count() % 2 == 0 else x ^ odd
        if y:
            even_rows.append(y)
    Beven = gf2_basis(even_rows)
    assert len(Beven) == 20
    assert all(in_span(x, BM) for x in Beven)
    assert all(in_span(x, Beven) for x in Mcols)

    # Double-six slice intersection scheme.
    H36_edges = set()
    for i, j in itertools.combinations(range(36), 2):
        if len(DS[i] & DS[j]) == 6:
            H36_edges.add((i, j))
    assert len(H36_edges) == 360

    pair_counts = Counter()
    for i, j in itertools.combinations(range(36), 2):
        inter = (Ncols[i] & Ncols[j]).bit_count()
        rel = "H36_edge" if (i, j) in H36_edges else "H36_nonedge"
        pair_counts[(rel, inter)] += 1
    assert pair_counts == Counter({("H36_edge", 6): 360, ("H36_nonedge", 3): 270})

    out = {
        "schema": "w33.pass7241_7248.double_six_slice_generator.v1",
        "status": "PASS",
        "passes": "7241-7248",
        "matrix_identity": "N = J + M over F2",
        "M": {
            "shape": [45, 36],
            "meaning": "M[t,D]=1 iff tritangent t meets double-six D in two lines",
            "rank": 20,
            "column_span": "even subcode of C_spread",
        },
        "N": {
            "shape": [45, 36],
            "meaning": "N[t,D]=1 iff tritangent t is disjoint from D, i.e. lies in its doily slice",
            "column_weight": 15,
            "row_weight": 12,
            "rank": 21,
            "column_span": "C_spread=[45,21,5]_2",
        },
        "span_equalities": {
            "col_N_equals_Cspread": True,
            "col_M_equals_even_Cspread": True,
            "Cspread_equals_1_plus_V20": "realized directly by complementing the tritangent/double-six incidence columns",
        },
        "slice_intersections": {
            "H36_edge": {"double_six_pairs": 360, "doily_slice_intersection": 6},
            "H36_nonedge": {"double_six_pairs": 270, "doily_slice_intersection": 3},
        },
        "interpretation": (
            "The 27 ten-D4 spreads and the 36 cubic-surface double-sixes are two generating systems for the same "
            "45-coordinate [45,21,5] code.  The even 20-space is the column space of the old tritangent/double-six "
            "selector M, while adding the complements N=J+M supplies the odd line and yields the full spread code."
        ),
        "boundary": "Exact finite incidence/coding identity only; no physical interpretation is promoted.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "rankM": 20, "rankN": 21, "Cspread": "col(N)"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
