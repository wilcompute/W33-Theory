"""W(3,3) BREAKTHROUGH 321: Q4/Reye complement lift duality.

BT320 found the unique non-coordinate C2 that doubles the BT319 selector D4
inside GL(4,2):

    kappa = J + I over F2 = [14, 13, 11, 7].

This packet identifies what kappa does on the Q4/Reye/tomotope carrier already
used by the self-entanglement papers.

On the 16 Q4 vertices, kappa acts by parity:

    even words -> fixed
    odd words  -> antipodal complement.

Therefore kappa fixes every antipodal axis setwise.  It is invisible on the
8-axis Reye quotient, but it is not trivial on the two-sheet lift:

    Q4 edge lift (weight-1 difference)
        <-> cubical body-diagonal lift (weight-3 difference)

over the same quotient edge.  Each of the 16 quotient K4,4/Reye edges has four
cross-sheet lifts between its two antipodal axes: two Q4 edges and two
distance-3 body diagonals.  Kappa swaps those two lift species while leaving the
quotient edge unchanged.

So the BT320 complement C2 is the hidden edge/cell-diagonal lift duality above
the already verified Q4 -> Reye -> tomotope/24-cell common spine.  It is not a
new tomotope automorphism claim; it is the local Q4 lift operation that the
Reye quotient forgets.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_320_ecube_d4_gl42_normalizer import (  # noqa: E402
    COMPLEMENT_INVOLUTION,
    row_times_matrix,
)


Q = 3
LAMBDA = 2
MU = 4
K = 12
TOMOTOPE = (4, 12, 16, 8)
ALL_ONES = 15
VERTICES = tuple(range(16))
BITS = (1, 2, 4, 8)


def weight(word: int) -> int:
    return word.bit_count()


def parity(word: int) -> int:
    return weight(word) % 2


def kappa(word: int) -> int:
    return row_times_matrix(word, COMPLEMENT_INVOLUTION)


def pair(a: int, b: int) -> tuple[int, int]:
    return tuple(sorted((a, b)))


def antipodal_axes() -> list[tuple[int, int]]:
    axes = []
    seen = set()
    for vertex in VERTICES:
        if vertex in seen:
            continue
        axis = pair(vertex, ALL_ONES ^ vertex)
        axes.append(axis)
        seen.update(axis)
    return axes


def q4_edges() -> set[tuple[int, int]]:
    return {pair(vertex, vertex ^ bit) for vertex in VERTICES for bit in BITS}


def distance_three_pairs() -> set[tuple[int, int]]:
    return {
        pair(a, b)
        for a, b in combinations(VERTICES, 2)
        if weight(a ^ b) == Q
    }


def cubical_3faces() -> list[dict]:
    faces = []
    for fixed_bit_index, fixed_bit in enumerate(BITS):
        free_bits = [bit for bit in BITS if bit != fixed_bit]
        for fixed_value in (0, 1):
            vertices = [
                sum(bit for bit, value in zip(free_bits, values) if value) | (fixed_bit if fixed_value else 0)
                for values in product((0, 1), repeat=3)
            ]
            diagonals = {
                pair(a, b)
                for a, b in combinations(vertices, 2)
                if weight(a ^ b) == Q
            }
            faces.append(
                {
                    "fixed_coordinate": fixed_bit_index,
                    "fixed_bit": fixed_bit,
                    "fixed_value": fixed_value,
                    "vertices": sorted(vertices),
                    "body_diagonals": sorted(diagonals),
                }
            )
    return faces


def quotient_graph(axes: list[tuple[int, int]]) -> tuple[dict[int, int], dict[tuple[int, int], list[tuple[int, int]]]]:
    axis_of = {vertex: index for index, axis in enumerate(axes) for vertex in axis}
    lifts_by_quotient_edge: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for edge in q4_edges():
        qa = axis_of[edge[0]]
        qb = axis_of[edge[1]]
        lifts_by_quotient_edge[pair(qa, qb)].append(edge)
    return axis_of, dict(lifts_by_quotient_edge)


def all_cross_pairs_for_quotient_edge(
    quotient_edge: tuple[int, int], axes: list[tuple[int, int]]
) -> set[tuple[int, int]]:
    left_axis = axes[quotient_edge[0]]
    right_axis = axes[quotient_edge[1]]
    return {pair(a, b) for a in left_axis for b in right_axis}


def q4_reye_complement_lift_duality_packet() -> dict:
    axes = antipodal_axes()
    axis_of, edge_lifts = quotient_graph(axes)
    edge_set = q4_edges()
    diagonal_set = distance_three_pairs()
    faces = cubical_3faces()

    kappa_vertex_image = {vertex: kappa(vertex) for vertex in VERTICES}
    fixed_vertices = [vertex for vertex, image in kappa_vertex_image.items() if vertex == image]
    moved_vertices = [vertex for vertex, image in kappa_vertex_image.items() if vertex != image]
    vertex_orbits = []
    seen = set()
    for vertex in VERTICES:
        if vertex in seen:
            continue
        orbit = sorted({vertex, kappa(vertex)})
        vertex_orbits.append(orbit)
        seen.update(orbit)

    axis_action = {index: pair(kappa(axis[0]), kappa(axis[1])) for index, axis in enumerate(axes)}
    even_axes = [index for index, axis in enumerate(axes) if all(parity(vertex) == 0 for vertex in axis)]
    odd_axes = [index for index, axis in enumerate(axes) if all(parity(vertex) == 1 for vertex in axis)]
    pointwise_fixed_axes = [
        index
        for index, axis in enumerate(axes)
        if all(kappa(vertex) == vertex for vertex in axis)
    ]
    endpoint_swapped_axes = [
        index
        for index, axis in enumerate(axes)
        if pair(kappa(axis[0]), kappa(axis[1])) == axis and kappa(axis[0]) != axis[0]
    ]

    quotient_diagonal_lifts: dict[tuple[int, int], list[tuple[int, int]]] = {}
    lift_profiles = {}
    kappa_edge_images = {edge: pair(kappa(edge[0]), kappa(edge[1])) for edge in edge_set}
    kappa_diagonal_images = {diag: pair(kappa(diag[0]), kappa(diag[1])) for diag in diagonal_set}
    for quotient_edge, lifts in edge_lifts.items():
        cross_pairs = all_cross_pairs_for_quotient_edge(quotient_edge, axes)
        diagonal_lifts = sorted(cross_pairs & diagonal_set)
        quotient_diagonal_lifts[quotient_edge] = diagonal_lifts
        lift_profiles[quotient_edge] = {
            "q4_edge_lifts": sorted(lifts),
            "distance3_diagonal_lifts": diagonal_lifts,
            "all_cross_pairs": sorted(cross_pairs),
        }

    hinge = 0
    hinge_neighbors = sorted({other for edge in edge_lifts for other in edge if hinge in edge and other != hinge})
    direction_axes = sorted(set(range(len(axes))) - {hinge} - set(hinge_neighbors))
    nonhinge_edges = [edge for edge in edge_lifts if hinge not in edge]

    face_diagonals = {diag for face in faces for diag in face["body_diagonals"]}
    diagonal_face_membership = Counter(
        diag for face in faces for diag in face["body_diagonals"]
    )

    checks = {
        "kappa_row_masks_are_bt320_complement": COMPLEMENT_INVOLUTION == (14, 13, 11, 7),
        "kappa_is_involution_on_vertices": all(kappa(kappa(vertex)) == vertex for vertex in VERTICES),
        "kappa_fixes_exactly_even_words": fixed_vertices == [v for v in VERTICES if parity(v) == 0],
        "kappa_moves_exactly_odd_words": moved_vertices == [v for v in VERTICES if parity(v) == 1],
        "vertex_orbit_split_8_fixed_4_pairs": Counter(len(orbit) for orbit in vertex_orbits) == {1: 8, 2: 4},
        "antipodal_axes_count_8": len(axes) == 2**Q,
        "kappa_fixes_every_axis_setwise": all(axis_action[index] == axis for index, axis in enumerate(axes)),
        "even_axes_pointwise_fixed_count_4": pointwise_fixed_axes == even_axes and len(even_axes) == MU,
        "odd_axes_endpoint_swapped_count_4": endpoint_swapped_axes == odd_axes and len(odd_axes) == MU,
        "q4_edges_count_32": len(edge_set) == 32,
        "distance3_pairs_count_32": len(diagonal_set) == 32,
        "cubical_3faces_count_8": len(faces) == 2**Q,
        "cubical_body_diagonals_are_distance3_pairs": face_diagonals == diagonal_set,
        "each_distance3_pair_lies_in_one_cubical_3face": diagonal_face_membership == {diag: 1 for diag in diagonal_set},
        "kappa_maps_q4_edges_to_distance3_diagonals": set(kappa_edge_images.values()) == diagonal_set,
        "kappa_maps_distance3_diagonals_to_q4_edges": set(kappa_diagonal_images.values()) == edge_set,
        "quotient_edges_count_16": len(edge_lifts) == 16,
        "each_quotient_edge_has_two_q4_edge_lifts": all(len(lifts) == LAMBDA for lifts in edge_lifts.values()),
        "each_quotient_edge_has_two_distance3_lifts": all(
            len(lifts) == LAMBDA for lifts in quotient_diagonal_lifts.values()
        ),
        "each_quotient_edge_has_four_cross_pairs": all(
            len(all_cross_pairs_for_quotient_edge(edge, axes)) == MU for edge in edge_lifts
        ),
        "kappa_preserves_quotient_edge_while_swapping_lift_species": all(
            kappa_edge_images[lift] in quotient_diagonal_lifts[quotient_edge]
            for quotient_edge, lifts in edge_lifts.items()
            for lift in lifts
        )
        and all(
            kappa_diagonal_images[lift] in edge_lifts[quotient_edge]
            for quotient_edge, lifts in quotient_diagonal_lifts.items()
            for lift in lifts
        ),
        "hinge_neighbors_are_odd_affine_axes": hinge_neighbors == odd_axes,
        "direction_axes_are_even_nonhinge_axes": direction_axes == [axis for axis in even_axes if axis != hinge],
        "tomotope_fvector_from_q4_reye_split": (
            len(hinge_neighbors),
            len(nonhinge_edges),
            len(edge_lifts),
            len(axes),
        )
        == TOMOTOPE,
    }

    return {
        "breakthrough": 321,
        "title": "Q4/Reye complement lift duality",
        "kappa": {
            "row_masks": list(COMPLEMENT_INVOLUTION),
            "formula": "x -> x if wt(x) is even, else 15 xor x",
            "matrix_description": "J + I over F2",
        },
        "vertex_action": {
            "fixed_vertices": fixed_vertices,
            "moved_vertices": moved_vertices,
            "orbits": vertex_orbits,
            "orbit_size_distribution": dict(sorted(Counter(len(orbit) for orbit in vertex_orbits).items())),
        },
        "axis_action": {
            "axes": [list(axis) for axis in axes],
            "even_axes_pointwise_fixed": even_axes,
            "odd_axes_endpoint_swapped": odd_axes,
            "quotient_action": "identity on all 8 antipodal axes",
        },
        "lift_duality": {
            "q4_edges": len(edge_set),
            "distance3_body_diagonals": len(diagonal_set),
            "quotient_edges": len(edge_lifts),
            "per_quotient_edge": "2 Q4 edge lifts + 2 distance-3 cubical body-diagonal lifts",
            "profiles": {
                f"{edge[0]}-{edge[1]}": {
                    "q4_edge_lifts": [list(lift) for lift in profile["q4_edge_lifts"]],
                    "distance3_diagonal_lifts": [list(lift) for lift in profile["distance3_diagonal_lifts"]],
                    "all_cross_pairs": [list(lift) for lift in profile["all_cross_pairs"]],
                }
                for edge, profile in sorted(lift_profiles.items())
            },
        },
        "cubical_cell_layer": {
            "cubical_3faces": len(faces),
            "body_diagonals_total": len(face_diagonals),
            "body_diagonals_per_face": [len(face["body_diagonals"]) for face in faces],
        },
        "tomotope_reye_reading": {
            "hinge_axis": hinge,
            "affine_point_axes": hinge_neighbors,
            "direction_axes": direction_axes,
            "f_vector": list(TOMOTOPE),
            "reading": (
                "The complement involution is invisible on the Reye quotient but "
                "nontrivial on the Q4 two-sheet lift: it toggles the four affine "
                "point axes and swaps edge lifts with cubical cell-diagonal lifts."
            ),
        },
        "boundary": (
            "This identifies the BT320 complement C2 as a Q4/Reye lift-duality. "
            "It does not claim this map alone is the full tomotope automorphism "
            "group or the full 24-cell/Reye common-spine symmetry."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = q4_reye_complement_lift_duality_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 321: Q4/REYE COMPLEMENT LIFT DUALITY")
    print("=" * 78)
    print()
    print(f"kappa row masks       = {packet['kappa']['row_masks']}")
    print(f"vertex orbit split    = {packet['vertex_action']['orbit_size_distribution']}")
    print(f"axis quotient action   = {packet['axis_action']['quotient_action']}")
    print(f"Q4 edges              = {packet['lift_duality']['q4_edges']}")
    print(f"distance-3 diagonals  = {packet['lift_duality']['distance3_body_diagonals']}")
    print(f"quotient edges        = {packet['lift_duality']['quotient_edges']}")
    print(f"verified              = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("TOMOTOPE/REYE READING:")
    print(f"  {packet['tomotope_reye_reading']['reading']}")

    out = ROOT / "data" / "w33_BREAKTHROUGH_321_q4_reye_complement_lift_duality.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
