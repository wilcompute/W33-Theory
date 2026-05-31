#!/usr/bin/env python3
"""Fano 84 chart-codec to toroidal 84 flag-codecs.

Previous theorem built a natural Fano-atlas object of size

    84 = 7 charts * 12 local chart states.

This verifier sharpens the local meaning of the 12 states.

For a fixed Fano line as infinity, the complement is AG(2,2), a four-point
affine tetrahedron.  A local chart state is

    (affine anchor p, infinity direction d),

which is equivalent to the directed affine edge

    p -> p+d.

Thus each chart's 12 states are the 12 directed edges of K4:

    4 affine vertices * 3 outgoing directions = 6 undirected edges * 2 signs.

This matches the local toroidal flag codec in two dual ways:

    Csaszar: 7 vertex codecs, each degree 6 vertex has 6 incident edges * 2 sides = 12 flags.
    Szilassi: 7 face codecs, each hexagonal face has 6 boundary edges * 2 sides = 12 flags.

The theorem is an axis-level equivalence:

    Fano 84 = seven chart axes * directed-K4 local codec
             = seven Csaszar vertex codecs * local 12 flags
             = seven Szilassi face codecs * local 12 flags.

It does not claim a canonical embedding of Csaszar/Szilassi flags without an
explicit labeling of the seven toroidal axes by the seven Fano chart lines.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

Vec2 = tuple[int, int]
Vec3 = tuple[int, int, int]


def add2(a: Vec2, b: Vec2) -> Vec2:
    return ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2)


def add3(a: Vec3, b: Vec3) -> Vec3:
    return tuple((x + y) % 2 for x, y in zip(a, b))  # type: ignore[return-value]


def fano_points() -> list[Vec3]:
    return [v for v in itertools.product(range(2), repeat=3) if any(v)]


def fano_lines(points: list[Vec3]) -> list[tuple[Vec3, Vec3, Vec3]]:
    out = set()
    for a, b in itertools.combinations(points, 2):
        out.add(tuple(sorted((a, b, add3(a, b)))))
    return sorted(out)


def chart_directed_edges() -> list[tuple[Vec2, Vec2, Vec2]]:
    affine = [(0, 0), (1, 0), (0, 1), (1, 1)]
    directions = [(1, 0), (0, 1), (1, 1)]
    return [(p, d, add2(p, d)) for p in affine for d in directions]


def undirected_edge_key(a: Vec2, b: Vec2) -> tuple[Vec2, Vec2]:
    return tuple(sorted((a, b)))  # type: ignore[return-value]


def local_k4_codec_stats() -> dict:
    directed = chart_directed_edges()
    undir = Counter(undirected_edge_key(p, q) for p, _d, q in directed)
    outgoing = Counter(p for p, _d, _q in directed)
    incoming = Counter(q for _p, _d, q in directed)
    direction = Counter(d for _p, d, _q in directed)
    reverse_closure = all((q, d, p) in directed for p, d, q in directed)
    return {
        "directed_edges": directed,
        "directed_count": len(directed),
        "undirected_edge_count": len(undir),
        "undirected_edge_multiplicities": dict(Counter(undir.values())),
        "outgoing_per_vertex": dict(Counter(outgoing.values())),
        "incoming_per_vertex": dict(Counter(incoming.values())),
        "direction_multiplicities": dict(Counter(direction.values())),
        "reverse_closure": reverse_closure,
    }


def build_payload() -> dict:
    P = fano_points()
    L = fano_lines(P)
    local = local_k4_codec_stats()
    total_fano_states = len(L) * local["directed_count"]

    # Abstract toroidal local flag counts.
    cs_vertex_codecs = 7
    cs_degree = 6
    cs_flags_per_vertex = 2 * cs_degree
    sz_face_codecs = 7
    sz_face_size = 6
    sz_flags_per_face = 2 * sz_face_size
    tet_oriented_edges = 4 * 3
    tet_edges_twosides = 6 * 2

    identities = {
        "fano_chart_axes_7": len(L) == 7,
        "local_directed_K4_edges_12": local["directed_count"] == 12,
        "local_undirected_K4_edges_6_each_two_orientations": local["undirected_edge_count"] == 6 and local["undirected_edge_multiplicities"] == {2: 6},
        "each_affine_vertex_three_out_three_in": local["outgoing_per_vertex"] == {3: 4} and local["incoming_per_vertex"] == {3: 4},
        "each_direction_four_directed_edges": local["direction_multiplicities"] == {4: 3},
        "reverse_closed": local["reverse_closure"],
        "fano_total_84": total_fano_states == 84,
        "csaszar_vertex_codec_84": cs_vertex_codecs * cs_flags_per_vertex == 84 and cs_flags_per_vertex == 12,
        "szilassi_face_codec_84": sz_face_codecs * sz_flags_per_face == 84 and sz_flags_per_face == 12,
        "tetrahedral_local_directed_edges_are_12": tet_oriented_edges == tet_edges_twosides == 12,
    }
    return {
        "theorem": "fano_84_to_toroidal_flag_codecs",
        "local_K4_codec": local,
        "global_Fano_codec": {
            "chart_axes": len(L),
            "states_per_chart": local["directed_count"],
            "total_states": total_fano_states,
            "identity": "84 = 7 Fano chart axes * 12 directed K4-edge states",
        },
        "toroidal_flag_codecs": {
            "csaszar": {
                "axis_type": "vertex codec",
                "axes": cs_vertex_codecs,
                "degree_per_axis": cs_degree,
                "flags_per_axis": cs_flags_per_vertex,
                "total_flags": cs_vertex_codecs * cs_flags_per_vertex,
                "reading": "7 vertices * (6 incident edges * 2 sides) = 84",
            },
            "szilassi": {
                "axis_type": "face codec",
                "axes": sz_face_codecs,
                "face_size_per_axis": sz_face_size,
                "flags_per_axis": sz_flags_per_face,
                "total_flags": sz_face_codecs * sz_flags_per_face,
                "reading": "7 faces * (6 boundary edges * 2 sides) = 84",
            },
            "tetrahedral_local_model": {
                "directed_edges_K4": tet_oriented_edges,
                "edge_two_side_model": tet_edges_twosides,
                "reading": "local 12 = directed edges of tetrahedron = six edges with two orientations/sides",
            },
        },
        "interpretation": {
            "proved": "Fano 84 and toroidal 84 share the exact decomposition seven axes times a local directed-K4 12-codec.",
            "not_yet_proved": "A canonical Csaszar/Szilassi flag labeling requires choosing a bijection from seven Fano chart axes to seven toroidal vertex/face axes and comparing adjacency/chirality relations.",
            "duality": "Csaszar uses vertex axes; Szilassi uses dual face axes; both receive the same Fano chart-axis local directed-edge codec at this abstract level.",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_fano_84_to_toroidal_flag_codecs.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
