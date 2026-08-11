#!/usr/bin/env python3
"""Pass4953 — correction of the Pass4947 W33 triad-center classification.

Pass4870 identifies the 40-fiber quotient explicitly with the standard
symplectic W(3,3) point graph.  In that graph, three pairwise noncollinear
projective points span either a 3-space or a nondegenerate projective line.
Their common perpendicular therefore has projective size 1 or 4, not 0 or 2.

This verifier constructs W(3,3) directly over F3, counts all independent
triads, and identifies the 360 four-center triads with the 90 non-isotropic
projective lines times four 3-subsets per line.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4953_CORRECT_W33_TRIAD_CENTERS.json"


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

    # Enumerate projective lines by 2-dimensional spans of pairs.
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
        "correction_target": "Pass4947 geometric center-count equivalence",
        "standard_W33": {
            "model": "projective points of F3^4 with symplectic collinearity",
            "parameters": [40, 12, 2, 4],
        },
        "pairwise_noncollinear_triads": 3240,
        "correct_common_neighbor_distribution": {
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
        "Pass4947_status": {
            "claimed_center_counts_0_and_2": "FALSE for standard W(3,3)",
            "raw_holonomy_counts_1080_2160": "not invalidated by this verifier, but their claimed equivalence to 0/2 center counts is invalid and requires recomputation",
        },
        "theorem": "In standard W(3,3), every pairwise noncollinear triple has exactly one or four common neighbors. The distribution is 2880 one-center and 360 four-center triples. The four-center triples are exactly the 3-subsets of the 90 non-isotropic projective lines.",
        "boundary": "This corrects only the geometric center classification in Pass4947. It does not yet recompute the S3 holonomy cross-tab against the correct 1/4-center classes.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
