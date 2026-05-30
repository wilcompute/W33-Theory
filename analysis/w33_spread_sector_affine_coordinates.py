#!/usr/bin/env python3
"""Affine F3^2 coordinates for spread-sector labels.

Previous verifier:
  For fixed anchor p, anchor line L, and allowed direction d in p^perp\L,
  the 9 spreads containing L biject with the 9 affine lines of direction d in
  AG(3,3).

This verifier adds coordinates.  In an affine chart at p, the 27-point affine
bulk is F3^3.  A direction d is a nonzero vector in the tangent hyperplane.
The 9 parallel affine lines of direction d are the cosets of <d>, i.e.

    F3^3 / <d> ~= F3^2.

For each allowed direction, choose two linear functionals that annihilate d.
They assign a quotient label in F3^2 to every affine line parallel to d.
The theorem checks that, in every anchor-line sector and every allowed direction,

the 9 spreads realize all 9 labels in F3^2 exactly once.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
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


def inv3(x: int) -> int:
    x %= q
    if x == 1:
        return 1
    if x == 2:
        return 2
    raise ValueError("0 has no inverse")


def normalize(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(x % q for x in v)
    i = next(i for i, x in enumerate(v) if x)
    inv = inv3(v[i])
    return tuple((inv * x) % q for x in v)


def sub(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((x - y) % q for x, y in zip(a, b))


def dot(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x * y for x, y in zip(a, b)) % q


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


def affine_chart(points: list[tuple[int, ...]], anchor_index: int, hyperplane: set[int]) -> dict[int, tuple[int, ...]]:
    """Coordinates for affine complement PG(3,3) \ p^perp.

    We choose the anchor vector p as the chart normal.  Any affine point x has
    symplectic pairing with p nonzero; scaling x so <p,x>=1 gives a vector of
    the form x0 + tangent.  Differences of normalized affine points lie in the
    3D tangent hyperplane p^perp / <p>.  We keep 4D representatives; quotient
    labels are computed by linear functionals that annihilate p and direction d.
    """
    p = points[anchor_index]

    def symp(a: tuple[int, ...], b: tuple[int, ...]) -> int:
        return (a[0] * b[2] + a[1] * b[3] - a[2] * b[0] - a[3] * b[1]) % q

    coords = {}
    for idx, x in enumerate(points):
        if idx in hyperplane:
            continue
        s = symp(p, x)
        scale = inv3(s)
        coords[idx] = tuple((scale * t) % q for t in x)
    return coords


def direction_vector(points: list[tuple[int, ...]], direction_index: int, anchor_index: int) -> tuple[int, ...]:
    # Direction point lies in p^perp.  Use the projective representative itself;
    # functionals below also annihilate p, so this represents a tangent direction.
    return points[direction_index]


def annihilator_functionals(p: tuple[int, ...], d: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return two independent linear functionals l with l(p)=l(d)=0."""
    candidates = list(itertools.product(range(q), repeat=4))
    good = [c for c in candidates if any(c) and dot(c, p) == 0 and dot(c, d) == 0]
    for a, b in itertools.combinations(good, 2):
        if rank_mod3([a, b]) == 2:
            return a, b
    raise RuntimeError("no annihilator basis")


def line_label(line: tuple[int, ...], affine_coords: dict[int, tuple[int, ...]], functionals: tuple[tuple[int, ...], tuple[int, ...]]) -> tuple[int, int]:
    affine_members = [idx for idx in line if idx in affine_coords]
    if len(affine_members) != 3:
        raise ValueError("expected affine line with 3 affine points")
    labels = {tuple(dot(f, affine_coords[idx]) for f in functionals) for idx in affine_members}
    if len(labels) != 1:
        raise AssertionError(f"label not constant on line: {labels}")
    return next(iter(labels))


def analyze(anchor_index: int = 0) -> dict[str, Any]:
    points = projective_points()
    lines = isotropic_lines(points, projective_lines(points))
    spreads = symplectic_spreads(lines, n_points=len(points))
    hyperplane = set(point_perp(anchor_index, points))
    affine_points = set(range(len(points))) - hyperplane
    chart = affine_chart(points, anchor_index, hyperplane)
    anchor_lines = [i for i, line in enumerate(lines) if anchor_index in line]

    sector_records = []
    all_ok = []
    for anchor_line_index in anchor_lines:
        anchor_line = set(lines[anchor_line_index])
        directions = sorted(hyperplane - anchor_line)
        sector = [spread for spread in spreads if anchor_line_index in spread]
        direction_records = []
        for direction_index in directions:
            d = direction_vector(points, direction_index, anchor_index)
            fs = annihilator_functionals(points[anchor_index], d)
            parallel_lines = [
                i for i, line in enumerate(lines)
                if direction_index in line
                and len(set(line) & affine_points) == 3
                and len(set(line) & hyperplane) == 1
            ]
            all_line_labels = {line_label(lines[i], chart, fs) for i in parallel_lines}
            spread_labels = []
            for spread in sector:
                chosen = [i for i in spread if i in parallel_lines]
                if len(chosen) != 1:
                    spread_labels.append(None)
                else:
                    spread_labels.append(line_label(lines[chosen[0]], chart, fs))
            label_counter = Counter(spread_labels)
            expected = set(itertools.product(range(q), repeat=2))
            ok = set(spread_labels) == expected and all(v == 1 for v in label_counter.values()) and all_line_labels == expected
            direction_records.append(
                {
                    "direction_index": direction_index,
                    "functionals": [fs[0], fs[1]],
                    "parallel_line_count": len(parallel_lines),
                    "line_label_set_size": len(all_line_labels),
                    "spread_label_distribution": {str(k): v for k, v in label_counter.items()},
                    "ok": ok,
                }
            )
            all_ok.append(ok)
        sector_records.append(
            {
                "anchor_line_index": anchor_line_index,
                "sector_size": len(sector),
                "direction_count": len(directions),
                "all_direction_coordinates_ok": all(r["ok"] for r in direction_records),
                "direction_records": direction_records,
            }
        )
    return {
        "anchor_index": anchor_index,
        "point_count": len(points),
        "line_count": len(lines),
        "spread_count": len(spreads),
        "hyperplane_size": len(hyperplane),
        "affine_size": len(affine_points),
        "anchor_line_count": len(anchor_lines),
        "sector_records": sector_records,
        "all_coordinate_bijections_hold": all(all_ok),
    }


def build_payload() -> dict[str, Any]:
    canonical = analyze(0)
    identities = {
        "base_counts": canonical["point_count"] == 40 and canonical["line_count"] == 40 and canonical["spread_count"] == 36,
        "local_shell_13_27": canonical["hyperplane_size"] == 13 and canonical["affine_size"] == 27,
        "four_anchor_lines": canonical["anchor_line_count"] == 4,
        "all_coordinate_bijections_hold": canonical["all_coordinate_bijections_hold"],
    }
    return {
        "theorem": "spread_sector_affine_coordinates",
        "statement": "Every anchor-line sector and allowed affine direction gives an explicit F3^2 coordinate system on the nine spread labels.",
        "canonical_anchor": canonical,
        "interpretation": {
            "quotient": "parallel affine lines of fixed direction d are cosets of <d>, hence AG(3,3)/d ~= F3^2",
            "coordinate_test": "two annihilating functionals label those cosets; the nine spreads in the sector realize every F3^2 label exactly once",
            "bridge": "this upgrades 36=4*9 from count to four memory-line sectors times explicit affine F3^2 coordinate labels",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_spread_sector_affine_coordinates.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
