#!/usr/bin/env python3
"""Affine chart-transition test for the nine spread labels in each sector.

Previous theorem:
  For fixed anchor p, anchor-line sector L, and allowed direction d in p^perp\L,
  the nine spreads containing L are labeled by F3^2 via the quotient AG(3,3)/<d>.

This verifier tests the stronger coordinate claim:
  The nine spreads in one sector carry a genuine affine-plane structure.  Any
  allowed direction d gives one F3^2 coordinate chart on the same nine spreads,
  and every transition between two such charts is an affine-linear bijection
  of F3^2.

That is exactly the structure needed to identify the sector label set with the
9-point affine fiber in the projection PG(5,3)->PG(3,3), up to affine gauge.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts"):
    s = str(candidate)
    if s not in sys.path:
        sys.path.insert(0, s)

from scripts.w33_projective_affine_shell_audit import (  # noqa: E402
    isotropic_lines,
    point_perp,
    projective_lines,
    projective_points,
)
from scripts.w33_symplectic_spread_frame_audit import symplectic_spreads  # noqa: E402

q = 3
F32 = list(itertools.product(range(q), repeat=2))


def inv3(x: int) -> int:
    x %= q
    if x == 1:
        return 1
    if x == 2:
        return 2
    raise ValueError("zero has no inverse")


def dot(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x * y for x, y in zip(a, b)) % q


def mat_vec(M: tuple[tuple[int, int], tuple[int, int]], x: tuple[int, int]) -> tuple[int, int]:
    return ((M[0][0] * x[0] + M[0][1] * x[1]) % q, (M[1][0] * x[0] + M[1][1] * x[1]) % q)


def add2(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return ((a[0] + b[0]) % q, (a[1] + b[1]) % q)


def det2(M: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % q


def gl23() -> list[tuple[tuple[int, int], tuple[int, int]]]:
    mats = []
    for a, b, c, d in itertools.product(range(q), repeat=4):
        M = ((a, b), (c, d))
        if det2(M) != 0:
            mats.append(M)
    return mats


def affine_maps() -> list[tuple[tuple[tuple[int, int], tuple[int, int]], tuple[int, int]]]:
    return [(M, t) for M in gl23() for t in F32]


def rank_mod3(rows: list[tuple[int, ...]]) -> int:
    A = [list(r) for r in rows if any(x % q for x in r)]
    if not A:
        return 0
    m, n = len(A), len(A[0])
    rank = 0
    col = 0
    while rank < m and col < n:
        piv = next((i for i in range(rank, m) if A[i][col] % q), None)
        if piv is None:
            col += 1
            continue
        A[rank], A[piv] = A[piv], A[rank]
        inv = inv3(A[rank][col])
        A[rank] = [(x * inv) % q for x in A[rank]]
        for i in range(m):
            if i != rank and A[i][col] % q:
                fac = A[i][col] % q
                A[i] = [(x - fac * y) % q for x, y in zip(A[i], A[rank])]
        rank += 1
        col += 1
    return rank


def symp(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return (a[0] * b[2] + a[1] * b[3] - a[2] * b[0] - a[3] * b[1]) % q


def affine_chart(points: list[tuple[int, ...]], anchor_index: int, hyperplane: set[int]) -> dict[int, tuple[int, ...]]:
    p = points[anchor_index]
    coords = {}
    for idx, x in enumerate(points):
        if idx in hyperplane:
            continue
        s = symp(p, x)
        scale = inv3(s)
        coords[idx] = tuple((scale * t) % q for t in x)
    return coords


def annihilator_functionals(p: tuple[int, ...], d: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    candidates = list(itertools.product(range(q), repeat=4))
    good = [c for c in candidates if any(c) and dot(c, p) == 0 and dot(c, d) == 0]
    for a, b in itertools.combinations(good, 2):
        if rank_mod3([a, b]) == 2:
            return a, b
    raise RuntimeError("no annihilator basis")


def line_label(line: tuple[int, ...], affine_coords: dict[int, tuple[int, ...]], functionals: tuple[tuple[int, ...], tuple[int, ...]]) -> tuple[int, int]:
    members = [idx for idx in line if idx in affine_coords]
    labels = {tuple(dot(f, affine_coords[idx]) for f in functionals) for idx in members}
    if len(labels) != 1:
        raise AssertionError(f"line label not constant: {labels}")
    return next(iter(labels))


def chart_for_direction(
    points: list[tuple[int, ...]],
    lines: list[tuple[int, ...]],
    sector: list[tuple[int, ...]],
    direction_index: int,
    anchor_index: int,
    hyperplane: set[int],
    affine_points: set[int],
    affine_coords: dict[int, tuple[int, ...]],
) -> dict[int, tuple[int, int]]:
    p = points[anchor_index]
    d = points[direction_index]
    fs = annihilator_functionals(p, d)
    parallel_lines = [
        i for i, line in enumerate(lines)
        if direction_index in line
        and len(set(line) & affine_points) == 3
        and len(set(line) & hyperplane) == 1
    ]
    spread_to_label: dict[int, tuple[int, int]] = {}
    for spread_index, spread in enumerate(sector):
        chosen = [i for i in spread if i in parallel_lines]
        if len(chosen) != 1:
            raise AssertionError("spread did not choose exactly one parallel line")
        spread_to_label[spread_index] = line_label(lines[chosen[0]], affine_coords, fs)
    if set(spread_to_label.values()) != set(F32):
        raise AssertionError("chart does not realize all F3^2 labels")
    return spread_to_label


def find_affine_transition(source: dict[int, tuple[int, int]], target: dict[int, tuple[int, int]]):
    pairs = [(source[i], target[i]) for i in sorted(source)]
    for M, t in affine_maps():
        if all(add2(mat_vec(M, x), t) == y for x, y in pairs):
            return M, t
    return None


def analyze(anchor_index: int = 0) -> dict[str, Any]:
    points = projective_points()
    lines = isotropic_lines(points, projective_lines(points))
    spreads = symplectic_spreads(lines, n_points=len(points))
    hyperplane = set(point_perp(anchor_index, points))
    affine_points = set(range(len(points))) - hyperplane
    affine_coords = affine_chart(points, anchor_index, hyperplane)
    anchor_lines = [i for i, line in enumerate(lines) if anchor_index in line]

    sector_records = []
    transition_counts = Counter()
    all_ok = []
    for anchor_line_index in anchor_lines:
        anchor_line = set(lines[anchor_line_index])
        directions = sorted(hyperplane - anchor_line)
        sector = [spread for spread in spreads if anchor_line_index in spread]
        charts = {
            d: chart_for_direction(points, lines, sector, d, anchor_index, hyperplane, affine_points, affine_coords)
            for d in directions
        }
        transitions = []
        for d1, d2 in itertools.permutations(directions, 2):
            tr = find_affine_transition(charts[d1], charts[d2])
            ok = tr is not None
            all_ok.append(ok)
            transition_counts["affine" if ok else "non_affine"] += 1
            if ok and len(transitions) < 12:
                M, t = tr
                transitions.append({"from": d1, "to": d2, "matrix": M, "translation": t})
        sector_records.append(
            {
                "anchor_line_index": anchor_line_index,
                "sector_size": len(sector),
                "direction_count": len(directions),
                "transition_count": len(directions) * (len(directions) - 1),
                "all_transitions_affine": all(find_affine_transition(charts[d1], charts[d2]) is not None for d1, d2 in itertools.permutations(directions, 2)),
                "sample_transitions": transitions,
            }
        )
    return {
        "anchor_index": anchor_index,
        "point_count": len(points),
        "line_count": len(lines),
        "spread_count": len(spreads),
        "anchor_line_count": len(anchor_lines),
        "sector_records": sector_records,
        "transition_counts": dict(transition_counts),
        "all_chart_transitions_affine": all(all_ok),
    }


def build_payload() -> dict[str, Any]:
    canonical = analyze(0)
    identities = {
        "base_counts": canonical["point_count"] == 40 and canonical["line_count"] == 40 and canonical["spread_count"] == 36,
        "four_sectors": canonical["anchor_line_count"] == 4,
        "all_transitions_affine": canonical["all_chart_transitions_affine"],
        "expected_transition_count": canonical["transition_counts"] == {"affine": 4 * 9 * 8},
    }
    return {
        "theorem": "spread_sector_chart_transition_affinity",
        "statement": "All F3^2 coordinate charts on the nine spreads in a fixed sector differ by affine-linear transformations over F3.",
        "canonical_anchor": canonical,
        "interpretation": {
            "sector_label_set": "the nine spreads in a sector are not merely a 9-element set; they form an affine plane over F3 up to affine gauge",
            "projection_fiber_bridge": "this is the same affine-plane structure carried by each 9-point fiber in PG(5,3)->PG(3,3)",
            "gauge_group": "chart changes lie in AGL(2,3), order 432",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_spread_sector_chart_transition_affinity.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
