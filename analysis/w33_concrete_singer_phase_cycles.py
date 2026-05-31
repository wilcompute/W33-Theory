#!/usr/bin/env python3
"""Concrete Singer phase cycles for the Csaszar/Szilassi toroidal system.

Previous theorem:
    the eight toroidal seven-hexagon systems on the Heawood graph are
    equivariantly bijective with the eight Sylow-7/Singer subgroups of GL(3,2).

This file extracts the actual Singer phase attached to the concrete
Csaszar/Szilassi system used in the repo.

For the chosen toroidal face system, its collineation stabilizer is 7:3.  The
unique Sylow-7 subgroup inside that stabilizer acts as a Singer cycle.  We record
how one generator cycles:

    - the seven Fano points;
    - the seven Fano lines;
    - the seven Szilassi hexagonal faces;
    - the 84 directed hexagon-edge flags.

Key result:
    the Singer generator has 12 orbits of length 7 on the 84 local flags, i.e.

        84 = 12 local phases * 7 Singer time/axis steps.

The 7:3 normalizer acts on the Singer generator by multipliers {1,2,4} modulo 7,
confirming the Frobenius phase structure.
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
Flag = tuple[Cycle, int, int]

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


def perm_power(p: Perm, n: int) -> Perm:
    out = tuple(range(len(p)))
    for _ in range(n):
        out = compose(p, out)
    return out


def perm_order(p: Perm) -> int:
    e = tuple(range(len(p)))
    x = e
    for n in range(1, 500):
        x = compose(p, x)
        if x == e:
            return n
    raise RuntimeError("order too large")


def cyclic_subgroup(g: Perm) -> frozenset[Perm]:
    return frozenset(perm_power(g, k) for k in range(perm_order(g)))


def canonical_heawood():
    pts = f2_points()
    lns = fano_lines(pts)
    idx = {}
    rev = {}
    for i, p in enumerate(pts):
        idx[("P", p)] = i
        rev[i] = ("P", p)
    for j, L in enumerate(lns):
        idx[("L", L)] = 7 + j
        rev[7 + j] = ("L", L)
    edges = {tuple(sorted((idx[("P", p)], idx[("L", L)]))) for p in pts for L in lns if p in L}
    return pts, lns, idx, rev, edges


def heawood_collineations() -> set[Perm]:
    pts, lns, idx, _rev, _edges = canonical_heawood()
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
    pts, lns, idx, _rev, he_edges = canonical_heawood()
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


def apply_perm_to_cycle(perm: Perm, cycle: Cycle) -> Cycle:
    return canonical_cycle([perm[x] for x in cycle])


def apply_perm_to_system(perm: Perm, system: HexSystem) -> HexSystem:
    return canonical_system([[perm[x] for x in cyc] for cyc in system])


def stabilizer(group: set[Perm], system: HexSystem) -> set[Perm]:
    return {g for g in group if apply_perm_to_system(g, system) == system}


def orbit_cycle_on_items(g: Perm, items: list[int]) -> list[int]:
    start = items[0]
    seen = [start]
    cur = start
    while True:
        cur = g[cur]
        if cur == start:
            break
        seen.append(cur)
        if len(seen) > len(items):
            raise RuntimeError("not one cycle")
    return seen


def hexagon_permutation(g: Perm, system: HexSystem) -> Perm:
    idx = {h: i for i, h in enumerate(system)}
    return tuple(idx[apply_perm_to_cycle(g, h)] for h in system)


def flags_for_system(system: HexSystem) -> set[Flag]:
    flags = set()
    for h in system:
        n = len(h)
        for i in range(n):
            a, b = h[i], h[(i + 1) % n]
            flags.add((h, a, b))
            flags.add((h, b, a))
    return flags


def apply_perm_to_flag(g: Perm, flag: Flag, system: HexSystem) -> Flag:
    h, a, b = flag
    h2 = apply_perm_to_cycle(g, h)
    return (h2, g[a], g[b])


def flag_orbits(g: Perm, system: HexSystem) -> list[list[Flag]]:
    flags = flags_for_system(system)
    remaining = set(flags)
    out = []
    while remaining:
        start = next(iter(remaining))
        orb = []
        cur = start
        while cur not in orb:
            orb.append(cur)
            cur = apply_perm_to_flag(g, cur, system)
        out.append(orb)
        remaining -= set(orb)
    return out


def conjugation_multiplier(h: Perm, g: Perm) -> int | None:
    conj = compose(compose(h, g), invert(h))
    for k in range(7):
        if perm_power(g, k) == conj:
            return k
    return None


def stringify_cycle(cyc: list[int], rev: dict[int, tuple[str, object]]) -> list[str]:
    return [f"{rev[x][0]}:{rev[x][1]}" for x in cyc]


def build_payload() -> dict:
    pts, lns, idx, rev, he_edges = canonical_heawood()
    colls = heawood_collineations()

    d_edges = dual_edges()
    iso = find_dual_to_heawood_isomorphism(d_edges)
    oriented = orient_faces(FACES_UNORIENTED)
    hexes = dual_hexagons(oriented)
    base_dual = canonical_system(list(hexes.values()))
    base = canonical_system([[iso[x] for x in cyc] for cyc in base_dual])

    stab = stabilizer(colls, base)
    order7 = sorted([g for g in stab if perm_order(g) == 7])
    singer = cyclic_subgroup(order7[0])
    # Choose a generator whose point cycle starts at point index 0 and has lexicographically minimal cycle.
    generators = [g for g in singer if perm_order(g) == 7]
    gen = min(generators, key=lambda x: orbit_cycle_on_items(x, list(range(7))))
    point_cycle = orbit_cycle_on_items(gen, list(range(7)))
    line_cycle = orbit_cycle_on_items(gen, list(range(7, 14)))
    hex_perm = hexagon_permutation(gen, base)
    hex_cycle_indices = orbit_cycle_on_items(hex_perm, list(range(7)))
    hex_cycle = [base[i] for i in hex_cycle_indices]
    flag_orbs = flag_orbits(gen, base)

    order3_elements = [h for h in stab if perm_order(h) == 3]
    multipliers = sorted({conjugation_multiplier(h, gen) for h in order3_elements})

    # For each hexagon, record its alternating point/line content.
    hex_records = []
    for h in base:
        p_vertices = [x for x in h if x < 7]
        l_vertices = [x for x in h if x >= 7]
        hex_records.append(
            {
                "cycle": h,
                "points_in_hex": [str(rev[x][1]) for x in p_vertices],
                "lines_in_hex": [str(rev[x][1]) for x in l_vertices],
            }
        )

    identities = {
        "stabilizer_order_21": len(stab) == 21,
        "unique_singer_subgroup_in_stabilizer": len({cyclic_subgroup(g) for g in order7}) == 1 and len(singer) == 7,
        "selected_generator_order_7": perm_order(gen) == 7,
        "point_cycle_length_7": len(point_cycle) == 7 and set(point_cycle) == set(range(7)),
        "line_cycle_length_7": len(line_cycle) == 7 and set(line_cycle) == set(range(7, 14)),
        "hexagon_cycle_length_7": len(hex_cycle_indices) == 7 and set(hex_cycle_indices) == set(range(7)),
        "flag_orbits_12_of_size_7": len(flag_orbs) == 12 and set(len(o) for o in flag_orbs) == {7},
        "normalizer_order3_multipliers_2_4": multipliers == [2, 4],
        "84_flags_total": sum(len(o) for o in flag_orbs) == 84,
    }
    return {
        "theorem": "concrete_singer_phase_cycles",
        "statement": "The concrete Csaszar/Szilassi toroidal system carries a unique Singer C7 inside its GL(3,2) stabilizer; a generator cycles Fano points, Fano lines, and the seven Szilassi hexagons, and decomposes the 84 flags into twelve 7-cycles.",
        "stabilizer": {
            "size": len(stab),
            "order_profile": dict(Counter(perm_order(g) for g in stab)),
            "singer_subgroup_size": len(singer),
            "order3_conjugation_multipliers_mod7": multipliers,
            "normalizer_reading": "7:3 with order-3 elements acting by multipliers 2 and 4 on C7",
        },
        "selected_singer_generator": {
            "permutation_on_heawood_vertices": gen,
            "point_cycle_indices": point_cycle,
            "point_cycle_labels": stringify_cycle(point_cycle, rev),
            "line_cycle_indices": line_cycle,
            "line_cycle_labels": stringify_cycle(line_cycle, rev),
            "hexagon_cycle_indices": hex_cycle_indices,
            "hexagon_cycle_cycles": hex_cycle,
        },
        "base_toroidal_system": {
            "hexagons": base,
            "hexagon_records": hex_records,
        },
        "flag_phase_orbits": {
            "orbit_count": len(flag_orbs),
            "orbit_size_distribution": dict(Counter(len(o) for o in flag_orbs)),
            "sample_orbits": [[(str(f[0]), f[1], f[2]) for f in orb] for orb in flag_orbs[:3]],
            "interpretation": "84 directed hexagon-edge flags split as 12 local flag phases transported through 7 Singer steps.",
        },
        "interpretation": {
            "phase_structure": "The toroidal seven-hexagon system is a Singer phase structure: one C7 simultaneously cycles Fano points, Fano lines, and the seven toroidal hexagons.",
            "84_codec": "The earlier 7*12=84 can be read dynamically as 12 local flag phases over a 7-step Singer orbit.",
            "normalizer": "The 7:3 stabilizer consists of the Singer cycle plus order-3 relabelings that multiply the phase exponent by 2 or 4 modulo 7.",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_concrete_singer_phase_cycles.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
