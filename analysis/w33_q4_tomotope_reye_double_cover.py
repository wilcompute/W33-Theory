"""Part MCLXXXII: Q4 antipodal tomotope-Reye double cover.

MCLXXXI found that the Q4 router has 24 square faces and 96 face-edge
incidences.  The tomotope clue is stronger than a count match:

    Q4 face-edge incidence / antipodal translation = Reye (12_4, 16_3).

The quotient has 12 face-orbits, 16 edge-orbits, and 48 incidences.  This is
exactly the Reye configuration model used for the tomotope edge-triangle medial
layer: 12 points, 16 lines, each point on 4 lines, each line on 3 points.

Thus the live Q4 plaquette packet is a two-sheet cover of the tomotope/Reye
medial layer.  The 96 lifted incidences also equal the tomotope automorphism
order, while adding the tomotope vertex-choice factor gives 192 flags.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict, deque
from itertools import product
from pathlib import Path
from typing import Any

import networkx as nx
from networkx.algorithms import isomorphism as iso


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "exploration"):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from analysis.w33_q4_plaquette_directed_change_lift import (  # noqa: E402
    face_edges,
    q4_square_faces,
)
from exploration.w33_tomotope_order_bridge import build_tomotope_order_summary  # noqa: E402


Bits4 = tuple[int, int, int, int]
Bits3 = tuple[int, int, int]
Face = tuple[Bits4, Bits4, Bits4, Bits4]
Edge = tuple[Bits4, Bits4]
Node = tuple[str, int]
Point = tuple[str, object]


ANTIPODAL: Bits4 = (1, 1, 1, 1)


def _xor4(left: Bits4, right: Bits4 = ANTIPODAL) -> Bits4:
    return tuple(a ^ b for a, b in zip(left, right))  # type: ignore[return-value]


def _canonical_edge(left: Bits4, right: Bits4) -> Edge:
    return tuple(sorted((left, right)))  # type: ignore[return-value]


def _translate_face(face: Face) -> Face:
    return tuple(sorted(_xor4(vertex) for vertex in face))  # type: ignore[return-value]


def _translate_edge(edge: Edge) -> Edge:
    return _canonical_edge(_xor4(edge[0]), _xor4(edge[1]))


def _connected_components(graph: nx.Graph) -> list[int]:
    return sorted(len(component) for component in nx.connected_components(graph))


def _degree_profile(graph: nx.Graph) -> dict[int, int]:
    return dict(sorted(Counter(dict(graph.degree()).values()).items()))


def q4_face_edge_incidence_graph() -> tuple[nx.Graph, list[Face], list[Edge]]:
    """Build the bipartite graph between Q4 square faces and Q4 edges."""

    faces = [tuple(face["vertices"]) for face in q4_square_faces()]  # type: ignore[list-item]
    edges = sorted({edge for face in faces for edge in face_edges(face)})
    edge_index = {edge: index for index, edge in enumerate(edges)}

    graph = nx.Graph()
    for index, _face in enumerate(faces):
        graph.add_node(("F", index), kind="face")
    for index, _edge in enumerate(edges):
        graph.add_node(("E", index), kind="edge")
    for face_index, face in enumerate(faces):
        for edge in face_edges(face):
            graph.add_edge(("F", face_index), ("E", edge_index[edge]))
    return graph, faces, edges


def antipodal_orbits(items: list[Any], translate: Any) -> list[tuple[int, int]]:
    """Two-element orbits under the antipodal Q4 translation."""

    index = {item: item_index for item_index, item in enumerate(items)}
    seen: set[int] = set()
    orbits: list[tuple[int, int]] = []
    for item_index, item in enumerate(items):
        if item_index in seen:
            continue
        mate_index = index[translate(item)]
        orbit = tuple(sorted((item_index, mate_index)))
        seen.update(orbit)
        orbits.append(orbit)  # type: ignore[arg-type]
    return orbits


def q4_antipodal_quotient_graph() -> dict[str, Any]:
    """Quotient Q4 face-edge incidence by bitwise complement."""

    source_graph, faces, edges = q4_face_edge_incidence_graph()
    face_orbits = antipodal_orbits(faces, _translate_face)
    edge_orbits = antipodal_orbits(edges, _translate_edge)
    face_orbit_of = {face_index: orbit_index for orbit_index, orbit in enumerate(face_orbits) for face_index in orbit}
    edge_orbit_of = {edge_index: orbit_index for orbit_index, orbit in enumerate(edge_orbits) for edge_index in orbit}
    edge_index = {edge: index for index, edge in enumerate(edges)}

    quotient = nx.Graph()
    for index, orbit in enumerate(face_orbits):
        quotient.add_node(("P", index), kind="point", orbit=orbit)
    for index, orbit in enumerate(edge_orbits):
        quotient.add_node(("L", index), kind="line", orbit=orbit)

    multiplicities: Counter[tuple[int, int]] = Counter()
    for face_index, face in enumerate(faces):
        for edge in face_edges(face):
            q_face = face_orbit_of[face_index]
            q_edge = edge_orbit_of[edge_index[edge]]
            multiplicities[(q_face, q_edge)] += 1
            quotient.add_edge(("P", q_face), ("L", q_edge))

    return {
        "source_graph": source_graph,
        "quotient_graph": quotient,
        "faces": faces,
        "edges": edges,
        "face_orbits": face_orbits,
        "edge_orbits": edge_orbits,
        "multiplicities": multiplicities,
    }


def reye_configuration_graph() -> dict[str, Any]:
    """Classical Reye model: cube vertices, center, infinity points, edges, diagonals."""

    finite_points: list[Point] = [("v", bits) for bits in product((0, 1), repeat=3)]
    points: list[Point] = [*finite_points, ("center", 0), *[("infinity", dim) for dim in range(3)]]
    lines: list[dict[str, Any]] = []

    for dim in range(3):
        frozen_dims = [candidate for candidate in range(3) if candidate != dim]
        for frozen_values in product((0, 1), repeat=2):
            left = [0, 0, 0]
            right = [0, 0, 0]
            for frozen_dim, value in zip(frozen_dims, frozen_values):
                left[frozen_dim] = value
                right[frozen_dim] = value
            left[dim] = 0
            right[dim] = 1
            lines.append(
                {
                    "kind": "cube_edge",
                    "dimension": dim,
                    "frozen_values": frozen_values,
                    "points": [("v", tuple(left)), ("v", tuple(right)), ("infinity", dim)],
                }
            )

    for bits in product((0, 1), repeat=3):
        if bits[0] != 0:
            continue
        opposite = tuple(1 - bit for bit in bits)
        lines.append(
            {
                "kind": "body_diagonal",
                "start": bits,
                "points": [("v", bits), ("v", opposite), ("center", 0)],
            }
        )

    graph = nx.Graph()
    for index, point in enumerate(points):
        graph.add_node(("P", index), kind="point", label=repr(point))
    for index, line in enumerate(lines):
        graph.add_node(("L", index), kind="line", label=repr(line))
        for point in line["points"]:
            graph.add_edge(("P", points.index(point)), ("L", index))

    return {"graph": graph, "points": points, "lines": lines}


def _tomotope_data() -> dict[str, int]:
    summary = build_tomotope_order_summary()
    tomotope = summary["tomotope"]
    return {
        "vertices": int(tomotope["vertices"]),
        "edges": int(tomotope["edges"]),
        "triangles": int(tomotope["triangles"]),
        "tetrahedra": int(tomotope["tetrahedra"]),
        "hemioctahedra": int(tomotope["hemioctahedra"]),
        "cells": int(tomotope["tetrahedra"]) + int(tomotope["hemioctahedra"]),
        "automorphism_group_order": int(tomotope["automorphism_group_order"]),
        "monodromy_group_order": int(tomotope["monodromy_group_order"]),
        "flags": int(tomotope["flags"]),
    }


def q4_tomotope_reye_double_cover_packet() -> dict[str, Any]:
    q4 = q4_antipodal_quotient_graph()
    reye = reye_configuration_graph()
    tomotope = _tomotope_data()

    source = q4["source_graph"]
    quotient = q4["quotient_graph"]
    reye_graph = reye["graph"]
    multiplicities: Counter[tuple[int, int]] = q4["multiplicities"]
    node_match = iso.categorical_node_match("kind", None)
    quotient_is_reye = nx.is_isomorphic(quotient, reye_graph, node_match=node_match)

    source_incidences = source.number_of_edges()
    quotient_incidences = quotient.number_of_edges()
    reye_incidences = reye_graph.number_of_edges()
    tomotope_medial_incidences = tomotope["edges"] * 4

    checks = {
        "q4_source_is_mclxxxi_incidence_graph": source.number_of_nodes() == 56 and source_incidences == 96,
        "q4_source_is_connected": nx.is_connected(source),
        "antipodal_has_twelve_face_orbits": len(q4["face_orbits"]) == 12,
        "antipodal_has_sixteen_edge_orbits": len(q4["edge_orbits"]) == 16,
        "antipodal_has_no_fixed_faces": all(left != right for left, right in q4["face_orbits"]),
        "antipodal_has_no_fixed_edges": all(left != right for left, right in q4["edge_orbits"]),
        "quotient_has_reye_size": quotient.number_of_nodes() == 28 and quotient_incidences == 48,
        "quotient_degree_profile_is_reye_profile": _degree_profile(quotient) == {3: 16, 4: 12},
        "quotient_is_connected": nx.is_connected(quotient),
        "each_quotient_incidence_has_two_lifts": dict(Counter(multiplicities.values())) == {2: 48},
        "reye_has_12_points_16_lines": len(reye["points"]) == 12 and len(reye["lines"]) == 16,
        "reye_incidence_profile_is_12_4_16_3": _degree_profile(reye_graph) == {3: 16, 4: 12},
        "reye_is_connected": nx.is_connected(reye_graph),
        "q4_antipodal_quotient_is_reye": quotient_is_reye,
        "tomotope_medial_count_is_reye": tomotope_medial_incidences == reye_incidences == 48,
        "q4_incidence_is_double_tomotope_medial": source_incidences == 2 * tomotope_medial_incidences == 96,
        "q4_incidence_equals_tomotope_automorphism_order": (
            source_incidences == tomotope["automorphism_group_order"] == 96
        ),
        "tomotope_flags_are_two_q4_incidence_packets": tomotope["flags"] == 2 * source_incidences == 192,
        "tomotope_cells_match_q4_cube_facets": tomotope["cells"] == 8,
        "claim_boundary_preserved": quotient_is_reye and tomotope["flags"] == 192,
    }

    return {
        "part": "MCLXXXII",
        "theorem": "Q4 antipodal tomotope-Reye double cover",
        "external_source_alignment": {
            "networkx_hypercube_graph": "Q_n nodes are bit tuples and edges differ in exactly one bit",
            "mathworld_hypercube": "the tesseract has 16 vertices, 32 edges, 24 squares, and 8 cubes",
            "tomotope_paper": "the tomotope medial layer I_{1,2} has Reye parameters (12_4, 16_3)",
        },
        "q4_source": {
            "face_nodes": 24,
            "edge_nodes": 32,
            "incidences": source_incidences,
            "degree_profile": _degree_profile(source),
            "component_sizes": _connected_components(source),
        },
        "antipodal_quotient": {
            "translation": ANTIPODAL,
            "face_orbits": len(q4["face_orbits"]),
            "edge_orbits": len(q4["edge_orbits"]),
            "incidences": quotient_incidences,
            "degree_profile": _degree_profile(quotient),
            "component_sizes": _connected_components(quotient),
            "incidence_lift_multiplicity_profile": dict(sorted(Counter(multiplicities.values()).items())),
            "isomorphic_to_reye": quotient_is_reye,
        },
        "reye_model": {
            "points": len(reye["points"]),
            "lines": len(reye["lines"]),
            "incidences": reye_incidences,
            "point_line_profile": "12_4, 16_3",
            "degree_profile": _degree_profile(reye_graph),
            "component_sizes": _connected_components(reye_graph),
            "construction": "12 points = cube vertices + center + 3 infinity points; 16 lines = 12 cube edges + 4 body diagonals",
        },
        "tomotope_lock": {
            **tomotope,
            "edge_triangle_medial_incidences": tomotope_medial_incidences,
            "q4_to_medial_cover_degree": source_incidences // tomotope_medial_incidences,
            "q4_incidence_equals_automorphism_group_order": source_incidences == tomotope["automorphism_group_order"],
            "tomotope_flags_over_q4_incidence": tomotope["flags"] // source_incidences,
        },
        "reading": (
            "The MCLXXXI Q4 plaquette packet is a connected two-sheet antipodal cover "
            "of the Reye incidence graph that the tomotope paper identifies with the "
            "tomotope edge-triangle medial layer. The lifted 96 incidences are exactly "
            "the tomotope automorphism order; adjoining the remaining rank-0 vertex "
            "choice doubles this to the 192 tomotope flags."
        ),
        "claim_boundary": (
            "finite incidence-cover theorem only; this proves a Q4/tomotope-Reye "
            "combinatorial bridge, not a continuum field equation"
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = q4_tomotope_reye_double_cover_packet()
    out_path = ROOT / "PART_MCLXXXII_Q4_TOMOTOPE_REYE_DOUBLE_COVER_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXXII: Q4 Antipodal Tomotope-Reye Double Cover ===")
    print("Q4 face-edge incidences:", packet["q4_source"]["incidences"])
    print("Antipodal quotient:", packet["antipodal_quotient"]["face_orbits"], "x", packet["antipodal_quotient"]["edge_orbits"])
    print("Reye incidence profile:", packet["reye_model"]["point_line_profile"])
    print("Tomotope lock: 48 medial, 96 automorphism, 192 flags")
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
