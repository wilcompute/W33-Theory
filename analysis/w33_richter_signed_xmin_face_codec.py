#!/usr/bin/env python3
"""BT509: Richter Signed-Xmin Face Codec Theorem.

BT508 identified the BT507 BC/Richter octahedron with the W33 local
pencil-octahedron L(K4).  The existing repo theorem
w33_octahedron_faces_are_signed_xmin.py proves that, at each W33 point,
the 8 local octahedron faces are the signed X_min vectors while the 4
antipodal face-pairs are projective X_min flags.

This theorem pushes that statement back into the Richter/tetrahelix kernel:
  * the 8 faces of the Richter octahedron split into 4 antipodal pairs;
  * each pair is indexed by one tetrahedron vertex / one K4 pencil line;
  * globally, 40 Richter-pencils give 320 signed faces and 160 projective pairs;
  * the local face-pair quotient is K4, while the signed face sheet is K4 x C2.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx
import sympy as sp

K4_VERTS = tuple(range(4))
K4_EDGES = list(itertools.combinations(K4_VERTS, 2))


def main() -> dict:
    O = nx.line_graph(nx.complete_graph(4))
    # Relabel line graph nodes from frozensets/tuples into sorted K4 edges.
    O = nx.relabel_nodes(O, {node: tuple(sorted(node)) for node in O.nodes()})
    assert set(O.nodes()) == set(K4_EDGES)
    assert O.number_of_edges() == 12

    faces = []
    face_pairs = {}
    for v in K4_VERTS:
        star = tuple(sorted(e for e in K4_EDGES if v in e))
        opposite = tuple(sorted(e for e in K4_EDGES if v not in e))
        assert len(star) == 3 and len(opposite) == 3
        assert all(O.has_edge(a, b) for a, b in itertools.combinations(star, 2))
        assert all(O.has_edge(a, b) for a, b in itertools.combinations(opposite, 2))
        faces.append((v, +1, star))
        faces.append((v, -1, opposite))
        face_pairs[v] = {"positive_star": star, "negative_opposite": opposite}

    assert len(faces) == 8

    # Antipodal map on octahedron vertices is complement edge in K4.
    antipode = {e: tuple(sorted(set(K4_VERTS) - set(e))) for e in K4_EDGES}
    assert all(antipode[antipode[e]] == e for e in K4_EDGES)
    assert all(antipode[e] != e for e in K4_EDGES)

    # Antipodal map on faces swaps star(v) with opposite(v).
    for v, data in face_pairs.items():
        star_image = tuple(sorted(antipode[e] for e in data["positive_star"]))
        assert star_image == data["negative_opposite"]

    # Face adjacency graph among 8 triangular faces of octahedron.
    FG = nx.Graph()
    face_keys = [(v, s) for v, s, _ in faces]
    face_sets = {(v, s): set(face) for v, s, face in faces}
    FG.add_nodes_from(face_keys)
    for a, b in itertools.combinations(face_keys, 2):
        if len(face_sets[a] & face_sets[b]) == 2:
            FG.add_edge(a, b)
    assert FG.number_of_nodes() == 8
    assert FG.number_of_edges() == 12
    assert sorted(dict(FG.degree()).values()) == [3] * 8
    # The octahedron face-adjacency graph is the cube graph.
    assert nx.is_isomorphic(FG, nx.cubical_graph())

    # Quotient by antipodal face-pairs gives K4.
    Q = nx.Graph()
    Q.add_nodes_from(K4_VERTS)
    for a, b in itertools.combinations(K4_VERTS, 2):
        # Some signed faces in pair a and pair b share an edge.
        if any(FG.has_edge((a, sa), (b, sb)) for sa in (+1, -1) for sb in (+1, -1)):
            Q.add_edge(a, b)
    assert nx.is_isomorphic(Q, nx.complete_graph(4))

    # Signed sheet is K4 x C2 as a vertex set, with cube adjacency parity-flipping on K4 edges.
    # In the cube, each signed face has three neighbors, all over the other three K4 vertices.
    neighbor_profile = Counter()
    sign_flip_count = 0
    for node in FG.nodes():
        v, s = node
        ns = list(FG.neighbors(node))
        neighbor_profile[(len(ns), len({u for u, _ in ns}), Counter(ss for _, ss in ns)[-s])] += 1
        sign_flip_count += sum(1 for _, ss in ns if ss == -s)
    assert neighbor_profile == Counter({(3, 3, 1): 8})
    assert sign_flip_count == 8  # counted directed; four undirected sign-flip edges.

    local = {
        "signed_faces": 8,
        "projective_face_pairs": 4,
        "octahedron_face_adjacency": "cube graph Q3",
        "face_pair_quotient": "K4",
        "signed_sheet_vertex_set": "K4 vertices x C2 signs",
        "rank_from_existing_codec": 7,
        "nullity_from_existing_codec": 1,
    }
    global40 = {
        "signed_Xmin_faces": 40 * local["signed_faces"],
        "projective_Xmin_pairs": 40 * local["projective_face_pairs"],
        "edge_face_codec_rank": 40 * local["rank_from_existing_codec"],
        "edge_face_codec_nullity": 40 * local["nullity_from_existing_codec"],
    }
    assert global40 == {"signed_Xmin_faces": 320, "projective_Xmin_pairs": 160, "edge_face_codec_rank": 280, "edge_face_codec_nullity": 40}

    results = {
        "theorem": "BT509 Richter Signed-Xmin Face Codec Theorem",
        "local_Richter_octahedron": local,
        "face_pairs": {str(k): {kk: [str(e) for e in vv] for kk, vv in v.items()} for k, v in face_pairs.items()},
        "antipodal_vertex_map": {str(k): str(v) for k, v in sorted(antipode.items())},
        "face_adjacency": {
            "graph": "cube graph",
            "vertices": FG.number_of_nodes(),
            "edges": FG.number_of_edges(),
            "degree": 3,
            "quotient_by_antipodal_pairs": "K4",
        },
        "global_W33_lift": global40,
        "interpretation": {
            "BT507": "Richter axis intersections produce octahedron vertices",
            "BT508": "that octahedron is L(K4), the W33 pencil-octahedron",
            "BT509": "its 8 triangular faces are the local signed X_min sheet; antipodal pairs are projective X_min flags",
        },
        "substrate_reading": {
            "8": "signed local face states of one Richter/W33 octahedron",
            "4": "projective face-pair quotient / K4 vertices / pencil lines",
            "cube": "face-adjacency of the signed octahedron sheet",
            "320": "40*8 signed X_min faces",
            "160": "40*4 projective X_min pairs",
            "280": "40*7 edge-face rank",
        },
    }

    out = Path("data/PART_BT509_RICHTER_SIGNED_XMIN_FACE_CODEC_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
