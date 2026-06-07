#!/usr/bin/env python3
"""BT508: Richter-Pencil Octahedron Bridge Theorem.

Repo context checked before this script:
  * analysis/w33_local_pencil_octahedra.py proves each W33 point carries
    a local pencil-octahedron O_p=L(K4), aggregate 40*(6,12,8)=(240,480,320).
  * analysis/w33_octahedron_faces_are_signed_xmin.py proves the 320 signed
    local octahedron faces equal signed X_min vectors and gives local
    edge-face codec rank 7.
  * BT507 proved the BC/Qi-Men/Richter tetrahelix axes through one tetrahedron
    pairwise intersect in a regular octahedron at ±(2/5)e_i.

New bridge:
  The BT507 Richter octahedron is exactly the same combinatorial object as
  the W33 pencil octahedron: both are L(K4).  Under the map
      K4 edge ij -> midpoint of tetrahedron edge ij,
  the line graph L(K4) is isomorphic to the octahedron graph on the six
  midpoint vertices.  This identifies the physical BC/Richter octahedral
  crossing kernel with the algebraic W33 local pencil codec.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx
import sympy as sp

# Standard tetrahedron used in BT507 / uploaded BC paper calculations.
T = {
    0: sp.Matrix([1, 1, 1]),
    1: sp.Matrix([-1, -1, 1]),
    2: sp.Matrix([-1, 1, -1]),
    3: sp.Matrix([1, -1, -1]),
}


def norm2(v: sp.Matrix) -> sp.Expr:
    return sp.simplify(v.dot(v))


def main() -> dict:
    k4_edges = list(itertools.combinations(range(4), 2))
    assert len(k4_edges) == 6

    # Pencil-octahedron: L(K4) vertices are K4 edges; adjacency means shared endpoint.
    L = nx.Graph()
    L.add_nodes_from(k4_edges)
    for e, f in itertools.combinations(k4_edges, 2):
        if set(e) & set(f):
            L.add_edge(e, f)
    assert L.number_of_nodes() == 6
    assert L.number_of_edges() == 12
    assert sorted(dict(L.degree()).values()) == [4] * 6

    # Richter/octahedron coordinates: midpoints of K4 edges.
    midpoint = {e: sp.simplify((T[e[0]] + T[e[1]]) / 2) for e in k4_edges}
    expected_points = {
        (sp.Rational(1), 0, 0), (-sp.Rational(1), 0, 0),
        (0, sp.Rational(1), 0), (0, -sp.Rational(1), 0),
        (0, 0, sp.Rational(1)), (0, 0, -sp.Rational(1)),
    }
    assert {tuple(v) for v in midpoint.values()} == expected_points

    # Scale BT507 axis-pair octahedron ±(2/5)e_i to midpoint octahedron ±e_i.
    scale = sp.Rational(5, 2)
    bt507_points_scaled = {
        tuple(scale * sp.Matrix(v)) for v in [
            (sp.Rational(2,5),0,0), (-sp.Rational(2,5),0,0),
            (0,sp.Rational(2,5),0), (0,-sp.Rational(2,5),0),
            (0,0,sp.Rational(2,5)), (0,0,-sp.Rational(2,5)),
        ]
    }
    assert bt507_points_scaled == expected_points

    # Coordinate octahedron graph: minimal nonzero distance edges.
    coordG = nx.Graph()
    coordG.add_nodes_from(k4_edges)
    for e, f in itertools.combinations(k4_edges, 2):
        d2 = norm2(midpoint[e] - midpoint[f])
        if d2 == 2:
            coordG.add_edge(e, f)
    assert nx.is_isomorphic(coordG, L)
    assert coordG.number_of_edges() == 12

    # Octahedron faces: triangles in L(K4), split as four stars and four opposite triangles.
    faces = [tri for tri in itertools.combinations(k4_edges, 3) if all(coordG.has_edge(a, b) for a, b in itertools.combinations(tri, 2))]
    assert len(faces) == 8
    star_faces = []
    opposite_faces = []
    for tri in faces:
        common = set(tri[0]) & set(tri[1]) & set(tri[2])
        if common:
            star_faces.append(tri)
        else:
            opposite_faces.append(tri)
    assert len(star_faces) == 4
    assert len(opposite_faces) == 4

    # Edge-face incidence matrix local rank should match prior repo theorem: rank 7, nullity 1.
    face_index = {face: i for i, face in enumerate(faces)}
    oct_edges = list(coordG.edges())
    M = sp.zeros(len(oct_edges), len(faces))
    for i, edge in enumerate(oct_edges):
        for j, face in enumerate(faces):
            if edge[0] in face and edge[1] in face:
                M[i, j] = 1
    assert M.shape == (12, 8)
    assert M.rank() == 7
    assert len(faces) - M.rank() == 1
    assert Counter(sum(M[i, j] for j in range(M.shape[1])) for i in range(M.shape[0])) == Counter({2: 12})
    assert Counter(sum(M[i, j] for i in range(M.shape[0])) for j in range(M.shape[1])) == Counter({3: 8})

    # Scale global W33 aggregate from prior local theorem.
    aggregate = {
        "local_octahedra": 40,
        "global_vertices": 40 * 6,
        "global_edges": 40 * 12,
        "global_faces": 40 * 8,
        "global_edge_face_rank": 40 * 7,
        "global_face_nullity": 40,
    }
    assert aggregate == {
        "local_octahedra": 40,
        "global_vertices": 240,
        "global_edges": 480,
        "global_faces": 320,
        "global_edge_face_rank": 280,
        "global_face_nullity": 40,
    }

    results = {
        "theorem": "BT508 Richter-Pencil Octahedron Bridge Theorem",
        "bridge_statement": "BT507 BC/Richter crossing octahedron and W33 local pencil-octahedron are the same object L(K4)",
        "local_model": {
            "K4_edges": [str(e) for e in k4_edges],
            "line_graph": "L(K4)",
            "octahedron_f_vector": [6, 12, 8],
            "degree": 4,
            "coordinate_vertices": {str(k): [str(x) for x in v] for k, v in midpoint.items()},
            "BT507_scale_to_midpoint_octahedron": "multiply ±(2/5)e_i by 5/2 to get ±e_i",
        },
        "face_codec": {
            "star_faces": len(star_faces),
            "opposite_faces": len(opposite_faces),
            "edge_face_matrix_shape": [12, 8],
            "rank": int(M.rank()),
            "nullity": int(len(faces) - M.rank()),
            "row_degree": {"2": 12},
            "col_degree": {"3": 8},
        },
        "W33_global_lift": aggregate,
        "interpretation": {
            "Richter_kernel": "physical BC-axis crossing octahedron inside one tetrahedral now",
            "pencil_codec": "algebraic W33 local pencil octahedron at one point",
            "identity": "both are L(K4), so the local memory now and local W33 gauge codec share the same octahedral carrier",
        },
        "substrate_reading": {
            "6": "K4 edges / octahedron vertices / local axis-pair crossings",
            "12": "octahedron edges / local BC axis codec / W33 valency",
            "8": "signed local faces / X_min signs per W33 point",
            "7": "rank of one octahedral edge-face codec",
            "40": "one octahedral codec at every W33 point",
            "240_480_320": "global vertices/edges/faces of the 40-octahedron lift",
        },
    }

    out = Path("data/PART_BT508_RICHTER_PENCIL_OCTAHEDRON_BRIDGE_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
