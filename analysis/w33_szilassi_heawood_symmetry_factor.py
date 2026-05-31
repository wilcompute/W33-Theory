#!/usr/bin/env python3
"""Szilassi/Heawood symmetry factor verifier.

The previous verifier constructed the Szilassi dual map from the concrete
Csaszar rotation system.  This file separates the two symmetry layers:

    map symmetry:      automorphisms preserving the toroidal face structure;
    skeleton symmetry: automorphisms of the underlying Heawood graph.

Main result:
    |Aut(Szilassi toroidal map)| = 42, all orientation-preserving;
    |Aut(Heawood skeleton)|      = 336;
    336 / 42 = 8.

The factor 8 is therefore the symmetry gain obtained by forgetting the toroidal
hexagonal face structure and remembering only the cubic bipartite Heawood graph.

Implementation notes:
  - The dual Szilassi skeleton is built from the Csaszar face adjacency graph.
  - The canonical Heawood graph is built as the incidence graph of the Fano plane.
  - A graph isomorphism from the dual skeleton to the canonical Heawood graph is
    found by identifying one bipartition class with the 7 Fano points.
  - The Heawood automorphism group is constructed explicitly as PGL(3,2)
    collineations plus dualities/polarities, total 168+168=336.
  - The 42 toroidal map automorphisms are transported through the isomorphism and
    checked to form a subgroup of the 336 skeleton automorphisms.
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
    normals = [n for n in points if all(dot3(n, p) == 0 for p in line)]
    assert len(normals) == 1
    return normals[0]


def det3(M: Matrix3) -> int:
    # determinant mod 2 by expansion; minus=plus in F2.
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


def edge_incidence(faces: list[Face]) -> dict[tuple[int, int], list[int]]:
    out: dict[tuple[int, int], list[int]] = defaultdict(list)
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
    color: dict[int, int] = {}
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


def girth(edges: set[tuple[int, int]], n: int) -> int | None:
    adj = graph_adj(edges, n)
    best = None
    for start in range(n):
        dist = {start: 0}
        parent = {start: -1}
        queue = deque([start])
        while queue:
            x = queue.popleft()
            for y in adj[x]:
                if y not in dist:
                    dist[y] = dist[x] + 1
                    parent[y] = x
                    queue.append(y)
                elif parent[x] != y and parent[y] != x:
                    length = dist[x] + dist[y] + 1
                    best = length if best is None else min(best, length)
    return best


def orient_faces(faces: list[Face]) -> list[Face]:
    def oriented_edges(face: Face) -> list[tuple[int, int]]:
        a, b, c = face
        return [(a, b), (b, c), (c, a)]

    def flip(face: Face) -> Face:
        a, b, c = face
        return (a, c, b)

    edge_to_faces = edge_incidence(faces)
    oriented: dict[int, Face] = {0: faces[0]}
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


def vertex_rotation(oriented_faces: list[Face]) -> tuple[dict[int, dict[int, int]], dict[tuple[int, int, int], int]]:
    succ: dict[int, dict[int, int]] = {v: {} for v in range(N_VERTICES)}
    corner_face: dict[tuple[int, int, int], int] = {}
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
    hexes: dict[int, list[int]] = {}
    for v, succ in rot.items():
        neigh = cycle_from_succ(succ)
        hexes[v] = [corner_face[(v, neigh[i], neigh[(i + 1) % len(neigh)])] for i in range(len(neigh))]
    return hexes


def cyclic_forms(seq: list[int]) -> set[tuple[int, ...]]:
    n = len(seq)
    return {tuple(seq[i:] + seq[:i]) for i in range(n)}


def reversed_cyclic_forms(seq: list[int]) -> set[tuple[int, ...]]:
    r = list(reversed(seq))
    return cyclic_forms(r)


def primal_map_automorphisms(oriented_faces: list[Face], hexes: dict[int, list[int]]) -> dict:
    face_set = {tuple(sorted(f)) for f in FACES_UNORIENTED}
    face_index = {tuple(sorted(f)): i for i, f in enumerate(FACES_UNORIENTED)}
    autos = []
    dual_face_perms = []
    dual_orientation_preserving = []
    dual_orientation_reversing = []
    for perm in itertools.permutations(range(N_VERTICES)):
        img_faces = {tuple(sorted(perm[i] for i in f)) for f in FACES_UNORIENTED}
        if img_faces != face_set:
            continue
        autos.append(perm)
        fperm = tuple(face_index[tuple(sorted(perm[i] for i in f))] for f in FACES_UNORIENTED)
        dual_face_perms.append(fperm)
        preserving = True
        reversing = True
        for v, hex_seq in hexes.items():
            image_seq = [fperm[i] for i in hex_seq]
            target = hexes[perm[v]]
            preserving = preserving and tuple(image_seq) in cyclic_forms(target)
            reversing = reversing and tuple(image_seq) in reversed_cyclic_forms(target)
        if preserving:
            dual_orientation_preserving.append(perm)
        if reversing:
            dual_orientation_reversing.append(perm)
    return {
        "primal_vertex_perms": autos,
        "dual_face_perms": dual_face_perms,
        "dual_orientation_preserving": dual_orientation_preserving,
        "dual_orientation_reversing": dual_orientation_reversing,
    }


def canonical_heawood() -> tuple[list[Vec3], list[tuple[Vec3, Vec3, Vec3]], dict[tuple[str, object], int], set[tuple[int, int]]]:
    pts = f2_points()
    lns = fano_lines(pts)
    idx: dict[tuple[str, object], int] = {}
    for i, p in enumerate(pts):
        idx[("P", p)] = i
    for j, L in enumerate(lns):
        idx[("L", L)] = 7 + j
    edges = {(idx[("P", p)], idx[("L", L)]) for p in pts for L in lns if p in L}
    return pts, lns, idx, edges


def heawood_automorphisms() -> set[Perm]:
    pts, lns, idx, _edges = canonical_heawood()
    line_index = {L: L for L in lns}
    normal = {L: line_normal(L, pts) for L in lns}
    polar = {p: polar_line(p, pts) for p in pts}
    autos: set[Perm] = set()
    for M in gl32():
        # Collineation.
        image = [None] * 14
        for p in pts:
            image[idx[("P", p)]] = idx[("P", mat_vec(M, p))]
        for L in lns:
            ML = tuple(sorted(mat_vec(M, p) for p in L))
            image[idx[("L", L)]] = idx[("L", ML)]
        autos.add(tuple(image))  # type: ignore[arg-type]
        # Duality: polarity then collineation.
        image2 = [None] * 14
        for p in pts:
            line_img = tuple(sorted(mat_vec(M, x) for x in polar[p]))
            image2[idx[("P", p)]] = idx[("L", line_img)]
        for L in lns:
            image2[idx[("L", L)]] = idx[("P", mat_vec(M, normal[L]))]
        autos.add(tuple(image2))  # type: ignore[arg-type]
    return autos


def find_dual_to_heawood_isomorphism(dual_edges_: set[tuple[int, int]]) -> dict[int, int]:
    pts, lns, idx, he_edges = canonical_heawood()
    dual_adj = graph_adj(dual_edges_, N_FACES)
    colors = bipartition(dual_edges_, N_FACES)
    color_classes = [[v for v, c in colors.items() if c == color] for color in (0, 1)]
    line_set = set(lns)
    line_to_idx = {L: idx[("L", L)] for L in lns}
    point_to_idx = {p: idx[("P", p)] for p in pts}

    for point_side in (0, 1):
        A = color_classes[point_side]
        B = color_classes[1 - point_side]
        for perm_pts in itertools.permutations(pts):
            mapping: dict[int, int] = {a: point_to_idx[p] for a, p in zip(A, perm_pts)}
            ok = True
            for b in B:
                triple = tuple(sorted(perm_pts[A.index(n)] for n in dual_adj[b]))
                if triple not in line_set:
                    ok = False
                    break
                mapping[b] = line_to_idx[triple]
            if not ok:
                continue
            mapped_edges = {tuple(sorted((mapping[a], mapping[b]))) for a, b in dual_edges_}
            if mapped_edges == he_edges:
                return mapping
    raise RuntimeError("no isomorphism found")


def conjugate_dual_perm_to_heawood(dual_perm: Perm, iso: dict[int, int]) -> Perm:
    inv_iso = {v: k for k, v in iso.items()}
    out = [None] * 14
    for h_vertex in range(14):
        d_vertex = inv_iso[h_vertex]
        out[h_vertex] = iso[dual_perm[d_vertex]]
    return tuple(out)  # type: ignore[return-value]


def left_coset_count(group: set[Perm], subgroup: set[Perm]) -> int:
    remaining = set(group)
    count = 0
    while remaining:
        g = next(iter(remaining))
        coset = {compose(g, h) for h in subgroup}
        remaining -= coset
        count += 1
    return count


def build_payload() -> dict:
    oriented = orient_faces(FACES_UNORIENTED)
    hexes = dual_hexagons(oriented)
    d_edges = dual_edges()
    deg = Counter()
    for a, b in d_edges:
        deg[a] += 1
        deg[b] += 1
    colors = bipartition(d_edges, N_FACES)
    g = girth(d_edges, N_FACES)

    map_aut = primal_map_automorphisms(oriented, hexes)
    he_aut = heawood_automorphisms()
    iso = find_dual_to_heawood_isomorphism(d_edges)
    transported_map_aut = {conjugate_dual_perm_to_heawood(fp, iso) for fp in map_aut["dual_face_perms"]}
    he_edges = canonical_heawood()[3]
    transported_edges = {tuple(sorted((iso[a], iso[b]))) for a, b in d_edges}
    cosets = left_coset_count(he_aut, transported_map_aut)

    identities = {
        "dual_skeleton_counts": N_FACES == 14 and len(d_edges) == 21,
        "dual_skeleton_cubic_bipartite_girth6": set(deg.values()) == {3} and set(Counter(colors.values()).values()) == {7} and g == 6,
        "heawood_aut_order_336": len(he_aut) == 336,
        "map_aut_order_42": len(map_aut["primal_vertex_perms"]) == 42 and len(map_aut["dual_face_perms"]) == 42,
        "dual_map_all_orientation_preserving": len(map_aut["dual_orientation_preserving"]) == 42 and len(map_aut["dual_orientation_reversing"]) == 0,
        "dual_graph_isomorphic_to_heawood": transported_edges == he_edges,
        "map_aut_subgroup_of_heawood_aut": transported_map_aut.issubset(he_aut),
        "symmetry_gain_factor_8": len(he_aut) // len(transported_map_aut) == 8 and cosets == 8,
        "fano_collineation_plus_duality_split": len(gl32()) == 168 and len(he_aut) == 2 * len(gl32()),
    }
    return {
        "theorem": "szilassi_heawood_symmetry_factor",
        "dual_skeleton": {
            "vertices": N_FACES,
            "edges": len(d_edges),
            "degree_distribution": dict(Counter(deg.values())),
            "bipartition_sizes": dict(Counter(colors.values())),
            "girth": g,
        },
        "dual_map_automorphisms": {
            "order": len(map_aut["primal_vertex_perms"]),
            "orientation_preserving": len(map_aut["dual_orientation_preserving"]),
            "orientation_reversing": len(map_aut["dual_orientation_reversing"]),
            "sample_vertex_perms": map_aut["primal_vertex_perms"][:8],
        },
        "heawood_skeleton_automorphisms": {
            "order": len(he_aut),
            "construction": "168 Fano collineations GL(3,2) plus 168 polarity/duality maps",
            "GL32_order": len(gl32()),
        },
        "embedding_of_map_group": {
            "isomorphism_dual_to_canonical_heawood_sample": {str(k): v for k, v in list(iso.items())[:14]},
            "transported_map_aut_size": len(transported_map_aut),
            "is_subgroup_of_heawood_aut": transported_map_aut.issubset(he_aut),
            "left_coset_count_in_heawood_aut": cosets,
            "factor": len(he_aut) // len(transported_map_aut),
        },
        "interpretation": {
            "map_vs_skeleton": "The toroidal Szilassi map has 42 automorphisms because the seven hexagonal faces/rotation system are remembered. The underlying Heawood skeleton has 336 automorphisms after forgetting that toroidal face structure.",
            "factor_8": "The symmetry gain 336/42=8 is the extra Fano incidence freedom of the Heawood graph relative to the toroidal map codec.",
            "chirality": "Like the Csaszar map, the dual Szilassi map automorphisms are all orientation-preserving at the map level; the larger Heawood group includes symmetries that do not preserve the chosen toroidal face structure.",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_szilassi_heawood_symmetry_factor.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
