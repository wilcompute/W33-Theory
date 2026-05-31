#!/usr/bin/env python3
"""Eight Heawood toroidal systems as Singer/Sylow-7 data.

Previous correction:
    The eight toroidal seven-hexagon systems are one orbit under GL(3,2), with
    stabilizer order 21.  Hence

        8 = 168 / 21.

This verifier identifies the group-theoretic object behind the 8.

In GL(3,2), a Singer cycle is an element of order 7 acting transitively on the
seven nonzero vectors of F2^3.  Its normalizer has order 21 = 7:3.  By Sylow,
there are exactly

        n_7 = 8

Sylow-7 subgroups, each with a 21-element normalizer.

Main result:
    The eight toroidal Heawood face systems are naturally bijective with the
    eight Sylow-7/Singer subgroups of GL(3,2).  For each system, its collineation
    stabilizer is exactly the normalizer of one Singer 7-cycle.

So the corrected interpretation is:

    eight toroidal systems = eight Singer normalizers / Sylow-7 choices,
    each system stabilizer = 7:3,
    full Heawood map stabilizer = 7:6 after adjoining dualities.

This is stronger and cleaner than the earlier affine-cube guess.  The 8 is not
GL(3,2)'s natural action on F2^3 vectors; it is the Sylow/Singer orbit.
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


def gl32_matrices() -> list[Matrix3]:
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


def invert(p: Perm) -> Perm:
    out = [0] * len(p)
    for i, x in enumerate(p):
        out[x] = i
    return tuple(out)


def perm_order(p: Perm) -> int:
    e = tuple(range(len(p)))
    x = e
    for n in range(1, 500):
        x = compose(p, x)
        if x == e:
            return n
    raise RuntimeError("order too large")


def cyclic_subgroup(g: Perm) -> frozenset[Perm]:
    e = tuple(range(len(g)))
    out = {e}
    x = e
    while True:
        x = compose(g, x)
        if x == e:
            break
        out.add(x)
    return frozenset(out)


def normalizer(group: set[Perm], subgroup: frozenset[Perm]) -> set[Perm]:
    return {g for g in group if {compose(compose(g, h), invert(g)) for h in subgroup} == set(subgroup)}


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


def heawood_collineations() -> set[Perm]:
    pts, lns, idx, _edges = canonical_heawood()
    colls = set()
    for M in gl32_matrices():
        image = [None] * 14
        for p in pts:
            image[idx[("P", p)]] = idx[("P", mat_vec(M, p))]
        for L in lns:
            ML = tuple(sorted(mat_vec(M, p) for p in L))
            image[idx[("L", L)]] = idx[("L", ML)]
        colls.add(tuple(image))  # type: ignore[arg-type]
    return colls


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


def stabilizer(group: set[Perm], system: HexSystem) -> set[Perm]:
    return {g for g in group if apply_perm_to_system(g, system) == system}


def system_sylow7(stab: set[Perm]) -> frozenset[Perm]:
    order7 = [g for g in stab if perm_order(g) == 7]
    subgroups = {cyclic_subgroup(g) for g in order7}
    assert len(subgroups) == 1
    return next(iter(subgroups))


def build_payload() -> dict:
    colls = heawood_collineations()
    order_profile_gl = Counter(perm_order(g) for g in colls)

    sylow7s = {cyclic_subgroup(g) for g in colls if perm_order(g) == 7}
    normalizers = {H: normalizer(colls, H) for H in sylow7s}
    normalizer_sizes = Counter(len(N) for N in normalizers.values())

    d_edges = dual_edges()
    iso = find_dual_to_heawood_isomorphism(d_edges)
    oriented = orient_faces(FACES_UNORIENTED)
    hexes = dual_hexagons(oriented)
    base_dual = canonical_system(list(hexes.values()))
    base = canonical_system([[iso[x] for x in cyc] for cyc in base_dual])
    systems = {apply_perm_to_system(g, base) for g in colls}

    system_records = []
    system_to_sylow = {}
    for s in sorted(systems):
        stab = stabilizer(colls, s)
        H = system_sylow7(stab)
        system_to_sylow[s] = H
        N = normalizers[H]
        system_records.append(
            {
                "system": s,
                "stabilizer_size": len(stab),
                "stabilizer_order_profile": dict(Counter(perm_order(g) for g in stab)),
                "sylow7_size": len(H),
                "sylow7_order_profile": dict(Counter(perm_order(g) for g in H)),
                "normalizer_size": len(N),
                "stabilizer_equals_singer_normalizer": stab == N,
            }
        )

    sylows_from_systems = set(system_to_sylow.values())

    # Check equivariance: g sends system's Sylow H to conjugate gHg^-1.
    equivariance_failures = 0
    for g in colls:
        invg = invert(g)
        for s, H in system_to_sylow.items():
            image_s = apply_perm_to_system(g, s)
            conjugate_H = frozenset(compose(compose(g, h), invg) for h in H)
            if system_to_sylow[image_s] != conjugate_H:
                equivariance_failures += 1
                break
        if equivariance_failures:
            break

    identities = {
        "GL32_order_168": len(colls) == 168,
        "GL32_order_profile_expected": order_profile_gl == {1: 1, 2: 21, 3: 56, 4: 42, 7: 48},
        "sylow7_count_8": len(sylow7s) == 8,
        "sylow7_normalizer_size_21": normalizer_sizes == {21: 8},
        "toroidal_system_count_8": len(systems) == 8,
        "each_system_stabilizer_21": all(r["stabilizer_size"] == 21 for r in system_records),
        "each_stabilizer_is_7_3_profile": all(r["stabilizer_order_profile"] == {1: 1, 3: 14, 7: 6} for r in system_records),
        "each_stabilizer_equals_singer_normalizer": all(r["stabilizer_equals_singer_normalizer"] for r in system_records),
        "systems_biject_sylow7s": len(sylows_from_systems) == len(systems) == len(sylow7s) == 8,
        "equivariant_system_sylow_bijection": equivariance_failures == 0,
    }
    return {
        "theorem": "heawood_eight_systems_singer_sylow",
        "statement": "The eight Heawood toroidal seven-hexagon systems are equivariantly bijective with the eight Sylow-7/Singer subgroups of GL(3,2).",
        "GL32": {
            "order": len(colls),
            "element_order_profile": dict(order_profile_gl),
            "interpretation": "GL(3,2) is PSL(2,7), acting by Fano collineations on the Heawood graph.",
        },
        "sylow_singer_data": {
            "sylow7_count": len(sylow7s),
            "normalizer_size_distribution": dict(normalizer_sizes),
            "normalizer_structure": "7:3 Singer normalizer",
            "sylow_formula": "n_7=8, n_7 ≡ 1 mod 7 and n_7 | 24",
        },
        "toroidal_systems": {
            "count": len(systems),
            "records": system_records,
        },
        "equivariance": {
            "failures": equivariance_failures,
            "meaning": "Under GL(3,2), transporting a toroidal face system transports its Singer subgroup by conjugation.",
        },
        "interpretation": {
            "correct_factor_8": "8 is the number of Sylow-7/Singer cycle choices in GL(3,2), not the natural 8-vector set of F2^3.",
            "stabilizer": "Choosing one toroidal system is equivalent to choosing one Singer normalizer 7:3; adding Heawood dualities extends this to the 7:6 map stabilizer of order 42.",
            "codec_meaning": "A toroidal face system is a Singer-cycle phase structure on the Fano/Heawood skeleton.",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_heawood_eight_systems_singer_sylow.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
