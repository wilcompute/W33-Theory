#!/usr/bin/env python3
"""BT559: W33 Levi Frame Automorphism Reconstruction Bound.

This is the promised full-automorphism-enumeration attempt, but carried out by
structural reconstruction rather than blind graph isomorphism.

Let L be the W33 point-line Levi graph and X=L(E(L)) its line graph on the 160
Levi flags.  The cycle-frame Gram depends only on distance in X, so every frame
automorphism is an automorphism of X.

BT559 proves that X reconstructs L internally:

  * X has exactly 80 maximal cliques of size 4.
  * These 80 cliques are precisely the stars of the 80 Levi vertices.
  * The clique-intersection graph is exactly the Levi graph L.

Therefore

    Aut(cycle frame) <= Aut(X) = Aut(L)

for the distance/Gram scheme.  The script then regenerates the exact symplectic
transvection action from BT557, giving a faithful transitive subgroup

    PSp(4,3) of order 25920

on the 160 flags.  Thus the unresolved full group is squeezed by structure: any
missing automorphisms must come from Levi-graph dualities, not hidden frame
symmetries.
"""

from __future__ import annotations

import collections
import itertools
import json
from pathlib import Path

import networkx as nx

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


def build_geometry():
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
    return points, lines, flags


def main() -> dict:
    points, lines, flags = build_geometry()
    p_index = {p: i for i, p in enumerate(points)}

    # Levi graph L on 80 vertices: point vertices 0..39 and line vertices 40..79.
    L = nx.Graph()
    L.add_nodes_from(range(80))
    for li, line in enumerate(lines):
        for p in line:
            L.add_edge(p_index[p], 40 + li)

    edge_list = sorted(tuple(sorted(e)) for e in L.edges())
    edge_index = {e: i for i, e in enumerate(edge_list)}

    # X is the line graph on the 160 Levi flag edges.
    X = nx.Graph()
    X.add_nodes_from(range(len(edge_list)))
    for i, e in enumerate(edge_list):
        se = set(e)
        for j, f in enumerate(edge_list[i + 1:], start=i + 1):
            if se & set(f):
                X.add_edge(i, j)

    # Maximal cliques in X reconstruct stars of L.
    max_cliques = [tuple(sorted(c)) for c in nx.find_cliques(X)]
    clique_size_profile = collections.Counter(map(len, max_cliques))
    star_cliques = []
    for vertex in L.nodes():
        incident_edges = tuple(sorted(edge_index[tuple(sorted(e))] for e in L.edges(vertex)))
        star_cliques.append(incident_edges)
    star_set = set(star_cliques)
    clique_set = set(max_cliques)

    # Reconstruct L from clique intersections: two star-cliques are adjacent iff they share one line-graph vertex.
    R = nx.Graph()
    R.add_nodes_from(range(len(max_cliques)))
    for i, c in enumerate(max_cliques):
        sc = set(c)
        for j, d in enumerate(max_cliques[i + 1:], start=i + 1):
            if sc & set(d):
                R.add_edge(i, j)

    # Symplectic transvection subgroup on flags/edges.
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

    # Distance-shell preservation by generators.
    all_dist = dict(nx.all_pairs_shortest_path_length(X))
    gen_preserve = []
    for perm in generators:
        ok = all(all_dist[perm[i]][perm[j]] == all_dist[i][j] for i in range(160) for j in range(160))
        gen_preserve.append(ok)

    orbit = {g[0] for g in group}
    stabilizer = sum(1 for g in group if g[0] == 0)

    checks = {
        "levi_size": L.number_of_nodes() == 80 and L.number_of_edges() == 160,
        "line_graph_size": X.number_of_nodes() == 160 and X.number_of_edges() == 480,
        "max_cliques_all_size_4": clique_size_profile == {4: 80},
        "max_cliques_are_exactly_stars": clique_set == star_set,
        "reconstructed_graph_is_levi": nx.is_isomorphic(R, L),
        "transvection_group_order": len(group) == 25920,
        "transvection_group_transitive_on_flags": len(orbit) == 160,
        "flag_stabilizer_162": stabilizer == 162,
        "orbit_stabilizer": len(orbit) * stabilizer == len(group),
        "generators_preserve_distance_gram_shells": all(gen_preserve),
    }

    result = {
        "theorem": "BT559 W33 Levi Frame Automorphism Reconstruction Bound",
        "reconstruction": {
            "levi_vertices": L.number_of_nodes(),
            "levi_edges_flags": L.number_of_edges(),
            "line_graph_vertices": X.number_of_nodes(),
            "line_graph_edges": X.number_of_edges(),
            "maximal_clique_size_profile": dict(clique_size_profile),
            "maximal_cliques_equal_levi_stars": clique_set == star_set,
            "clique_intersection_graph": "isomorphic to the original 80-vertex W33 Levi graph",
        },
        "automorphism_consequence": "Aut of the 160-flag distance/Gram frame is forced through the Levi incidence graph; hidden automorphisms cannot bypass the 80 star-clique reconstruction.",
        "constructive_subgroup": {
            "group": "PSp(4,3) generated by symplectic transvections",
            "order": len(group),
            "flag_orbit_size": len(orbit),
            "flag_stabilizer_order": stabilizer,
            "WE6_relation": "2*25920=51840",
        },
        "scope_note": "This is a structural reconstruction and exact lower-bound action certificate, not a completed exhaustive enumeration of Levi dualities.  Any remaining enlargement must be an incidence duality of the reconstructed Levi graph.",
        "all_identities": {k: bool(v) for k, v in checks.items()},
        "all_identities_hold": all(bool(v) for v in checks.values()),
    }
    out = Path("data/PART_BT559_W33_LEVI_FRAME_AUTOMORPHISM_RECONSTRUCTION_BOUND_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()
