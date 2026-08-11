#!/usr/bin/env python3
"""Pass4953 — standard W(3,3) triad-center baseline.

The repo contains two nonisomorphic GQ(3,3) collinearity graphs with the same
SRG(40,12,2,4) parameters: the standard symplectic W(3,3) point graph and the
point graph of its dual Q(4,3).  Pass4954 identifies the Steiner 40-fiber
quotient as the latter.  This pass freezes the standard W(3,3) baseline:
three pairwise noncollinear projective points have exactly 1 or 4 common
neighbors, with distribution 2880 and 360.

The 360 four-center triads are exactly the 3-subsets of the 90 non-isotropic
projective lines of PG(3,3).  Thus the earlier 0/2 statistics are not wrong
arithmetic; they belong to the dual Q(4,3) quotient rather than W(3,3) points.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4953_STANDARD_W33_TRIAD_CENTERS.json"


def canon(v):
    v = tuple(x % 3 for x in v)
    j = next(i for i, x in enumerate(v) if x)
    inv = 1 if v[j] == 1 else 2
    return tuple((inv * x) % 3 for x in v)


def symp(x, y):
    return (x[0]*y[1] - x[1]*y[0] + x[2]*y[3] - x[3]*y[2]) % 3


def rank3(rows):
    A = [list(r) for r in rows]
    m, n = len(A), len(A[0])
    r = 0
    for c in range(n):
        q = next((i for i in range(r, m) if A[i][c] % 3), None)
        if q is None:
            continue
        A[r], A[q] = A[q], A[r]
        if A[r][c] == 2:
            A[r] = [(2*x) % 3 for x in A[r]]
        for i in range(m):
            if i != r and A[i][c] % 3:
                f = A[i][c] % 3
                A[i] = [(A[i][j] - f*A[r][j]) % 3 for j in range(n)]
        r += 1
        if r == m:
            break
    return r


def main() -> int:
    pts = sorted({canon(v) for v in itertools.product(range(3), repeat=4) if any(v)})
    assert len(pts) == 40
    col = [[False]*40 for _ in range(40)]
    for i, j in itertools.combinations(range(40), 2):
        col[i][j] = col[j][i] = (symp(pts[i], pts[j]) == 0)
    deg = [sum(row) for row in col]
    assert set(deg) == {12}

    triads = []
    center_hist = {}
    span_center_hist = {}
    for t in itertools.combinations(range(40), 3):
        if any(col[i][j] for i, j in itertools.combinations(t, 2)):
            continue
        centers = sum(all(col[z][x] for x in t) for z in range(40) if z not in t)
        rk = rank3([pts[x] for x in t])
        triads.append(t)
        center_hist[centers] = center_hist.get(centers, 0) + 1
        span_center_hist[(rk, centers)] = span_center_hist.get((rk, centers), 0) + 1

    assert len(triads) == 3240
    assert center_hist == {1: 2880, 4: 360}
    assert span_center_hist == {(3, 1): 2880, (2, 4): 360}

    lines = set()
    for i, j in itertools.combinations(range(40), 2):
        vecs = set()
        for a, b in itertools.product(range(3), repeat=2):
            if a == b == 0:
                continue
            v = tuple((a*pts[i][k] + b*pts[j][k]) % 3 for k in range(4))
            if any(v):
                vecs.add(canon(v))
        assert len(vecs) == 4
        lines.add(tuple(sorted(pts.index(v) for v in vecs)))
    assert len(lines) == 130
    isotropic = [L for L in lines if all(col[i][j] for i,j in itertools.combinations(L,2))]
    nonisotropic = [L for L in lines if all(not col[i][j] for i,j in itertools.combinations(L,2))]
    assert len(isotropic) == 40
    assert len(nonisotropic) == 90
    four_center_from_lines = {tuple(sorted(t)) for L in nonisotropic for t in itertools.combinations(L,3)}
    four_center_direct = {t for t in triads if sum(all(col[z][x] for x in t) for z in range(40) if z not in t) == 4}
    assert len(four_center_from_lines) == 360
    assert four_center_from_lines == four_center_direct

    out = {
        "pass": 4953,
        "role": "standard W(3,3) point-graph baseline for duality correction",
        "standard_W33": {
            "model": "projective points of F3^4 with symplectic collinearity",
            "parameters": [40, 12, 2, 4],
        },
        "pairwise_noncollinear_triads": 3240,
        "common_neighbor_distribution": {
            "one_center": 2880,
            "four_centers": 360,
        },
        "span_classification": {
            "rank_3_span__one_center": 2880,
            "rank_2_span__four_centers": 360,
        },
        "projective_line_explanation": {
            "all_PG3_3_lines": 130,
            "isotropic_W33_lines": 40,
            "nonisotropic_lines": 90,
            "three_subsets_per_nonisotropic_line": 4,
            "four_center_triads": 360,
        },
        "duality_context": {
            "Pass4947_counts_0_2": "belong to the Steiner quotient identified in Pass4954 as the dual Q(4,3) point graph",
            "Pass4870_error": "the Steiner quotient was incorrectly promoted to the standard W(3,3) point graph"
        },
        "theorem": "In standard W(3,3), every pairwise noncollinear triple has exactly one or four common neighbors. The distribution is 2880 one-center and 360 four-center triples. The four-center triples are exactly the 3-subsets of the 90 non-isotropic projective lines.",
        "boundary": "This pass classifies the standard W(3,3) point graph only. Pass4954 separately identifies the Steiner quotient with the dual Q(4,3) line-intersection graph.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
