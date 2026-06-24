#!/usr/bin/env python3
"""BT1671 — automorphism-twirl bridge test for W33 Levi incidence edges.

We generate the projective symplectic action on W(3,3) points using symplectic
transvections over F_3.  The projective action has order 25920; its lift is the
usual |Sp(4,3)|=51840 with center acting trivially on projective points.

The key test: the orbit of one Levi incidence edge under this action has size
160, so the automorphism twirl of any edge-supported bridge is uniform on all
W33 Levi incidence edges.
"""
from __future__ import annotations

import itertools
import json
from collections import deque
from pathlib import Path

import networkx as nx

MOD = 3


def canonical_projective(v: tuple[int, ...]) -> tuple[int, ...] | None:
    vv = tuple(x % MOD for x in v)
    if all(x == 0 for x in vv):
        return None
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % MOD for y in vv)
    raise AssertionError("unreachable")


def symplectic_form(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> int:
    return (a[0] * b[2] + a[1] * b[3] - a[2] * b[0] - a[3] * b[1]) % MOD


def points() -> list[tuple[int, int, int, int]]:
    out = []
    seen = set()
    for v in itertools.product(range(MOD), repeat=4):
        c = canonical_projective(v)
        if c is not None and c not in seen:
            seen.add(c)
            out.append(c)  # type: ignore[arg-type]
    return sorted(out)


def transvection_perm(v: tuple[int, int, int, int], pts: list[tuple[int, int, int, int]], index: dict[tuple[int, int, int, int], int], sign: int) -> tuple[int, ...]:
    perm = []
    for x in pts:
        s = symplectic_form(x, v)
        y = tuple((x[i] + sign * s * v[i]) % MOD for i in range(4))
        perm.append(index[canonical_projective(y)])  # type: ignore[index]
    return tuple(perm)


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(len(p)))


def projective_symplectic_group() -> tuple[list[tuple[int, ...]], list[tuple[int, int, int, int]]]:
    pts = points()
    index = {p: i for i, p in enumerate(pts)}
    gens = set()
    for v in pts:
        gens.add(transvection_perm(v, pts, index, 1))
        gens.add(transvection_perm(v, pts, index, 2))
    identity = tuple(range(len(pts)))
    group = {identity}
    queue: deque[tuple[int, ...]] = deque([identity])
    while queue:
        g = queue.popleft()
        for h in gens:
            hg = compose(h, g)
            if hg not in group:
                group.add(hg)
                queue.append(hg)
    return list(group), pts


def w33_lines(pts: list[tuple[int, int, int, int]]) -> list[tuple[int, int, int, int]]:
    graph = nx.Graph()
    graph.add_nodes_from(range(len(pts)))
    for i, j in itertools.combinations(range(len(pts)), 2):
        if symplectic_form(pts[i], pts[j]) == 0:
            graph.add_edge(i, j)
    lines = [tuple(sorted(c)) for c in nx.find_cliques(graph) if len(c) == 4]
    return sorted(lines)


def main() -> None:
    group, pts = projective_symplectic_group()
    lines = w33_lines(pts)
    line_index = {line: i for i, line in enumerate(lines)}
    incidences = [(p, li) for li, line in enumerate(lines) for p in line]

    edge0 = incidences[0]
    edge_orbit = set()
    point_orbit = set()
    line_orbit = set()
    p0, l0 = edge0
    for perm in group:
        point_orbit.add(perm[p0])
        new_line = tuple(sorted(perm[p] for p in lines[l0]))
        line_orbit.add(line_index[new_line])
        edge_orbit.add((perm[p0], line_index[new_line]))

    result = {
        "theorem": "BT1671 Automorphism-Twirl Bridge Theorem",
        "group": {
            "projective_action_order": len(group),
            "sp43_order": 51840,
            "center_kernel_size": 2,
            "generators": "symplectic transvections over F3, projectivized",
        },
        "w33_levi": {
            "points": len(pts),
            "lines": len(lines),
            "incidence_edges": len(incidences),
        },
        "orbits": {
            "point_orbit_size": len(point_orbit),
            "line_orbit_size": len(line_orbit),
            "incidence_edge_orbit_size": len(edge_orbit),
        },
        "twirl_conclusion": {
            "edge_twirl": "uniform over all 160 W33 Levi incidence edges",
            "vertex_twirl": "uniform on 40 points and uniform on 40 lines separately under the projective symplectic action",
            "bridge_mean_edge_weight_for_64_edge_events": 64 / 160,
        },
        "boundary": "This automorphism twirl does not produce a sparse 8-cycle embedding. It collapses the bridge support to the uniform incidence-edge idempotent. Dualities that swap points and lines are not needed for the incidence-edge transitivity test.",
    }
    assert result["group"]["projective_action_order"] == 25920
    assert result["orbits"]["point_orbit_size"] == 40
    assert result["orbits"]["line_orbit_size"] == 40
    assert result["orbits"]["incidence_edge_orbit_size"] == 160
    out = Path("data/PART_BT1671_AUTOMORPHISM_TWIRL_BRIDGE_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
