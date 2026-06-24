#!/usr/bin/env python3
"""BT1688 — exact character irreducibility certificate for Levi H1.

Instead of solving an 81x81 commutant directly, use the graph-chain character:
chi_H1(g) = fixed_edges(g) - fixed_vertices(g) + 1.
The exact group sum <chi,chi> = 1 certifies complex irreducibility.
"""
from __future__ import annotations

from collections import Counter, deque
import itertools
import json
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


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(len(p)))


def make_points() -> list[tuple[int, int, int, int]]:
    pts = []
    seen = set()
    for v in itertools.product(range(MOD), repeat=4):
        c = canonical_projective(v)
        if c is not None and c not in seen:
            seen.add(c)
            pts.append(c)  # type: ignore[arg-type]
    return sorted(pts)


def transvection_perm(v, pts, index, sign):
    perm = []
    for x in pts:
        s = symplectic_form(x, v)
        y = tuple((x[i] + sign * s * v[i]) % MOD for i in range(4))
        perm.append(index[canonical_projective(y)])  # type: ignore[index]
    return tuple(perm)


def projective_group(pts):
    index = {p: i for i, p in enumerate(pts)}
    gens = set()
    for v in pts:
        gens.add(transvection_perm(v, pts, index, 1))
        gens.add(transvection_perm(v, pts, index, 2))
    identity = tuple(range(len(pts)))
    group = {identity}
    queue = deque([identity])
    while queue:
        g = queue.popleft()
        for h in gens:
            hg = compose(h, g)
            if hg not in group:
                group.add(hg)
                queue.append(hg)
    return list(group)


def w33_lines(pts):
    graph = nx.Graph()
    graph.add_nodes_from(range(len(pts)))
    for i, j in itertools.combinations(range(len(pts)), 2):
        if symplectic_form(pts[i], pts[j]) == 0:
            graph.add_edge(i, j)
    return sorted(tuple(sorted(c)) for c in nx.find_cliques(graph) if len(c) == 4)


def main() -> None:
    pts = make_points()
    group = projective_group(pts)
    lines = w33_lines(pts)
    line_index = {line: i for i, line in enumerate(lines)}
    edges = [(p, li) for li, line in enumerate(lines) for p in line]
    char_sum_sq = 0
    distribution = Counter()
    for perm in group:
        fixed_points = sum(1 for i in range(40) if perm[i] == i)
        lperm = []
        for line in lines:
            new_line = tuple(sorted(perm[p] for p in line))
            lperm.append(line_index[new_line])
        fixed_lines = sum(1 for i, j in enumerate(lperm) if i == j)
        fixed_vertices = fixed_points + fixed_lines
        fixed_edges = sum(1 for p, li in edges if perm[p] == p and lperm[li] == li)
        chi = fixed_edges - fixed_vertices + 1
        distribution[chi] += 1
        char_sum_sq += chi * chi
    result = {
        "theorem": "BT1688 Exact H1 Character Irreducibility Certificate",
        "group": {"projective_order": len(group), "sp43_order": 51840, "center_kernel_size": 2},
        "levi_complex": {"points": 40, "lines": 40, "vertices": 80, "edges": 160, "h1_dimension": 81},
        "character_formula": "chi_H1(g) = fixed_incidence_edges(g) - fixed_vertices(g) + 1",
        "character_distribution": {str(k): distribution[k] for k in sorted(distribution)},
        "character_square_sum": char_sum_sq,
        "character_inner_product": f"{char_sum_sq}/{len(group)}",
        "character_inner_product_value": char_sum_sq / len(group),
        "conclusion": "Since <chi_H1, chi_H1> = 1, the 81-dimensional Levi H1 character is irreducible over C. Thus the BT1683 Schur step is unconditional over the complexified representation.",
        "boundary": "This is an exact character certificate for complex irreducibility of the generated projective symplectic action. It replaces the prior numeric-only irreducibility status."
    }
    assert len(group) == 25920
    assert char_sum_sq == len(group)
    out = Path("data/PART_BT1688_EXACT_H1_CHARACTER_IRREDUCIBILITY_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
