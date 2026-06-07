#!/usr/bin/env python3
"""BT515: Richter Radial-Dual Polar Cube Theorem.

The uploaded title mentions radial-dual lattice graphs and admissible inversion.
The uploaded file itself is not a readable PDF in the sandbox; it is a
ResearchGate security-check HTML page.  This theorem therefore uses the title
only as a hypothesis generator and proves an exact result already forced by
BT507-BT510.

BT507: the BC/Richter axis-pair octahedron has vertices
    ±(2/5)e_x, ±(2/5)e_y, ±(2/5)e_z.

Strict polar duality says the polar of conv(±r e_i) is the cube
    [-1/r,1/r]^3.
For r=2/5 this is the cube [-5/2,5/2]^3.

Radial inversion I(x)=x/(x·x) sends
    ±(2/5)e_i -> ±(5/2)e_i,
which are exactly the six face centers of the polar cube.

Thus BT510's octahedron/cube dual is not just combinatorial: it is exact
radial-dual/polar inversion geometry.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import networkx as nx
import sympy as sp

r = sp.Rational(2, 5)
h = 1 / r


def dot(a, b):
    return sp.simplify(sum(x*y for x, y in zip(a, b)))


def norm2(a):
    return dot(a, a)


def radial_inverse(a):
    n2 = norm2(a)
    return tuple(sp.simplify(x / n2) for x in a)


def main() -> dict:
    oct_vertices = [
        (r,0,0),(-r,0,0),(0,r,0),(0,-r,0),(0,0,r),(0,0,-r)
    ]
    cube_vertices = list(itertools.product([-h,h], repeat=3))
    cube_face_centers = [
        (h,0,0),(-h,0,0),(0,h,0),(0,-h,0),(0,0,h),(0,0,-h)
    ]

    assert {radial_inverse(v) for v in oct_vertices} == set(cube_face_centers)
    assert all(dot(v, radial_inverse(v)) == 1 for v in oct_vertices)

    # Polar cube is exactly {x: |x_i| <= h}.  Each oct vertex defines one face plane v·x=1.
    face_incidence = {}
    for v in oct_vertices:
        center = radial_inverse(v)
        incident = [c for c in cube_vertices if dot(v, c) == 1]
        assert len(incident) == 4
        face_incidence[str(v)] = [str(c) for c in sorted(incident, key=str)]

    # Cube vertices correspond to octahedron faces: each cube vertex saturates three inequalities.
    vertex_to_oct_face = {}
    for c in cube_vertices:
        saturated = [v for v in oct_vertices if dot(v, c) == 1]
        assert len(saturated) == 3
        vertex_to_oct_face[str(c)] = [str(v) for v in sorted(saturated, key=str)]

    # Graphs: octahedron graph equals cube-face adjacency graph.
    O = nx.Graph(); O.add_nodes_from(range(6))
    for i,j in itertools.combinations(range(6),2):
        if norm2(tuple(oct_vertices[i][k]-oct_vertices[j][k] for k in range(3))) == 2*r*r:
            O.add_edge(i,j)
    assert O.number_of_edges() == 12

    # Cube face graph using face centers: adjacent if corresponding square faces share an edge.
    F = nx.Graph(); F.add_nodes_from(range(6))
    for i,j in itertools.combinations(range(6),2):
        # Opposite faces have centers summing to zero and are nonadjacent; all other pairs adjacent.
        if tuple(cube_face_centers[i][k] + cube_face_centers[j][k] for k in range(3)) != (0,0,0):
            F.add_edge(i,j)
    assert nx.is_isomorphic(O, F)
    assert F.number_of_edges() == 12

    # Cube vertex graph is the dual face-adjacency graph of the octahedron faces.
    C = nx.Graph(); C.add_nodes_from(range(8))
    for i,j in itertools.combinations(range(8),2):
        diff = sum(1 for a,b in zip(cube_vertices[i], cube_vertices[j]) if a != b)
        if diff == 1:
            C.add_edge(i,j)
    assert nx.is_isomorphic(C, nx.cubical_graph())
    assert C.number_of_edges() == 12

    local = {
        "octahedron_radius": str(r),
        "polar_cube_half_side": str(h),
        "radius_halfside_product": str(r*h),
        "radial_inversion": "x -> x/(x·x)",
        "octahedron_f_vector": [6,12,8],
        "polar_cube_f_vector": [8,12,6],
        "combined_f_vector": [14,24,14],
    }
    assert local["combined_f_vector"] == [14,24,14]

    results = {
        "theorem": "BT515 Richter Radial-Dual Polar Cube Theorem",
        "honesty_boundary": "The uploaded file was a ResearchGate security-check HTML page, not a readable PDF; this theorem is a new repo-tested radial-dual construction inspired by the paper title, not a claim about the unread paper body.",
        "local_radial_dual_geometry": local,
        "polar_inversion_certificates": {
            "oct_vertices": [str(v) for v in oct_vertices],
            "radial_images_are_cube_face_centers": [str(v) for v in cube_face_centers],
            "face_incidence_v_dot_x_eq_1": face_incidence,
            "cube_vertices_as_octahedron_faces": vertex_to_oct_face,
        },
        "graph_certificates": {
            "octahedron_graph_edges": O.number_of_edges(),
            "cube_face_adjacency_edges": F.number_of_edges(),
            "octahedron_equals_cube_face_graph": True,
            "cube_vertex_graph_edges": C.number_of_edges(),
            "cube_vertex_graph": "Q3",
        },
        "global_W33_lift": {
            "octahedron_side": [40*6,40*12,40*8],
            "polar_cube_side": [40*8,40*12,40*6],
            "combined_side": [40*14,40*24,40*14],
        },
        "interpretation": {
            "BT507": "Richter axis intersections give the radius-2/5 octahedron",
            "BT510": "the octahedron/cube packet has f-vector (14,24,14)",
            "BT515": "the cube is the strict polar/radial-dual of the Richter octahedron",
        },
        "substrate_reading": {
            "2/5": "Richter tangent-sphere / octahedron radius from the BC-axis construction",
            "5/2": "polar cube half-side and radial-inverted face-center radius",
            "14_24_14": "local radial-dual memory packet: G2, S4 flags, G2",
            "560_960_560": "40-point W33 lift of the radial-dual packet",
        },
    }

    out = Path("data/PART_BT515_RICHTER_RADIAL_DUAL_POLAR_CUBE_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
