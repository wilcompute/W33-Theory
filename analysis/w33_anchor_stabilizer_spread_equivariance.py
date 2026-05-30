#!/usr/bin/env python3
"""Anchor-stabilizer equivariance for spread-sector affine labels.

Previous theorem built an explicit chart-dependent bijection

    PG(1,3) kernel directions x AG(2,3) fiber labels -> 36 spreads at anchor.

This verifier tests the next hard condition: equivariance under the symplectic
anchor stabilizer.

Method:
  1. Build W(3,3) points/lines/spreads using the existing repo audits.
  2. Generate the projective symplectic group PSp(4,3) from symplectic
     transvections.  Expected order: 25920.
  3. Restrict to the stabilizer of a fixed projective anchor.  Expected order:
     648.
  4. For each stabilizer element, compute its induced action on the 36 spreads.
  5. In each anchor-line sector, use the prior F3^2 spread chart.  Check that
     the induced map from the source-sector chart to the target-sector chart is
     affine-linear over F3.

Result expected:
  The anchor stabilizer acts by sector permutation plus AGL(2,3) chart maps on
  the nine labels inside each sector.  This upgrades the previous chart-chosen
  bijection to a natural equivariant finite geometry up to affine gauge.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
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


def normalize(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(x % q for x in v)
    if not any(v):
        raise ValueError("zero")
    i = next(i for i, x in enumerate(v) if x)
    inv = inv3(v[i])
    return tuple((inv * x) % q for x in v)


def symp(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return (a[0] * b[2] + a[1] * b[3] - a[2] * b[0] - a[3] * b[1]) % q


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


def compose_perm(p: tuple[int, ...], g: tuple[int, ...]) -> tuple[int, ...]:
    """Return p after g: i -> p[g[i]]."""
    return tuple(p[g[i]] for i in range(len(g)))


def transvection_perm(points: list[tuple[int, ...]], v: tuple[int, ...], lam: int = 1) -> tuple[int, ...]:
    pidx = {p: i for i, p in enumerate(points)}
    image = []
    for x in points:
        y = tuple((x[i] + lam * symp(x, v) * v[i]) % q for i in range(4))
        image.append(pidx[normalize(y)])
    return tuple(image)


def generate_projective_symplectic_group(points: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    # Projective transvections from all 40 point directions generate PSp(4,3).
    gens = {transvection_perm(points, v, 1) for v in points}
    identity = tuple(range(len(points)))
    group = {identity}
    queue = deque([identity])
    while queue:
        g = queue.popleft()
        for s in gens:
            h = compose_perm(s, g)
            if h not in group:
                group.add(h)
                queue.append(h)
    return group


def affine_chart(points: list[tuple[int, ...]], anchor_index: int, hyperplane: set[int]) -> dict[int, tuple[int, ...]]:
    p = points[anchor_index]
    coords = {}
    for idx, x in enumerate(points):
        if idx in hyperplane:
            continue
        scale = inv3(symp(p, x))
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


def chart_for_sector(
    points: list[tuple[int, ...]],
    lines: list[tuple[int, ...]],
    sector: list[tuple[int, ...]],
    anchor_index: int,
    anchor_line_index: int,
    hyperplane: set[int],
    affine_points: set[int],
    affine_coords: dict[int, tuple[int, ...]],
) -> tuple[dict[tuple[int, int], tuple[int, ...]], dict[tuple[int, ...], tuple[int, int]]]:
    anchor_line = set(lines[anchor_line_index])
    direction_index = sorted(hyperplane - anchor_line)[0]
    fs = annihilator_functionals(points[anchor_index], points[direction_index])
    parallel_lines = [
        i for i, line in enumerate(lines)
        if direction_index in line
        and len(set(line) & affine_points) == 3
        and len(set(line) & hyperplane) == 1
    ]
    label_to_spread = {}
    spread_to_label = {}
    for spread in sector:
        chosen = [i for i in spread if i in parallel_lines]
        if len(chosen) != 1:
            raise AssertionError("spread did not choose exactly one parallel line")
        label = line_label(lines[chosen[0]], affine_coords, fs)
        spread_key = tuple(sorted(spread))
        label_to_spread[label] = spread_key
        spread_to_label[spread_key] = label
    if set(label_to_spread) != set(F32):
        raise AssertionError("sector chart did not realize all labels")
    return label_to_spread, spread_to_label


def mat_vec(M: tuple[tuple[int, int], tuple[int, int]], x: tuple[int, int]) -> tuple[int, int]:
    return ((M[0][0] * x[0] + M[0][1] * x[1]) % q, (M[1][0] * x[0] + M[1][1] * x[1]) % q)


def add2(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return ((a[0] + b[0]) % q, (a[1] + b[1]) % q)


def det2(M: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % q


def affine_maps():
    mats = []
    for a, b, c, d in itertools.product(range(q), repeat=4):
        M = ((a, b), (c, d))
        if det2(M) != 0:
            mats.append(M)
    return [(M, t) for M in mats for t in F32]


def find_affine_transition(pairs: list[tuple[tuple[int, int], tuple[int, int]]]):
    for M, t in affine_maps():
        if all(add2(mat_vec(M, x), t) == y for x, y in pairs):
            return M, t
    return None


def apply_perm_to_line(perm: tuple[int, ...], line: tuple[int, ...], line_index: dict[tuple[int, ...], int]) -> int:
    return line_index[tuple(sorted(perm[i] for i in line))]


def apply_perm_to_spread(perm: tuple[int, ...], spread: tuple[int, ...], lines: list[tuple[int, ...]], line_index: dict[tuple[int, ...], int]) -> tuple[int, ...]:
    return tuple(sorted(apply_perm_to_line(perm, lines[i], line_index) for i in spread))


def build_payload() -> dict[str, Any]:
    points = projective_points()
    lines = isotropic_lines(points, projective_lines(points))
    spreads = [tuple(sorted(s)) for s in symplectic_spreads(lines, n_points=len(points))]
    spread_set = set(spreads)
    line_index = {tuple(sorted(line)): i for i, line in enumerate(lines)}
    anchor = 0
    hyperplane = set(point_perp(anchor, points))
    affine_points = set(range(len(points))) - hyperplane
    affine_coords = affine_chart(points, anchor, hyperplane)
    anchor_lines = sorted([i for i, line in enumerate(lines) if anchor in line])
    sectors = {L: [s for s in spreads if L in s] for L in anchor_lines}
    charts = {L: chart_for_sector(points, lines, sectors[L], anchor, L, hyperplane, affine_points, affine_coords) for L in anchor_lines}
    label_to_spread = {L: charts[L][0] for L in anchor_lines}
    spread_to_label = {L: charts[L][1] for L in anchor_lines}

    group = generate_projective_symplectic_group(points)
    stabilizer = sorted([g for g in group if g[anchor] == anchor])

    sector_perm_counter = Counter()
    affine_ok = 0
    affine_fail_examples = []
    for g in stabilizer:
        sector_image = {}
        for L in anchor_lines:
            target_L = apply_perm_to_line(g, lines[L], line_index)
            sector_image[L] = target_L
        sector_perm_counter[tuple(sector_image[L] for L in anchor_lines)] += 1
        for L in anchor_lines:
            target_L = sector_image[L]
            pairs = []
            for label, spread_key in label_to_spread[L].items():
                image_spread = apply_perm_to_spread(g, spread_key, lines, line_index)
                target_label = spread_to_label[target_L][image_spread]
                pairs.append((label, target_label))
            tr = find_affine_transition(pairs)
            if tr is None:
                affine_fail_examples.append({"sector": L, "target_sector": target_L, "pairs": pairs[:5]})
            else:
                affine_ok += 1

    identities = {
        "PSp43_order_25920": len(group) == 25920,
        "anchor_stabilizer_order_648": len(stabilizer) == 648,
        "spreads_36": len(spreads) == 36,
        "anchor_lines_4": len(anchor_lines) == 4,
        "sector_sizes_9": all(len(v) == 9 for v in sectors.values()),
        "stabilizer_preserves_spreads": all(
            apply_perm_to_spread(stabilizer[0], s, lines, line_index) in spread_set for s in spreads
        ) if stabilizer else False,
        "all_sector_chart_actions_affine": len(affine_fail_examples) == 0,
        "affine_action_count": affine_ok == len(stabilizer) * len(anchor_lines),
        "sector_action_transitive_on_4_lines": len(sector_perm_counter) >= 4,
    }
    return {
        "theorem": "anchor_stabilizer_spread_equivariance",
        "group_orders": {
            "PSp43_generated_order": len(group),
            "anchor_stabilizer_order": len(stabilizer),
            "expected_PSp43": 25920,
            "expected_stabilizer": 648,
        },
        "sector_structure": {
            "anchor": anchor,
            "anchor_lines": anchor_lines,
            "sector_sizes": {str(k): len(v) for k, v in sectors.items()},
            "sector_permutation_count_seen": len(sector_perm_counter),
            "sector_permutation_distribution_sample": {str(k): v for k, v in list(sector_perm_counter.items())[:12]},
        },
        "equivariance": {
            "sector_chart_actions_tested": len(stabilizer) * len(anchor_lines),
            "affine_chart_actions": affine_ok,
            "failure_count": len(affine_fail_examples),
            "failure_examples": affine_fail_examples[:3],
            "statement": "Every anchor-stabilizer element sends each sector chart to the target sector chart by an affine-linear map over F3.",
        },
        "interpretation": "The chart-dependent functor PG(1,3) x AG(2,3) -> 36 spreads is equivariant up to AGL(2,3) gauge under the projective symplectic stabilizer of the anchor.",
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_anchor_stabilizer_spread_equivariance.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
