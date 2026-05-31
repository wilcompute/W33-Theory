#!/usr/bin/env python3
"""Eight toroidal face systems on the Heawood skeleton.

Previous theorem showed:
    |Aut(Heawood skeleton)| / |Aut(Szilassi toroidal map)| = 336 / 42 = 8.

This verifier gives the factor 8 a concrete geometric meaning.

A Szilassi toroidal map structure on the Heawood graph is a choice of seven
hexagonal face cycles such that each graph edge lies in exactly two hexagons.
The concrete dual of Csaszar supplies one such seven-hexagon system.

Act on that face system by the full 336 automorphisms of the Heawood graph.
The orbit has exactly 8 distinct systems.  Each system has stabilizer size 42.
Moreover the 8 split as:
    4 obtained by Fano collineations;
    4 obtained by Fano dualities/polarities.

Thus the index-8 quotient is not abstract noise: it is the set of eight possible
toroidal Szilassi hexagon systems carried by the same Heawood/Fano skeleton.
Forgetting which of the eight systems is chosen raises symmetry from 42 to 336.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

Vec3 = tuple[int, int, int]
Face = tuple[int, int, int]
Perm = tuple[int, ...]
Matrix3 = tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]
Cycle = tuple[int, ...]
HexSystem = tuple[Cycle, ...]

FACES_UNORIENTED: list[Face] = [
    (0, 1, 2), (0, 2, 5), (0, 5, 4), (0, 4, 6), (0, 6, 3), (0, 3, 1),
    (1, 3, 4), (1, 4, 5), (1, 5, 6), (1, 6, 2),
    (2, 6, 4), (2, 4, 3), (2, 3, 5), (5, 3, 6),
]
N_VERTICES = 7
N_FACES = 14


def add3(a: Vec3, b: Vec3) -> Vec3:
    return tuple((x + y) % 2 for x, y in zip(a, b))  # type: ignore[return-value]


def dot3(a: Vec3, b: Vec3) -> int:
    return sum(x * y for x, y in zip(a, b)) % 2


def f2_points() -> list[Vec3]:
    return sorted(v for v in itertools.product(range(2), repeat=3) if any(v))


def fano_line_from_pair(a: Vec3, b: Vec3) -> tuple[Vec3, Vec3, Vec3]:
    return tuple(sorted((a, b, add3(a, b))))  # type: ignore[return-value]


def fano_lines(points: list[Vec3]) -> list[tuple[Vec3, Vec3, Vec3]]:
    return sorted({fano_line_from_pair(a, b) for a, b in itertools.combinations(points, 2)})


def polar_line(n: Vec3, points: list[Vec3]) -> tuple[Vec3, Vec3, Vec3]:
    return tuple(sorted(p for p in points if dot3(n, p) == 0))  # type: ignore[return-value]


def line_normal(line: tuple[Vec3, Vec3, Vec3], points: list[Vec3]) -> Vec3:
    ns = [n for n in points if all(dot3(n, p) == 0 for p in line)]
    assert len(ns) == 1
    return ns[0]


def det3(M: Matrix3) -> int:
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    return (a * (e * i + f * h) + b * (d * i + f * g) + c * (d * h + e * g)) % 2


def gl32() -> list[Matrix3]:
    mats = []
    for entries in itertools.product(range(2), repeat=9):
        M: Matrix3 = (tuple(entries[0:3]), tuple(entries[3:6]), tuple(entries[6:9]))  # type: ignore[assignment]
        if det3(M) == 1:
            mats.append(M)
    return mats


def mat_vec(M: Matrix3, v: Vec3) -> Vec3:
    return tuple(sum(M[r][c] * v[c] for c in range(3)) % 2 for r in range(3))  # type: ignore[return-value]


def compose(p: Perm, q: Perm) -> Perm:
    return tuple(p[q[i]] for i in range(len(q)))


def canonical_heawood():
    pts = f2_points()
    lns = fano_lines(pts)
    idx = {}
    for i, p in enumerate(pts):
        idx[("P", p)] = i
    for j, L in enumerate(lns):
        idx[("L", L)] = 7 + j
    edges = {tuple(sorted((idx[("P", p)], idx[("L", L)]))) for p in pts for L in lns if p in L}
    return pts, lns, idx, edges


def heawood_automorphisms_by_type():
    pts, lns, idx, _edges = canonical_heawood()
    normal = {L: line_normal(L, pts) for L in lns}
    polar = {p: polar_line(p, pts) for p in pts}
    collineations = set()
    dualities = set()
    for M in gl32():
        img = [None] * 14
        for p in pts:
            img[idx[("P", p)]] = idx[("P", mat_vec(M, p))]
        for L in lns:
            ML = tuple(sorted(mat_vec(M, p) for p in L))
            img[idx[("L", L)]] = idx[("L", ML)]
        collineations.add(tuple(img))  # type: ignore[arg-type]

        img2 = [None] * 14
        for p in pts:
            line_img = tuple(sorted(mat_vec(M, x) for x in polar[p]))
            img2[idx[("P", p)]] = idx[("L", line_img)]
        for L in lns:
            img2[idx[("L", L)]] = idx[("P", mat_vec(M, normal[L]))]
        dualities.add(tuple(img2))  # type: ignore[arg-type]
    return collineations, dualities


def edge_incidence(faces: list[Face]) -> dict[tuple[int, int], list[int]]:
    out = defaultdict(list)
    for i, f in enumerate(faces):
        for e in itertools.combinations(f, 2):
            out[tuple(sorted(e))].append(i)
    return out


def dual_edges() -> set[tuple[int, int]]:
    return {tuple(sorted(v)) for v in edge_incidence(FACES_UNORIENTED).values()}  # type: ignore[arg-type]


def graph_adj(edges: set[tuple[int, int]], n: int) -> dict[int, set[int]]:
    adj = {i: set() for i in range(n)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def bipartition(edges: set[tuple[int, int]], n: int) -> dict[int, int]:
    adj = graph_adj(edges, n)
    color = {}
    for start in range(n):
        if start in color:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            x = queue.popleft()
            for y in adj[x]:
                if y not in color:
                    color[y] = 1 - color[x]
                    queue.append(y)
                elif color[y] == color[x]:
                    raise AssertionError("not bipartite")
    return color


def find_dual_to_heawood_isomorphism(d_edges: set[tuple[int, int]]) -> dict[int, int]:
    pts, lns, idx, he_edges = canonical_heawood()
    adj = graph_adj(d_edges, N_FACES)
    colors = bipartition(d_edges, N_FACES)
    classes = [[v for v, c in colors.items() if c == k] for k in (0, 1)]
    line_set = set(lns)
    point_to_idx = {p: idx[("P", p)] for p in pts}
    line_to_idx = {L: idx[("L", L)] for L in lns}
    for point_side in (0, 1):
        A = classes[point_side]
        B = classes[1 - point_side]
        for perm_pts in itertools.permutations(pts):
            mapping = {a: point_to_idx[p] for a, p in zip(A, perm_pts)}
            ok = True
            for b in B:
                triple = tuple(sorted(perm_pts[A.index(n)] for n in adj[b]))
                if triple not in line_set:
                    ok = False
                    break
                mapping[b] = line_to_idx[triple]
            if ok and {tuple(sorted((mapping[a], mapping[b]))) for a, b in d_edges} == he_edges:
                return mapping
    raise RuntimeError("no isomorphism")


def oriented_edges(face: Face) -> list[tuple[int, int]]:
    a, b, c = face
    return [(a, b), (b, c), (c, a)]


def flip(face: Face) -> Face:
    a, b, c = face
    return (a, c, b)


def orient_faces(faces: list[Face]) -> list[Face]:
    edge_to_faces = edge_incidence(faces)
    oriented = {0: faces[0]}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        directed_i = set(oriented_edges(oriented[i]))
        for key in [tuple(sorted(e)) for e in itertools.combinations(faces[i], 2)]:
            j = next(x for x in edge_to_faces[key] if x != i)
            if j in oriented:
                continue
            edge_i = next((u, v) for u, v in directed_i if set((u, v)) == set(key))
            for cand in (faces[j], flip(faces[j])):
                if (edge_i[1], edge_i[0]) in set(oriented_edges(cand)):
                    oriented[j] = cand
                    queue.append(j)
                    break
            else:
                raise RuntimeError("orientation failure")
    return [oriented[i] for i in range(len(faces))]


def vertex_rotation(oriented_faces: list[Face]):
    succ = {v: {} for v in range(N_VERTICES)}
    corner_face = {}
    for fi, f in enumerate(oriented_faces):
        a, b, c = f
        for pred, v, nxt in [(a, b, c), (b, c, a), (c, a, b)]:
            succ[v][pred] = nxt
            corner_face[(v, pred, nxt)] = fi
    return succ, corner_face


def cycle_from_succ(succ: dict[int, int]) -> list[int]:
    start = min(succ)
    cyc = [start]
    cur = start
    while True:
        cur = succ[cur]
        if cur == start:
            break
        cyc.append(cur)
    return cyc


def dual_hexagons(oriented_faces: list[Face]) -> dict[int, list[int]]:
    rot, corner_face = vertex_rotation(oriented_faces)
    hexes = {}
    for v, succ in rot.items():
        neigh = cycle_from_succ(succ)
        hexes[v] = [corner_face[(v, neigh[i], neigh[(i + 1) % len(neigh)])] for i in range(len(neigh))]
    return hexes


def canonical_cycle(cycle: list[int] | tuple[int, ...]) -> Cycle:
    vals = list(cycle)
    rotations = [tuple(vals[i:] + vals[:i]) for i in range(len(vals))]
    rev = list(reversed(vals))
    rotations += [tuple(rev[i:] + rev[:i]) for i in range(len(rev))]
    return min(rotations)


def canonical_system(cycles: list[list[int]] | list[tuple[int, ...]]) -> HexSystem:
    return tuple(sorted(canonical_cycle(c) for c in cycles))


def apply_perm_to_system(perm: Perm, system: HexSystem) -> HexSystem:
    return canonical_system([[perm[x] for x in cyc] for cyc in system])


def edge_multiset_of_system(system: HexSystem) -> Counter:
    counts = Counter()
    for cyc in system:
        n = len(cyc)
        for i in range(n):
            counts[tuple(sorted((cyc[i], cyc[(i + 1) % n])))] += 1
    return counts


def cycle_is_valid_graph_cycle(cycle: Cycle, edges: set[tuple[int, int]]) -> bool:
    return len(cycle) == 6 and len(set(cycle)) == 6 and all(tuple(sorted((cycle[i], cycle[(i + 1) % 6]))) in edges for i in range(6))


def build_payload() -> dict:
    d_edges = dual_edges()
    iso = find_dual_to_heawood_isomorphism(d_edges)
    he_edges = canonical_heawood()[3]
    oriented = orient_faces(FACES_UNORIENTED)
    hexes = dual_hexagons(oriented)
    base_system_dual = canonical_system(list(hexes.values()))
    base_system_heawood = canonical_system([[iso[x] for x in cyc] for cyc in base_system_dual])

    colls, duals = heawood_automorphisms_by_type()
    he_aut = colls | duals
    systems_all = {apply_perm_to_system(g, base_system_heawood) for g in he_aut}
    systems_coll = {apply_perm_to_system(g, base_system_heawood) for g in colls}
    systems_dual = {apply_perm_to_system(g, base_system_heawood) for g in duals}

    system_records = []
    stabilizer_sizes = Counter()
    for system in sorted(systems_all):
        edge_counts = edge_multiset_of_system(system)
        stabilizer = {g for g in he_aut if apply_perm_to_system(g, system) == system}
        stabilizer_sizes[len(stabilizer)] += 1
        system_records.append(
            {
                "system": system,
                "hexagon_count": len(system),
                "all_cycles_length_6_valid": all(cycle_is_valid_graph_cycle(c, he_edges) for c in system),
                "edge_multiplicity_distribution": dict(Counter(edge_counts.values())),
                "edge_support_size": len(edge_counts),
                "stabilizer_size": len(stabilizer),
                "from_collineation": system in systems_coll,
                "from_duality": system in systems_dual,
            }
        )

    identities = {
        "heawood_aut_336": len(he_aut) == 336 and len(colls) == 168 and len(duals) == 168,
        "orbit_has_8_toroidal_face_systems": len(systems_all) == 8,
        "collineation_side_has_4_systems": len(systems_coll) == 4,
        "duality_side_has_4_systems": len(systems_dual) == 4,
        "coll_dual_sides_partition_8": len(systems_coll | systems_dual) == 8 and len(systems_coll & systems_dual) == 0,
        "each_system_has_7_hexagons": all(r["hexagon_count"] == 7 for r in system_records),
        "each_hexagon_valid_6_cycle": all(r["all_cycles_length_6_valid"] for r in system_records),
        "each_system_covers_21_edges_twice": all(r["edge_support_size"] == 21 and r["edge_multiplicity_distribution"] == {2: 21} for r in system_records),
        "each_stabilizer_size_42": stabilizer_sizes == {42: 8},
        "orbit_stabilizer": len(he_aut) // 42 == 8,
    }
    return {
        "theorem": "heawood_eight_toroidal_face_systems",
        "base_system": {
            "description": "seven Szilassi hexagons transported from the concrete Csaszar dual into the canonical Heawood graph",
            "hexagon_system": base_system_heawood,
        },
        "orbit_counts": {
            "heawood_automorphisms": len(he_aut),
            "collineations": len(colls),
            "dualities": len(duals),
            "systems_total": len(systems_all),
            "systems_from_collineations": len(systems_coll),
            "systems_from_dualities": len(systems_dual),
            "stabilizer_size_distribution": dict(stabilizer_sizes),
        },
        "systems": system_records,
        "interpretation": {
            "factor_8": "The index 8 is the orbit of the chosen toroidal Szilassi seven-hexagon face system under Aut(Heawood).",
            "four_plus_four": "The eight systems split into four collineation images and four duality/polarity images.",
            "forgetting_structure": "Keeping one seven-hexagon toroidal face system leaves 42 automorphisms; forgetting which of the eight systems is chosen restores the full 336 Heawood symmetries.",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_heawood_eight_toroidal_face_systems.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
