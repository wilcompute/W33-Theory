#!/usr/bin/env python3
"""Correction/classification of the Heawood toroidal face-system orbit.

The previous note suggested the eight toroidal face systems split as 4
collineation images plus 4 duality images.  That split is mathematically suspect:
GL(3,2) has order 168 and is simple (isomorphic to PSL(2,7)), so it cannot act
nontrivially on four objects with stabilizer 42.

This verifier recomputes the orbit with the collineation and duality layers kept
separate.

Correct target:
    - The full Heawood automorphism group has 336 elements.
    - The stabilizer of one toroidal seven-hexagon face system has 42 elements.
    - The full orbit has 8 systems.
    - The collineation subgroup GL(3,2) of order 168 is already transitive on the
      same 8 systems, with stabilizer 21.
    - The duality/polarity coset also maps onto the same 8 systems; it does not
      provide a disjoint second set of 4.
    - The full stabilizer splits as 21 collineations + 21 dualities, i.e. a
      7:6 extension of the collineation-side 7:3 stabilizer.

Thus the corrected factorization is:

    8 = 168 / 21 = 336 / 42,

not 4+4.
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
    out = []
    for entries in itertools.product(range(2), repeat=9):
        M: Matrix3 = (tuple(entries[:3]), tuple(entries[3:6]), tuple(entries[6:9]))  # type: ignore[assignment]
        if det3(M) == 1:
            out.append(M)
    return out


def mat_vec(M: Matrix3, v: Vec3) -> Vec3:
    return tuple(sum(M[r][c] * v[c] for c in range(3)) % 2 for r in range(3))  # type: ignore[return-value]


def compose(p: Perm, q: Perm) -> Perm:
    return tuple(p[q[i]] for i in range(len(q)))


def perm_order(p: Perm) -> int:
    e = tuple(range(len(p)))
    x = e
    for n in range(1, 500):
        x = compose(p, x)
        if x == e:
            return n
    raise RuntimeError("order too large")


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
        image = [None] * 14
        for p in pts:
            image[idx[("P", p)]] = idx[("P", mat_vec(M, p))]
        for L in lns:
            ML = tuple(sorted(mat_vec(M, p) for p in L))
            image[idx[("L", L)]] = idx[("L", ML)]
        collineations.add(tuple(image))  # type: ignore[arg-type]

        image2 = [None] * 14
        for p in pts:
            line_img = tuple(sorted(mat_vec(M, x) for x in polar[p]))
            image2[idx[("P", p)]] = idx[("L", line_img)]
        for L in lns:
            image2[idx[("L", L)]] = idx[("P", mat_vec(M, normal[L]))]
        dualities.add(tuple(image2))  # type: ignore[arg-type]
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
    pidx = {p: idx[("P", p)] for p in pts}
    lidx = {L: idx[("L", L)] for L in lns}
    for point_side in (0, 1):
        A = classes[point_side]
        B = classes[1 - point_side]
        for perm_pts in itertools.permutations(pts):
            mapping = {a: pidx[p] for a, p in zip(A, perm_pts)}
            ok = True
            for b in B:
                triple = tuple(sorted(perm_pts[A.index(n)] for n in adj[b]))
                if triple not in line_set:
                    ok = False
                    break
                mapping[b] = lidx[triple]
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


def canonical_cycle(cycle) -> Cycle:
    vals = list(cycle)
    rots = [tuple(vals[i:] + vals[:i]) for i in range(len(vals))]
    rev = list(reversed(vals))
    rots += [tuple(rev[i:] + rev[:i]) for i in range(len(rev))]
    return min(rots)


def canonical_system(cycles) -> HexSystem:
    return tuple(sorted(canonical_cycle(c) for c in cycles))


def apply_perm_to_system(perm: Perm, system: HexSystem) -> HexSystem:
    return canonical_system([[perm[x] for x in cyc] for cyc in system])


def edge_multiset(system: HexSystem) -> Counter:
    c = Counter()
    for cyc in system:
        for i in range(len(cyc)):
            c[tuple(sorted((cyc[i], cyc[(i + 1) % len(cyc)])))] += 1
    return c


def stabilizer(group: set[Perm], system: HexSystem) -> set[Perm]:
    return {g for g in group if apply_perm_to_system(g, system) == system}


def build_payload() -> dict:
    d_edges = dual_edges()
    iso = find_dual_to_heawood_isomorphism(d_edges)
    oriented = orient_faces(FACES_UNORIENTED)
    hexes = dual_hexagons(oriented)
    base_dual = canonical_system(list(hexes.values()))
    base = canonical_system([[iso[x] for x in cyc] for cyc in base_dual])

    colls, duals = heawood_automorphisms_by_type()
    full = colls | duals
    coll_systems = {apply_perm_to_system(g, base) for g in colls}
    dual_systems = {apply_perm_to_system(g, base) for g in duals}
    full_systems = {apply_perm_to_system(g, base) for g in full}

    full_stab = stabilizer(full, base)
    coll_stab = stabilizer(colls, base)
    dual_stab = stabilizer(duals, base)
    coll_stab_orders = Counter(perm_order(g) for g in coll_stab)
    full_stab_orders = Counter(perm_order(g) for g in full_stab)

    system_records = []
    for s in sorted(full_systems):
        ec = edge_multiset(s)
        system_records.append(
            {
                "system": s,
                "edge_support": len(ec),
                "edge_multiplicity_distribution": dict(Counter(ec.values())),
                "full_stabilizer_size": len(stabilizer(full, s)),
                "collineation_stabilizer_size": len(stabilizer(colls, s)),
                "duality_stabilizer_size": len(stabilizer(duals, s)),
            }
        )

    identities = {
        "group_sizes": len(colls) == 168 and len(duals) == 168 and len(full) == 336,
        "orbit_size_8_all_layers": len(coll_systems) == len(dual_systems) == len(full_systems) == 8,
        "duality_and_collineation_images_same_orbit": coll_systems == dual_systems == full_systems,
        "stabilizer_split_21_21_42": len(coll_stab) == 21 and len(dual_stab) == 21 and len(full_stab) == 42,
        "orbit_stabilizer_collineation": len(colls) // len(coll_stab) == 8,
        "orbit_stabilizer_full": len(full) // len(full_stab) == 8,
        "coll_stab_has_7_3_shape": coll_stab_orders == {1: 1, 3: 14, 7: 6} or coll_stab_orders == {1: 1, 3: 14, 7: 6},
        "each_system_valid_edge_cover": all(r["edge_support"] == 21 and r["edge_multiplicity_distribution"] == {2: 21} for r in system_records),
        "each_system_same_stabilizer_sizes": all(r["full_stabilizer_size"] == 42 and r["collineation_stabilizer_size"] == 21 and r["duality_stabilizer_size"] == 21 for r in system_records),
    }
    return {
        "theorem": "heawood_toroidal_orbit_correction",
        "correction": "The eight systems do not split as 4 collineation + 4 duality systems. The collineation subgroup is already transitive on all eight; the duality coset reaches the same eight systems.",
        "orbit_counts": {
            "collineations": len(colls),
            "dualities": len(duals),
            "full_heawood_aut": len(full),
            "systems_from_collineations": len(coll_systems),
            "systems_from_dualities": len(dual_systems),
            "systems_total": len(full_systems),
            "coll_equals_dual_equals_full_orbit": coll_systems == dual_systems == full_systems,
        },
        "stabilizers_of_base_system": {
            "collineation_stabilizer_size": len(coll_stab),
            "duality_stabilizer_size": len(dual_stab),
            "full_stabilizer_size": len(full_stab),
            "collineation_stabilizer_order_distribution": dict(coll_stab_orders),
            "full_stabilizer_order_distribution": dict(full_stab_orders),
            "interpretation": "collineation stabilizer is 7:3 of order 21; adding dualities gives 7:6 of order 42",
        },
        "factorization": {
            "correct": "8 = 168/21 = 336/42",
            "incorrect": "8 is not a disjoint 4+4 split of collineation versus duality images",
        },
        "systems": system_records,
        "interpretation": {
            "why_this_matters": "It respects the simplicity of GL(3,2) ≅ PSL(2,7), which cannot have an index-4 subgroup.",
            "geometric_meaning": "The eight toroidal face systems are a single collineation orbit on the Heawood/Fano skeleton. Dualities do not create another half; they double each stabilizer from 21 to 42.",
            "next_target": "Identify these eight systems as the eight elements of a torsor over the affine cube F2^3 or the eight orientations/complements associated with the Singer 7-cycle normalizer.",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_heawood_toroidal_orbit_correction.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
