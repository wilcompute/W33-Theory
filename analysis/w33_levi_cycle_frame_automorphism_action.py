#!/usr/bin/env python3
"""BT557: W33 Levi Cycle Frame Automorphism Action Theorem.

Builds the symplectic polar model of W(3,3) over F_3^4, constructs its
point-line Levi flags, and lets the elementary symplectic transvections act on
those 160 flags.  The generated permutation group has order 25920, i.e.
|PSp(4,3)|=|W(E6)|/2, acts transitively on the 160 flags, and preserves the
Levi line-graph distance / cycle-frame inner-product shell.

This is intentionally a constructive action certificate, not a full nauty-style
automorphism enumeration.  It proves a large exact automorphism subgroup of the
160-point cycle frame and pins it to the expected W33 symplectic substrate.
"""

from __future__ import annotations

import collections
import itertools
import json
from pathlib import Path

MOD = 3


def canonical_projective(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(x % MOD for x in v)
    for a in v:
        if a:
            inv = 1 if a == 1 else 2
            return tuple((x * inv) % MOD for x in v)
    raise ValueError("zero vector")


def symplectic(u: tuple[int, int, int, int], v: tuple[int, int, int, int]) -> int:
    return (u[0] * v[2] + u[1] * v[3] - u[2] * v[0] - u[3] * v[1]) % MOD


def mat_vec(M: tuple[tuple[int, ...], ...], x: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(M[i][j] * x[j] for j in range(4)) % MOD for i in range(4))


def transvection(v: tuple[int, int, int, int], c: int = 1) -> tuple[tuple[int, ...], ...]:
    # T_v(x)=x+c*<x,v>v.  In characteristic 3 this is a symplectic transvection.
    columns = []
    for basis_idx in range(4):
        e = tuple(1 if i == basis_idx else 0 for i in range(4))
        bx = symplectic(e, v)
        col = tuple((e[i] + c * bx * v[i]) % MOD for i in range(4))
        columns.append(col)
    return tuple(tuple(columns[j][i] for j in range(4)) for i in range(4))


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(len(q)))


def closure(generators: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    identity = tuple(range(len(generators[0])))
    group = {identity}
    queue = collections.deque([identity])
    while queue:
        g = queue.popleft()
        for h in generators:
            hg = compose(h, g)
            if hg not in group:
                group.add(hg)
                queue.append(hg)
    return group


def main() -> dict:
    points = sorted({canonical_projective(v) for v in itertools.product(range(MOD), repeat=4) if any(v)})

    lines = set()
    for i, u in enumerate(points):
        for v in points[i + 1:]:
            if symplectic(u, v) != 0:
                continue
            line = tuple(sorted({
                canonical_projective(tuple(a * u[t] + b * v[t] for t in range(4)))
                for a, b in itertools.product(range(MOD), repeat=2)
                if (a, b) != (0, 0)
            }))
            if len(line) == 4:
                lines.add(line)
    lines = sorted(lines)

    flags = [(p, line) for line in lines for p in line]
    flag_index = {flag: i for i, flag in enumerate(flags)}

    def perm_from_matrix(M: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
        perm = []
        for p, line in flags:
            pp = canonical_projective(mat_vec(M, p))
            ll = tuple(sorted(canonical_projective(mat_vec(M, x)) for x in line))
            perm.append(flag_index[(pp, ll)])
        return tuple(perm)

    generators = list(dict.fromkeys(perm_from_matrix(transvection(v, 1)) for v in points))
    group = closure(generators)

    # Build Levi line graph distances on flags: flags adjacent if they share point or line.
    neighbors = [set() for _ in flags]
    for i, (p, line) in enumerate(flags):
        for j, (q, m) in enumerate(flags):
            if i < j and (p == q or line == m):
                neighbors[i].add(j)
                neighbors[j].add(i)

    def bfs_dist(src: int) -> list[int]:
        dist = [-1] * len(flags)
        dist[src] = 0
        dq = collections.deque([src])
        while dq:
            u = dq.popleft()
            for w in neighbors[u]:
                if dist[w] < 0:
                    dist[w] = dist[u] + 1
                    dq.append(w)
        return dist

    distance_rows = [bfs_dist(i) for i in range(len(flags))]
    distance_distribution = collections.Counter(distance_rows[0])

    # Verify generators preserve distances; group preservation follows by generation.
    generator_distance_preservation = []
    for perm in generators:
        ok = all(distance_rows[perm[i]][perm[j]] == distance_rows[i][j] for i in range(160) for j in range(160))
        generator_distance_preservation.append(ok)

    orbit = {g[0] for g in group}
    stabilizer_size = sum(1 for g in group if g[0] == 0)

    expected_order = 25920
    checks = {
        "points_40": len(points) == 40,
        "lines_40": len(lines) == 40,
        "flags_160": len(flags) == 160,
        "unique_transvection_generators_40": len(generators) == 40,
        "generated_group_order_PSp43": len(group) == expected_order,
        "flag_transitive": len(orbit) == 160,
        "flag_stabilizer_order": stabilizer_size == 162,
        "orbit_stabilizer": len(orbit) * stabilizer_size == len(group),
        "distance_distribution": dict(distance_distribution) == {0: 1, 1: 6, 2: 18, 3: 54, 4: 81},
        "generators_preserve_distance_shells": all(generator_distance_preservation),
        "order_is_half_WE6": 2 * len(group) == 51840,
    }

    result = {
        "theorem": "BT557 W33 Levi Cycle Frame Automorphism Action Theorem",
        "objects": {
            "projective_points": len(points),
            "isotropic_lines": len(lines),
            "levi_flags": len(flags),
            "transvection_generators": len(generators),
        },
        "group_action": {
            "generated_group_order": len(group),
            "identification": "PSp(4,3) acting on W33 Levi flags",
            "WE6_relation": "2*25920=51840=|W(E6)|",
            "flag_orbit_size": len(orbit),
            "flag_stabilizer_order": stabilizer_size,
            "orbit_stabilizer": f"{len(orbit)}*{stabilizer_size}={len(group)}",
        },
        "preserved_structure": {
            "line_graph_distance_distribution": dict(sorted(distance_distribution.items())),
            "cycle_frame_inner_products_by_distance": {
                "0": "1",
                "1": "-1/3",
                "2": "1/9",
                "3": "-1/27",
                "4": "1/81",
            },
            "preservation_certificate": "each symplectic transvection generator preserves the Levi line-graph distance matrix, hence the cycle-frame Gram shells",
        },
        "scope_note": "This is a constructive exact subgroup/action certificate, not a full graph-automorphism enumeration.  It proves at least PSp(4,3) of order 25920 acts faithfully and transitively on the 160-point cycle frame.",
        "all_identities": {k: bool(v) for k, v in checks.items()},
        "all_identities_hold": all(bool(v) for v in checks.values()),
    }
    out = Path("data/PART_BT557_W33_LEVI_CYCLE_FRAME_AUTOMORPHISM_ACTION_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()
