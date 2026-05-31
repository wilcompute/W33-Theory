#!/usr/bin/env python3
"""Concrete Csaszar rotation-system flag orientation.

Uses the McCooey Csaszar-1 coordinates/face list already present in the repo's
MDCCCXCIII-MDCCCCII deep dive.  This file moves beyond abstract Fano incidence:
it derives the orientable rotation system of the concrete Csaszar map.

Main checks:
  - 7 vertices, 21 edges, 14 triangular faces, 84 flags.
  - The face set can be coherently oriented so every shared edge is traversed in
    opposite directions by its two incident faces.
  - Around every vertex, the induced rotation is a 6-cycle of neighbors.
  - Local flags at a vertex are exactly: incident neighbor edge (6 choices) times
    side of edge in the rotation (left/right, 2 choices) = 12.
  - Globally this gives 7*6*2=84 concrete oriented side flags.
  - The map automorphism group preserving the unoriented triangular face set has
    order 42, and all of it preserves the chosen orientation system; there are no
    orientation-reversing automorphisms in the vertex permutation group.

Interpretation:
  The Fano-polarity 84 flag model's orientation label p->q should be read, in a
  concrete Csaszar realization, as the two-state side-of-edge choice in the local
  rotation system.  The Euclidean/map chirality is stronger: the Csaszar map has
  42 orientation-preserving automorphisms and no reversing automorphisms.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

# McCooey Csaszar-1 face list from repo deep-dive.
FACES_UNORIENTED = [
    (0, 1, 2), (0, 2, 5), (0, 5, 4), (0, 4, 6), (0, 6, 3), (0, 3, 1),
    (1, 3, 4), (1, 4, 5), (1, 5, 6), (1, 6, 2),
    (2, 6, 4), (2, 4, 3), (2, 3, 5), (5, 3, 6),
]
N = 7


def canonical_face(face: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(sorted(face))


def oriented_edges(face: tuple[int, int, int]) -> list[tuple[int, int]]:
    a, b, c = face
    return [(a, b), (b, c), (c, a)]


def flip(face: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = face
    return (a, c, b)


def orient_faces(faces: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    # Build face adjacency by shared unoriented edge.
    edge_to_faces: dict[tuple[int, int], list[int]] = defaultdict(list)
    for i, f in enumerate(faces):
        for e in itertools.combinations(f, 2):
            edge_to_faces[tuple(sorted(e))].append(i)
    assert all(len(v) == 2 for v in edge_to_faces.values())

    oriented: dict[int, tuple[int, int, int]] = {0: faces[0]}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        fi = oriented[i]
        directed_i = set(oriented_edges(fi))
        for e in itertools.combinations(faces[i], 2):
            key = tuple(sorted(e))
            j = next(x for x in edge_to_faces[key] if x != i)
            if j in oriented:
                continue
            # Choose orientation of face j so shared edge is opposite to face i.
            candidates = [faces[j], flip(faces[j])]
            chosen = None
            for cand in candidates:
                directed_j = set(oriented_edges(cand))
                ok = any((u, v) in directed_i and (v, u) in directed_j for u, v in [key, key[::-1]])
                # More direct: one of the two directed versions of key used by i must be reversed in j.
                edge_i = next((u, v) for u, v in directed_i if set((u, v)) == set(key))
                if (edge_i[1], edge_i[0]) in directed_j:
                    ok = True
                else:
                    ok = False
                if ok:
                    chosen = cand
                    break
            if chosen is None:
                raise RuntimeError("could not orient adjacent face")
            oriented[j] = chosen
            queue.append(j)
    return [oriented[i] for i in range(len(faces))]


def edge_incidence(faces: list[tuple[int, int, int]]) -> dict[tuple[int, int], list[int]]:
    out: dict[tuple[int, int], list[int]] = defaultdict(list)
    for i, f in enumerate(faces):
        for e in itertools.combinations(f, 2):
            out[tuple(sorted(e))].append(i)
    return out


def vertex_rotation(oriented_faces: list[tuple[int, int, int]]) -> dict[int, dict[int, int]]:
    # At vertex v, each oriented face segment pred -> v -> succ maps pred neighbor to succ neighbor.
    succ: dict[int, dict[int, int]] = {v: {} for v in range(N)}
    for f in oriented_faces:
        a, b, c = f
        triples = [(a, b, c), (b, c, a), (c, a, b)]
        for pred, v, nxt in triples:
            if pred in succ[v] and succ[v][pred] != nxt:
                raise AssertionError("rotation conflict")
            succ[v][pred] = nxt
    return succ


def cycle_from_succ(succ: dict[int, int]) -> list[int]:
    start = min(succ)
    cyc = [start]
    cur = start
    while True:
        cur = succ[cur]
        if cur == start:
            break
        cyc.append(cur)
        if len(cyc) > 10:
            raise RuntimeError("not a 6-cycle")
    return cyc


def concrete_flags_from_rotation(rot: dict[int, dict[int, int]]) -> list[tuple[int, int, str, int]]:
    # flag = (vertex axis v, adjacent neighbor w, side label, other neighbor forming face on that side)
    flags = []
    for v, succ in rot.items():
        inv = {b: a for a, b in succ.items()}
        for w in sorted(succ):
            flags.append((v, w, "next", succ[w]))
            flags.append((v, w, "prev", inv[w]))
    return flags


def permute_face(perm: tuple[int, ...], face: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(perm[i] for i in face)


def cyclic_forms(face: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    a, b, c = face
    return {(a, b, c), (b, c, a), (c, a, b)}


def reversed_cyclic_forms(face: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    a, b, c = face
    return {(a, c, b), (c, b, a), (b, a, c)}


def automorphism_profile(oriented_faces: list[tuple[int, int, int]]) -> dict:
    face_set = {canonical_face(f) for f in FACES_UNORIENTED}
    oriented_set = set().union(*(cyclic_forms(f) for f in oriented_faces))
    reversed_set = set().union(*(reversed_cyclic_forms(f) for f in oriented_faces))
    unoriented_aut = []
    orientation_preserving = []
    orientation_reversing = []
    for perm in itertools.permutations(range(N)):
        img_unoriented = {canonical_face(permute_face(perm, f)) for f in FACES_UNORIENTED}
        if img_unoriented != face_set:
            continue
        unoriented_aut.append(perm)
        img_oriented = set().union(*(cyclic_forms(permute_face(perm, f)) for f in oriented_faces))
        if img_oriented == oriented_set:
            orientation_preserving.append(perm)
        if img_oriented == reversed_set:
            orientation_reversing.append(perm)
    return {
        "unoriented_aut_count": len(unoriented_aut),
        "orientation_preserving_count": len(orientation_preserving),
        "orientation_reversing_count": len(orientation_reversing),
        "sample_orientation_preserving": orientation_preserving[:8],
        "sample_orientation_reversing": orientation_reversing[:8],
    }


def build_payload() -> dict:
    oriented = orient_faces(FACES_UNORIENTED)
    edges = edge_incidence(FACES_UNORIENTED)
    rot = vertex_rotation(oriented)
    cycles = {v: cycle_from_succ(succ) for v, succ in rot.items()}
    flags = concrete_flags_from_rotation(rot)
    aut = automorphism_profile(oriented)

    edge_count = len(edges)
    face_count = len(FACES_UNORIENTED)
    vertex_count = N
    euler = vertex_count - edge_count + face_count
    genus = (2 - euler) // 2
    flag_axis_counts = Counter(v for v, _w, _side, _other in flags)
    neighbor_axis_counts = {v: len({w for vv, w, _side, _other in flags if vv == v}) for v in range(N)}
    side_pair_counts = Counter((v, w) for v, w, _side, _other in flags)
    face_corner_count = sum(len(f) for f in FACES_UNORIENTED)

    identities = {
        "V_E_F_genus": (vertex_count, edge_count, face_count, genus) == (7, 21, 14, 1),
        "each_edge_two_faces": set(len(v) for v in edges.values()) == {2},
        "oriented_edge_cancellation": Counter(tuple(sorted(e)) for f in oriented for e in oriented_edges(f)) and all(
            sum(1 for f in oriented for e in oriented_edges(f) if set(e) == set(edge) and e == edge) <= 1
            for edge in itertools.permutations(range(N), 2)
        ),
        "rotation_six_cycle_each_vertex": all(len(cyc) == 6 and set(cyc) == set(range(N)) - {v} for v, cyc in cycles.items()),
        "concrete_flags_84": len(flags) == 84,
        "each_vertex_12_flags": flag_axis_counts == {v: 12 for v in range(N)},
        "each_vertex_6_neighbors": set(neighbor_axis_counts.values()) == {6},
        "each_ordered_vertex_neighbor_has_two_sides": len(side_pair_counts) == 42 and set(side_pair_counts.values()) == {2},
        "face_corners_42_half_flags": face_corner_count == 42 and len(flags) == 2 * face_corner_count,
        "automorphism_order_42": aut["unoriented_aut_count"] == 42,
        "all_aut_orientation_preserving": aut["orientation_preserving_count"] == 42 and aut["orientation_reversing_count"] == 0,
    }
    return {
        "theorem": "csaszar_concrete_rotation_flag_orientation",
        "source": "McCooey Csaszar-1 face list from repo deep dive; coordinates are not needed for combinatorial rotation but identify the concrete realization family.",
        "map_counts": {"V": vertex_count, "E": edge_count, "F": face_count, "Euler_characteristic": euler, "genus": genus},
        "oriented_faces": oriented,
        "vertex_rotation_cycles": cycles,
        "concrete_flag_model": {
            "definition": "(vertex axis v, adjacent neighbor w, side in {next,prev}, other neighbor completing the face on that side)",
            "flag_count": len(flags),
            "sample_flags": flags[:16],
            "axis_count_distribution": dict(Counter(flag_axis_counts.values())),
            "ordered_neighbor_pair_side_distribution": dict(Counter(side_pair_counts.values())),
        },
        "automorphisms": aut,
        "interpretation": {
            "finite_orientation": "The Fano p->q label corresponds concretely to choosing one of the two sides of an incident edge in the local Csaszar rotation system.",
            "chirality": "The vertex-permutation automorphism group preserving the Csaszar face map has order 42 and is entirely orientation-preserving; no orientation-reversing automorphisms are present.",
            "bridge": "This realizes the abstract Csaszar 84 flags as 7 vertices * 6 adjacent vertices * 2 local sides, matching the Fano-polarity labeling.",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_csaszar_concrete_rotation_flag_orientation.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
