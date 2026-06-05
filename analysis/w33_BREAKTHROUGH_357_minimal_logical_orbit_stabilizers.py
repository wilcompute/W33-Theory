#!/usr/bin/env python3
"""BT357: orbit-stabilizer theorem for minimal W33 CSS logicals.

The canonical W(3,3) edge CSS code has two minimal logical support families:

  * X_min: 160 isotropic line-stars;
  * Z_min: 1620 ordinary quadrangles.

This verifier generates the faithful projective symplectic action on the
40 W(3,3) points using symplectic transvections.  The generated group has
order 25920 = |PSp(4,3)| = |Omega(5,3)| and acts transitively on both
minimal support families.

Projective stabilizers:

  * |Stab(X_min)| = 25920 / 160  = 162 = 2 * 81;
  * |Stab(Z_min)| = 25920 / 1620 = 16  = 2^4.

Lifting to the double cover Sp(4,3) doubles these stabilizers to 324 and 32.
The Z double-cover stabilizer 32=2^(mu+1) is the same local obstruction
factor that appears in the selector-flatness counts.
"""
from __future__ import annotations

import json
from collections import deque
from itertools import combinations, product
from pathlib import Path
from typing import Iterable


P = 3
Q = 3
MU = 4
H1 = Q ** MU
PSP_ORDER = 25_920
SP_ORDER = 51_840

Vec = tuple[int, int, int, int]
Perm = tuple[int, ...]


def canonical(v: Iterable[int]) -> Vec:
    vv = tuple(int(x) % P for x in v)
    if vv == (0, 0, 0, 0):
        raise ValueError("zero vector")
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P for y in vv)  # type: ignore[return-value]
    raise AssertionError


def omega(u: Vec, v: Vec) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % P


def build_w33():
    points: list[Vec] = []
    seen: set[Vec] = set()
    for raw in product(range(P), repeat=4):
        if raw == (0, 0, 0, 0):
            continue
        c = canonical(raw)
        if c not in seen:
            seen.add(c)
            points.append(c)
    points = sorted(points)
    point_index = {p: i for i, p in enumerate(points)}

    edges = [(i, j) for i, j in combinations(range(len(points)), 2) if omega(points[i], points[j]) == 0]
    edge_index = {e: k for k, e in enumerate(edges)}

    lines: set[tuple[int, int, int, int]] = set()
    for i, j in edges:
        u, v = points[i], points[j]
        line = set()
        for a, b in product(range(P), repeat=2):
            if a == 0 and b == 0:
                continue
            line.add(point_index[canonical((a * u[t] + b * v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))

    adjacency = [[False] * len(points) for _ in points]
    for i, j in edges:
        adjacency[i][j] = adjacency[j][i] = True

    return points, edges, edge_index, sorted(lines), adjacency


def compose(p: Perm, q: Perm) -> Perm:
    """Permutation composition p after q."""

    return tuple(p[i] for i in q)


def transvection_permutations(points: list[Vec], point_index: dict[Vec, int]) -> list[Perm]:
    """Projective action of symplectic transvections x -> x + omega(x,v)v."""

    perms = []
    for v in points:
        perm = []
        for x in points:
            c = omega(x, v)
            y = tuple((x[t] + c * v[t]) % P for t in range(4))
            perm.append(point_index[canonical(y)])
        perms.append(tuple(perm))
    return perms


def generate_projective_symplectic_group(points: list[Vec]) -> set[Perm]:
    point_index = {p: i for i, p in enumerate(points)}
    gens = transvection_permutations(points, point_index)
    identity = tuple(range(len(points)))
    group = {identity}
    queue: deque[Perm] = deque([identity])
    while queue:
        g = queue.popleft()
        for s in gens:
            h = compose(s, g)
            if h not in group:
                group.add(h)
                queue.append(h)
    return group


def minimal_supports(lines, edges, edge_index, adjacency):
    x_supports = set()
    for line in lines:
        for p in line:
            support = tuple(sorted(edge_index[tuple(sorted((p, q)))] for q in line if q != p))
            x_supports.add(support)

    z_supports = set()
    for a, b in combinations(range(len(adjacency)), 2):
        if adjacency[a][b]:
            continue
        common = [x for x in range(len(adjacency)) if adjacency[a][x] and adjacency[b][x]]
        for c, d in combinations(common, 2):
            support = tuple(sorted(edge_index[tuple(sorted(e))] for e in ((a, c), (c, b), (b, d), (d, a))))
            z_supports.add(support)

    return x_supports, z_supports


def act_support(g: Perm, support: tuple[int, ...], edges, edge_index) -> tuple[int, ...]:
    out = []
    for edge_id in support:
        i, j = edges[edge_id]
        a, b = sorted((g[i], g[j]))
        out.append(edge_index[(a, b)])
    return tuple(sorted(out))


def orbit_data(group: set[Perm], supports: set[tuple[int, ...]], edges, edge_index) -> dict:
    base = next(iter(supports))
    orbit = {act_support(g, base, edges, edge_index) for g in group}
    stabilizer = sum(1 for g in group if act_support(g, base, edges, edge_index) == base)
    return {
        "support_count": len(supports),
        "orbit_size": len(orbit),
        "transitive": orbit == supports,
        "projective_stabilizer_order": stabilizer,
        "double_cover_stabilizer_order": 2 * stabilizer,
    }


def build_payload() -> dict:
    points, edges, edge_index, lines, adjacency = build_w33()
    group = generate_projective_symplectic_group(points)
    x_supports, z_supports = minimal_supports(lines, edges, edge_index, adjacency)
    x_orbit = orbit_data(group, x_supports, edges, edge_index)
    z_orbit = orbit_data(group, z_supports, edges, edge_index)

    identities = {
        "w33_counts": len(points) == 40 and len(edges) == 240 and len(lines) == 40,
        "projective_group_order": len(group) == PSP_ORDER,
        "x_support_count": len(x_supports) == 160,
        "z_support_count": len(z_supports) == 1620,
        "x_transitive": x_orbit["transitive"],
        "z_transitive": z_orbit["transitive"],
        "x_stabilizer_projective": x_orbit["projective_stabilizer_order"] == 162 == 2 * H1,
        "z_stabilizer_projective": z_orbit["projective_stabilizer_order"] == 16 == 2 ** MU,
        "x_stabilizer_double": x_orbit["double_cover_stabilizer_order"] == 324 == 4 * H1,
        "z_stabilizer_double": z_orbit["double_cover_stabilizer_order"] == 32 == 2 ** (MU + 1),
        "orbit_stabilizer_x": len(group) == len(x_supports) * x_orbit["projective_stabilizer_order"],
        "orbit_stabilizer_z": len(group) == len(z_supports) * z_orbit["projective_stabilizer_order"],
    }

    theorem = (
        "Minimal Logical Orbit-Stabilizer Theorem.  The faithful projective "
        "symplectic action PSp(4,3) generated by transvections has order "
        "25920 and acts transitively on both minimal CSS logical support "
        "families.  The 160 X_min line-star supports have projective "
        "stabilizer 162=2*81 and double-cover stabilizer 324=4*81.  The "
        "1620 Z_min quadrangle supports have projective stabilizer 16=2^4 "
        "and double-cover stabilizer 32=2^(mu+1)."
    )

    return {
        "summary": {
            "projective_group_order": len(group),
            "X_orbit_size": x_orbit["orbit_size"],
            "X_projective_stabilizer": x_orbit["projective_stabilizer_order"],
            "Z_orbit_size": z_orbit["orbit_size"],
            "Z_projective_stabilizer": z_orbit["projective_stabilizer_order"],
            "all_identities_hold": all(identities.values()),
        },
        "group": {
            "projective": "PSp(4,3) ~= Omega(5,3)",
            "projective_order": len(group),
            "double_cover": "Sp(4,3)",
            "double_cover_order": SP_ORDER,
            "generators": "40 projective symplectic transvections",
        },
        "X_min_orbit": {
            **x_orbit,
            "support_model": "isotropic line-stars",
            "closed_forms": {
                "support_count": "160 = 40 lines * 4 stars",
                "projective_stabilizer": "162 = 2 * 81",
                "double_cover_stabilizer": "324 = 4 * 81",
            },
        },
        "Z_min_orbit": {
            **z_orbit,
            "support_model": "ordinary quadrangles",
            "closed_forms": {
                "support_count": "1620 = 540 nonedges * C(4,2)/2",
                "projective_stabilizer": "16 = 2^mu",
                "double_cover_stabilizer": "32 = 2^(mu+1)",
            },
        },
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": (
            "This proves finite orbit-stabilizer facts for support sets.  It "
            "does not prove a physical braid representation or continuum TQFT."
        ),
    }


def main() -> int:
    payload = build_payload()
    out = Path("data/w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {out}")
    return 0 if payload["summary"]["all_identities_hold"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
