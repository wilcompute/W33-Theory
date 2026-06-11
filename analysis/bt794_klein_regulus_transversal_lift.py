#!/usr/bin/env python3
"""
BT794 - Klein/regulus lift for all 540 skew-line charts.

For every skew pair of totally isotropic W(3,3) lines:
  * there are exactly four common totally isotropic transversals;
  * the base pair plus those four transversals is the visible isotropic part of
    a Q+(3,3)-style grid;
  * the two same-ruling completion lines exist in PG(3,3), but are never
    totally isotropic.

This records the boundary: the regulus lift is real, but W33 sees a 6-line
isotropic shadow of an 8-line hyperbolic grid.
"""
from __future__ import annotations
from itertools import product, combinations
from collections import Counter
import json
from pathlib import Path

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
    return sorted({canon(v) for v in product(range(3), repeat=4) if v != (0, 0, 0, 0)})


def symp(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def all_projective_lines(pts, pt_index):
    out = set()
    for i, j in combinations(range(len(pts)), 2):
        p, q = pts[i], pts[j]
        line = set()
        for a, b in product(range(3), repeat=2):
            if a == 0 and b == 0:
                continue
            line.add(pt_index[canon(tuple((a*p[k] + b*q[k]) % 3 for k in range(4)))])
        out.add(frozenset(line))
    return list(out)


def is_isotropic(line, pts):
    return all(symp(pts[i], pts[j]) == 0 for i, j in combinations(line, 2))


def build_geometry():
    pts = points()
    pt_index = {p: i for i, p in enumerate(pts)}
    pg_lines = all_projective_lines(pts, pt_index)
    iso_lines = [line for line in pg_lines if is_isotropic(line, pts)]
    iso_lines.sort(key=lambda L: sorted(L))
    line_sets = [set(L) for L in iso_lines]
    pg_sets = [set(L) for L in pg_lines]
    pg_index = {L: i for i, L in enumerate(pg_lines)}
    iso_to_pg = [pg_index[frozenset(L)] for L in iso_lines]
    skew = [(i, j) for i, j in combinations(range(40), 2) if not (line_sets[i] & line_sets[j])]
    return pts, pg_lines, pg_sets, iso_lines, line_sets, iso_to_pg, skew


def main():
    pts, pg_lines, pg_sets, iso_lines, line_sets, iso_to_pg, skew = build_geometry()
    assert len(pts) == 40
    assert len(pg_lines) == 130
    assert len(iso_lines) == 40
    assert len(skew) == 540

    profile = Counter()
    examples = []
    for a, b in skew:
        trans = [k for k in range(40) if k not in (a, b) and line_sets[k] & line_sets[a] and line_sets[k] & line_sets[b]]
        trans_pg = [iso_to_pg[t] for t in trans]
        A, B = iso_to_pg[a], iso_to_pg[b]
        completions = [
            k for k in range(len(pg_lines))
            if k not in (A, B) and k not in trans_pg
            and not (pg_sets[k] & pg_sets[A]) and not (pg_sets[k] & pg_sets[B])
            and all(pg_sets[k] & pg_sets[t] for t in trans_pg)
        ]
        comp_iso = sum(1 for k in completions if is_isotropic(pg_lines[k], pts))
        trans_pairwise_skew = all(not (line_sets[i] & line_sets[j]) for i, j in combinations(trans, 2))
        full_grid_cross = all((pg_sets[x] & pg_sets[y]) for x in [A, B] + completions for y in trans_pg)
        same_ruling_skew = all(not (pg_sets[x] & pg_sets[y]) for x, y in combinations([A, B] + completions, 2))
        profile[(len(trans), len(completions), comp_iso, trans_pairwise_skew, full_grid_cross, same_ruling_skew)] += 1
        if len(examples) < 3:
            examples.append({
                "chart": [a, b],
                "isotropic_transversals": trans,
                "nonisotropic_completion_pg_line_indices": completions,
            })

    expected = {(4, 2, 0, True, True, True): 540}
    assert dict(profile) == expected
    out = {
        "theorem": "BT794 Klein regulus transversal lift",
        "charts": len(skew),
        "profile": {str(k): v for k, v in profile.items()},
        "uniform_result": {
            "common_isotropic_transversals_per_chart": 4,
            "same_ruling_completion_lines_per_chart_in_PG3_3": 2,
            "isotropic_completion_lines_per_chart": 0,
            "grid_cross_incidence_verified": True,
            "two_rulings_pairwise_skew_verified": True
        },
        "examples": examples,
        "interpretation": "Each W33 skew chart is a regulus shadow: W33 contains the base pair and four opposite-ruling isotropic transversals; the two missing same-ruling completion lines exist only outside the isotropic line set."
    }
    path = ROOT / "data" / "bt794_klein_regulus_transversal_lift.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
