"""Part MCXCIII: Reye tomotope/24-cell common spine.

The tomotope paper identifies the tomotope medial layer I_{1,2} as the Levi
graph of Reye's (12_4, 16_3) configuration.  Independently, the 24-cell has the
same Reye configuration: 12 antipodal axes through its D4-root vertices and 16
hexagonal central planes.

This verifier builds the 24-cell side directly from the D4 roots

    permutations of (+/-1, +/-1, 0, 0),

then proves that the axis/hexagon incidence graph is isomorphic to the same
Reye graph used in MCLXXXII.  The common automorphism group has order 576,
which is simultaneously 6 times the tomotope automorphism order 96 and the
rotational symmetry order of the 24-cell.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import Any

import networkx as nx
from networkx.algorithms import isomorphism as iso


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "exploration"):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from analysis.w33_q4_tomotope_reye_double_cover import reye_configuration_graph  # noqa: E402
from exploration.w33_d4_f4_tomotope_reye_bridge import (  # noqa: E402
    build_d4_f4_tomotope_reye_summary,
)


Vector4 = tuple[int, int, int, int]
Axis = tuple[Vector4, Vector4]


def d4_roots() -> list[Vector4]:
    """The 24 D4 roots / 24-cell vertices: permutations of (+/-1,+/-1,0,0)."""

    roots: list[Vector4] = []
    for left, right in combinations(range(4), 2):
        for left_sign, right_sign in product((-1, 1), repeat=2):
            vector = [0, 0, 0, 0]
            vector[left] = left_sign
            vector[right] = right_sign
            roots.append(tuple(vector))  # type: ignore[arg-type]
    return sorted(roots)


def rank_rational(vectors: list[Vector4]) -> int:
    """Exact rank over Q for short integer vectors."""

    matrix = [[Fraction(entry) for entry in vector] for vector in vectors]
    rows = len(matrix)
    cols = 4
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if matrix[row][col]:
                pivot = row
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][col]
        matrix[rank] = [entry / scale for entry in matrix[rank]]
        for row in range(rows):
            if row != rank and matrix[row][col]:
                factor = matrix[row][col]
                matrix[row] = [matrix[row][idx] - factor * matrix[rank][idx] for idx in range(cols)]
        rank += 1
    return rank


def twenty_four_cell_axes(roots: list[Vector4] | None = None) -> list[Axis]:
    """Pair opposite D4 roots into the 12 axes of the 24-cell."""

    roots = d4_roots() if roots is None else roots
    seen: set[Vector4] = set()
    axes: list[Axis] = []
    for root in roots:
        if root in seen:
            continue
        opposite = tuple(-entry for entry in root)  # type: ignore[assignment]
        axis = tuple(sorted((root, opposite)))  # type: ignore[assignment]
        axes.append(axis)
        seen.add(root)
        seen.add(opposite)
    return sorted(axes)


def twenty_four_cell_hexagon_planes(roots: list[Vector4], axes: list[Axis]) -> list[tuple[int, int, int]]:
    """Find the 16 central hexagon planes as triples of axes spanning a 2-plane."""

    planes: list[tuple[int, int, int]] = []
    for triple in combinations(range(len(axes)), 3):
        plane_vectors = [vector for axis_index in triple for vector in axes[axis_index]]
        if rank_rational(plane_vectors) != 2:
            continue
        roots_in_plane = [root for root in roots if rank_rational([*plane_vectors, root]) == 2]
        if len(roots_in_plane) == 6:
            planes.append(triple)
    return planes


def twenty_four_cell_reye_graph() -> dict[str, Any]:
    roots = d4_roots()
    axes = twenty_four_cell_axes(roots)
    hexagon_planes = twenty_four_cell_hexagon_planes(roots, axes)

    graph = nx.Graph()
    for index, axis in enumerate(axes):
        graph.add_node(("A", index), kind="point", axis=axis)
    for index, plane in enumerate(hexagon_planes):
        graph.add_node(("H", index), kind="line", axes=plane)
        for axis_index in plane:
            graph.add_edge(("A", axis_index), ("H", index))

    return {
        "graph": graph,
        "roots": roots,
        "axes": axes,
        "hexagon_planes": hexagon_planes,
    }


def automorphism_count(graph: nx.Graph) -> int:
    matcher = iso.GraphMatcher(graph, graph, node_match=iso.categorical_node_match("kind", None))
    return sum(1 for _ in matcher.isomorphisms_iter())


def degree_profile(graph: nx.Graph) -> dict[int, int]:
    return dict(sorted(Counter(dict(graph.degree()).values()).items()))


def reye_tomotope_24cell_common_spine_packet() -> dict[str, Any]:
    mclxxxii = json.loads((ROOT / "PART_MCLXXXII_Q4_TOMOTOPE_REYE_DOUBLE_COVER_results.json").read_text())
    mcxcii = json.loads((ROOT / "PART_MCXCII_REYE_K12_ORIENTABLE_HORIZON_COMPLETION_results.json").read_text())
    d4_f4 = build_d4_f4_tomotope_reye_summary()

    cell24 = twenty_four_cell_reye_graph()
    graph24 = cell24["graph"]
    cube_reye = reye_configuration_graph()["graph"]
    node_match = iso.categorical_node_match("kind", None)
    isomorphic_to_cube_reye = nx.is_isomorphic(graph24, cube_reye, node_match=node_match)
    aut_count = automorphism_count(graph24)

    axes = len(cell24["axes"])
    hexagons = len(cell24["hexagon_planes"])
    incidences = graph24.number_of_edges()
    tomotope_edges = int(mclxxxii["tomotope_lock"]["edges"])
    tomotope_triangles = int(mclxxxii["tomotope_lock"]["triangles"])
    tomotope_medial = int(mclxxxii["tomotope_lock"]["edge_triangle_medial_incidences"])
    tomotope_aut = int(mclxxxii["tomotope_lock"]["automorphism_group_order"])
    rotational_24 = int(d4_f4["f4_triality_lift"]["twenty_four_cell_rotational_symmetry_order"])
    weyl_f4 = int(d4_f4["f4_triality_lift"]["weyl_f4_order"])

    checks = {
        "d4_roots_are_24cell_vertices": len(cell24["roots"]) == 24,
        "opposite_root_pairs_are_12_axes": axes == 12,
        "central_hexagon_planes_are_16": hexagons == 16,
        "axis_hexagon_incidence_is_48": incidences == 48,
        "axis_hexagon_profile_is_reye": degree_profile(graph24) == {3: 16, 4: 12},
        "each_axis_lies_on_four_hexagons": all(graph24.degree(("A", idx)) == 4 for idx in range(axes)),
        "each_hexagon_plane_contains_three_axes": all(graph24.degree(("H", idx)) == 3 for idx in range(hexagons)),
        "cell24_reye_is_cube_reye": isomorphic_to_cube_reye,
        "reye_automorphism_order_is_576": aut_count == 576,
        "tomotope_edges_match_24cell_axes": tomotope_edges == axes == 12,
        "tomotope_triangles_match_24cell_hexagons": tomotope_triangles == hexagons == 16,
        "tomotope_medial_matches_24cell_reye_incidence": tomotope_medial == incidences == 48,
        "reye_automorphism_is_six_times_tomotope_automorphism": aut_count == 6 * tomotope_aut == 576,
        "reye_automorphism_is_24cell_rotational_symmetry": aut_count == rotational_24 == 576,
        "weyl_f4_is_two_times_common_reye_symmetry": weyl_f4 == 2 * aut_count == 1152,
        "k12_horizon_uses_same_12_reye_points": int(mcxcii["input_anchor"]["reye_points"]) == axes,
        "k12_horizon_uses_same_16_reye_lines": int(mcxcii["input_anchor"]["reye_lines"]) == hexagons,
        "common_spine_is_12_4_16_3": axes * 4 == hexagons * 3 == incidences,
    }

    return {
        "part": "MCXCIII",
        "theorem": "Reye tomotope/24-cell common spine",
        "external_source_alignment": {
            "tomotope_paper": "The tomotope text identifies I_{1,2}, the edge-triangle medial layer, with Reye's configuration and gives automorphism order 576.",
            "dlib_record": "dLib provides the 2012 Ars Mathematica Contemporanea record and TXT/PDF entries for The tomotope.",
            "24cell_references": "24-cell references describe the same Reye configuration as 12 axes and 16 hexagon planes.",
        },
        "twenty_four_cell_model": {
            "vertices": len(cell24["roots"]),
            "d4_root_formula": "permutations of (+/-1,+/-1,0,0)",
            "axes": axes,
            "hexagon_planes": hexagons,
            "axis_hexagon_incidences": incidences,
            "degree_profile": degree_profile(graph24),
            "automorphism_count": aut_count,
            "hexagon_plane_axis_triples": [list(plane) for plane in cell24["hexagon_planes"]],
        },
        "tomotope_match": {
            "tomotope_edges": tomotope_edges,
            "tomotope_triangles": tomotope_triangles,
            "tomotope_medial_incidences": tomotope_medial,
            "tomotope_automorphism_order": tomotope_aut,
            "reye_automorphism_over_tomotope_automorphism": aut_count // tomotope_aut,
        },
        "symmetry_lock": {
            "reye_automorphism_order": aut_count,
            "twenty_four_cell_rotational_symmetry_order": rotational_24,
            "weyl_f4_order": weyl_f4,
            "identity": "576 = 6*96 = |W(F4)|/2",
        },
        "horizon_anchor": {
            "mcxcii_k12_reye_points": int(mcxcii["input_anchor"]["reye_points"]),
            "mcxcii_k12_reye_lines": int(mcxcii["input_anchor"]["reye_lines"]),
            "reading": "MCXCII uses this same common Reye spine as the 12-vertex, 16-triangle seed inside the K12 horizon",
        },
        "reading": (
            "Reye is the exact shared spine of the tomotope and the 24-cell: "
            "tomotope edges correspond to 24-cell antipodal axes, tomotope "
            "triangles correspond to 24-cell hexagon planes, and the common Levi "
            "graph has 48 incidences and 576 automorphisms. The Q4/tomotope/K12 "
            "chain is therefore attached to the classical D4/F4 24-cell geometry "
            "through the same Reye configuration, not merely through matching counts."
        ),
        "claim_boundary": (
            "finite incidence-isomorphism theorem; this identifies a common Reye "
            "spine for tomotope and 24-cell combinatorics, not a continuum dynamics proof"
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = reye_tomotope_24cell_common_spine_packet()
    out_path = ROOT / "PART_MCXCIII_REYE_TOMOTOPE_24CELL_COMMON_SPINE_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCXCIII: Reye Tomotope/24-Cell Common Spine ===")
    print("24-cell roots/axes/hexagons:", packet["twenty_four_cell_model"]["vertices"], packet["twenty_four_cell_model"]["axes"], packet["twenty_four_cell_model"]["hexagon_planes"])
    print("Reye incidences:", packet["twenty_four_cell_model"]["axis_hexagon_incidences"])
    print("symmetry:", packet["symmetry_lock"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
