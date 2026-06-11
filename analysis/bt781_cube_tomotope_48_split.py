#!/usr/bin/env python3
"""
BT781 - The order-48 cube/tomotope half-split.

Prompt: the BT780 base cube-chart stabilizer has order 48, exactly half of
the tomotope edge symmetry group of order 96.  Is it the same 48?

Answer: no, and the failure is the breakthrough.  The cube-chart stabilizer
and the tomotope derived subgroup are two complementary order-48 halves:

    cube chart half:        2^3 : S3     = 8 * 6  = 48
    tomotope chiral half:   2^4 : C3     = 16 * 3 = 48

The cube keeps the full S3 permutation of the three Q3 coordinate matchings,
with only three binary translation bits.  The tomotope derived half keeps four
binary bits but only oriented triality C3.  So passing from chart transport to
tomotope chirality trades one binary bit for one reflection bit.
"""
from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
import json
from pathlib import Path

import networkx as nx


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
    return sorted({
        canon((a, b, c, d))
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a, b, c, d) != (0, 0, 0, 0)
    })


def symp(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(g):
    out = [0]*len(g)
    for i, j in enumerate(g):
        out[j] = i
    return tuple(out)


def order(g):
    ident = tuple(range(len(g)))
    cur = g
    n = 1
    while cur != ident:
        cur = compose(g, cur)
        n += 1
    return n


def closure(gens, n):
    ident = tuple(range(n))
    group = {ident}
    frontier = deque([ident])
    while frontier:
        g = frontier.popleft()
        for h in gens:
            gh = compose(h, g)
            if gh not in group:
                group.add(gh)
                frontier.append(gh)
    return group


def derived_subgroup(group):
    elems = list(group)
    gens = set()
    for a in elems:
        ia = inverse(a)
        for b in elems:
            ib = inverse(b)
            gens.add(compose(compose(compose(ia, ib), a), b))
    return closure(list(gens), len(elems[0]))


def dist(group):
    return {str(k): v for k, v in sorted(Counter(order(g) for g in group).items())}


def build_w33_chart_stabilizer():
    pts = points()
    pt_index = {p: i for i, p in enumerate(pts)}
    n = 40
    adj = [[False]*n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [frozenset(q) for q in combinations(range(n), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    assert len(lines) == 40
    line_sets = [set(l) for l in lines]
    line_key_index = {tuple(sorted(l)): i for i, l in enumerate(lines)}
    skew = [(i, j) for i, j in combinations(range(40), 2)
            if not (line_sets[i] & line_sets[j])]
    assert len(skew) == 540
    base_a, base_b = skew[0]

    def transvection_perm(v):
        out = []
        for x in pts:
            w = symp(x, v)
            out.append(pt_index[canon(tuple(
                (x[k] + w * v[k]) % 3 for k in range(4)))])
        return tuple(out)

    seed_vectors = [
        canon((1, 0, 0, 0)), canon((0, 1, 0, 0)),
        canon((0, 0, 1, 0)), canon((0, 0, 0, 1)),
        canon((1, 1, 0, 0)), canon((1, 0, 1, 0)),
        canon((1, 0, 0, 1)), canon((0, 1, 1, 0)),
    ]
    psp = closure([transvection_perm(v) for v in seed_vectors], 40)
    assert len(psp) == 25920

    def line_perm(g):
        return tuple(line_key_index[tuple(sorted(g[x] for x in line))]
                     for line in lines)

    stabilizer_point = []
    for g in psp:
        lp = line_perm(g)
        if {lp[base_a], lp[base_b]} == {base_a, base_b}:
            stabilizer_point.append(g)
    assert len(stabilizer_point) == 48

    # Induced action on the eight vertices of the Q3 chart.
    cube_vertices = sorted(line_sets[base_a] | line_sets[base_b])
    v_index = {v: i for i, v in enumerate(cube_vertices)}
    stabilizer_cube = set()
    for g in stabilizer_point:
        stabilizer_cube.add(tuple(v_index[g[v]] for v in cube_vertices))
    assert len(stabilizer_cube) == 48

    # Recover the three coordinate matchings of the Q3 chart and quotient the
    # stabilizer by its action on these dimensions.
    cube_edges = []
    for a in line_sets[base_a]:
        for b in line_sets[base_b]:
            if not adj[a][b]:
                cube_edges.append((v_index[a], v_index[b]))
    cube_graph = nx.Graph()
    cube_graph.add_nodes_from(range(8))
    cube_graph.add_edges_from(cube_edges)
    h3 = nx.hypercube_graph(3)
    gm = nx.algorithms.isomorphism.GraphMatcher(cube_graph, h3)
    assert gm.is_isomorphic()
    addr = gm.mapping

    dim_edges = []
    for d in range(3):
        es = set()
        for u, v in cube_edges:
            if sum(addr[u][k] != addr[v][k] for k in range(3)) == 1 and addr[u][d] != addr[v][d]:
                es.add(tuple(sorted((u, v))))
        dim_edges.append(frozenset(es))

    def edge_image(p, e):
        u, v = e
        return tuple(sorted((p[u], p[v])))

    dim_quotient_images = []
    kernel = []
    for p in stabilizer_cube:
        image_dims = []
        for dset in dim_edges:
            img = frozenset(edge_image(p, e) for e in dset)
            image_dims.append(dim_edges.index(img))
        image_dims = tuple(image_dims)
        dim_quotient_images.append(image_dims)
        if image_dims == (0, 1, 2):
            kernel.append(p)
    dim_quotient = set(dim_quotient_images)
    assert len(dim_quotient) == 6
    assert len(kernel) == 8

    return {
        "base_skew_pair": [base_a, base_b],
        "group": stabilizer_cube,
        "kernel_2cube": set(kernel),
        "dimension_quotient": dim_quotient,
        "derived": derived_subgroup(stabilizer_cube),
    }


def perm_from_cycles(n, cycles):
    p = list(range(n))
    for cyc in cycles:
        cyc = [x-1 for x in cyc]
        for a, b in zip(cyc, cyc[1:] + cyc[:1]):
            p[a] = b
    return tuple(p)


def build_tomotope_edge_group():
    # Γ(T) edge action from the tomotope paper, Definition 4.4 / lines r0..r3.
    r0 = perm_from_cycles(12, [(5, 10), (6, 9), (7, 12), (8, 11)])
    r1 = perm_from_cycles(12, [(1, 6), (2, 5), (3, 8), (4, 7)])
    r2 = perm_from_cycles(12, [(5, 9), (6, 10), (7, 11), (8, 12)])
    r3 = perm_from_cycles(12, [(5, 8), (6, 7), (9, 12), (10, 11)])
    p = closure([r0, r1, r2, r3], 12)
    assert len(p) == 96
    d = derived_subgroup(p)
    assert len(d) == 48
    involutive_core = {g for g in d if order(g) in (1, 2)}
    assert len(involutive_core) == 16
    assert closure(list(involutive_core), 12) == involutive_core
    return {"group": p, "derived": d, "derived_2core": involutive_core}


def main():
    cube = build_w33_chart_stabilizer()
    tomo = build_tomotope_edge_group()

    cube_group = cube["group"]
    cube_kernel = cube["kernel_2cube"]
    cube_quot = cube["dimension_quotient"]
    cube_derived = cube["derived"]
    tomo_group = tomo["group"]
    tomo_derived = tomo["derived"]
    tomo_2core = tomo["derived_2core"]

    assert len(cube_group) == 48
    assert len(cube_kernel) == 8
    assert len(cube_quot) == 6
    assert len(cube_derived) == 12
    assert len(tomo_group) == 96
    assert len(tomo_derived) == 48
    assert len(tomo_2core) == 16

    out = {
        "theorem": "BT781 cube/tomotope order-48 split",
        "cube_chart_half": {
            "interpretation": "Aut(Q3) = 2^3:S3",
            "order": len(cube_group),
            "base_skew_pair": cube["base_skew_pair"],
            "element_order_distribution": dist(cube_group),
            "binary_kernel_order": len(cube_kernel),
            "binary_kernel_structure": "C2^3",
            "binary_kernel_order_distribution": dist(cube_kernel),
            "dimension_quotient_order": len(cube_quot),
            "dimension_quotient_structure": "S3",
            "dimension_quotient_order_distribution": dist(cube_quot),
            "derived_order": len(cube_derived),
            "derived_structure": "A4",
            "derived_order_distribution": dist(cube_derived),
        },
        "tomotope_half": {
            "interpretation": "Gamma(T)' = 2^4:C3 inside Gamma(T)=2^4:S3",
            "tomotope_edge_group_order": len(tomo_group),
            "tomotope_edge_group_order_distribution": dist(tomo_group),
            "derived_order": len(tomo_derived),
            "derived_order_distribution": dist(tomo_derived),
            "derived_2core_order": len(tomo_2core),
            "derived_2core_structure": "C2^4",
            "derived_2core_order_distribution": dist(tomo_2core),
            "derived_quotient_order": len(tomo_derived) // len(tomo_2core),
            "derived_quotient_structure": "C3",
        },
        "split_identity": {
            "cube": "2^3 * |S3| = 8 * 6 = 48",
            "tomotope_derived": "2^4 * |C3| = 16 * 3 = 48",
            "trade": "chart transport trades one tomotope binary bit for one reflection bit",
            "not_isomorphic": dist(cube_group) != dist(tomo_derived),
            "cube_vs_tomotope_derived_distributions": [dist(cube_group), dist(tomo_derived)]
        },
        "normalizations": {
            "tomotope_flags": "192 = 4 * 48",
            "tomotope_edge_symmetry": "96 = 2 * 48",
            "w33_directed_edges_and_EH_action": "480 = 10 * 48"
        }
    }

    path = ROOT / "data" / "bt781_cube_tomotope_48_split.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)

    print("BT781 cube/tomotope order-48 split")
    print("cube chart half:", out["cube_chart_half"])
    print("tomotope half:", out["tomotope_half"])
    print("split identity:", out["split_identity"])
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
