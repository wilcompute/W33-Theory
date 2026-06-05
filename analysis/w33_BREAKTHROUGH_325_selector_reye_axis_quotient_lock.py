"""W(3,3) BREAKTHROUGH 325: selector/Reye axis quotient lock.

BT321 put the Q4/Reye carrier on eight antipodal axes.  Kappa fixes the four
even axes pointwise and swaps endpoints on the four odd axes.  BT324 then
proved that the eight kappa-pulled selectors are two affine projection sheets
with a common kernel <111>.

BT325 identifies these two facts as the same finite object:

    BT324 linear selector fibers = BT321 even/odd antipodal-axis split.

The four BT324 kernel cosets are exactly the four pointwise-fixed even axes.
The BT323 cross-fiber K4,4 is exactly the BT321 Reye quotient graph on axes.
Moreover, grouping selectors by the same BT324 translation gives the coordinate
1 perfect matching inside that K4,4.  Under the Q4 lift this is the coordinate
bit-1 matching, and in BT324's direction plane it is the zero label 00.

This gives an exact finite "now-pivot" statement: the synchronized
translation across the even/odd selector sheets is the same coordinate-1 pivot
already selected by the e-cube route, while the full cross-sheet transition
space remains the four-generator Reye K4,4.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_321_q4_reye_complement_lift_duality import (  # noqa: E402
    antipodal_axes,
    pair,
    quotient_graph,
    q4_reye_complement_lift_duality_packet,
)
from analysis.w33_BREAKTHROUGH_324_selector_affine_fiber_law import (  # noqa: E402
    DIAGONAL_KERNEL,
    DIRECTION_LABELS,
    kernel_cosets,
    selector_affine_fiber_law_packet,
    span_word,
)


Q = 3
MU = 4
NOW_AXIS_XOR = 1


def axis_label_coord(axis_index: int) -> tuple[int, int, int]:
    return ((axis_index >> 0) & 1, (axis_index >> 1) & 1, (axis_index >> 2) & 1)


def axis_label_parity(axis_index: int) -> int:
    return sum(axis_label_coord(axis_index)) % 2


def graph_from_edges(edges: set[tuple[int, int]]) -> dict[int, list[int]]:
    graph = {node: [] for edge in edges for node in edge}
    for left, right in sorted(edges):
        graph[left].append(right)
        graph[right].append(left)
    return {node: sorted(neighbors) for node, neighbors in sorted(graph.items())}


def complete_pairs(nodes: set[int]) -> set[tuple[int, int]]:
    return {pair(left, right) for left in nodes for right in nodes if left < right}


def kernel_coset_axis_indices(axes: list[tuple[int, int]]) -> list[int]:
    axis_index = {axis: index for index, axis in enumerate(axes)}
    result = []
    for coset in kernel_cosets(DIAGONAL_KERNEL):
        words = [span_word(coord) for coord in coset]
        result.append(axis_index[pair(words[0], words[1])])
    return result


def selector_translation_groups(bt324: dict) -> dict[tuple[int, int], list[int]]:
    groups: dict[tuple[int, int], list[int]] = defaultdict(list)
    for row in bt324["selector_rows"]:
        groups[tuple(row["translation"])].append(row["selector_index"])
    return {translation: sorted(indices) for translation, indices in sorted(groups.items())}


def selector_reye_axis_quotient_lock_packet() -> dict:
    bt321 = q4_reye_complement_lift_duality_packet()
    bt324 = selector_affine_fiber_law_packet()
    axes = antipodal_axes()
    _, quotient_edge_lifts = quotient_graph(axes)
    quotient_edges = set(quotient_edge_lifts)
    even_axes = set(bt321["axis_action"]["even_axes_pointwise_fixed"])
    odd_axes = set(bt321["axis_action"]["odd_axes_endpoint_swapped"])

    linear_fibers = {
        linear_part: set(indices)
        for linear_part, indices in bt324["linear_part_fibers"].items()
    }
    fiber_sets = set(frozenset(indices) for indices in linear_fibers.values())
    kernel_axis_indices = kernel_coset_axis_indices(axes)

    two_overlap_edges = {
        pair(left, right)
        for left, right in bt324["pair_intersection_explanation"]["different_linear_part_pairs"]
    }
    disjoint_edges = {
        pair(left, right)
        for left, right in bt324["pair_intersection_explanation"]["equal_linear_part_pairs"]
    }

    translation_groups = selector_translation_groups(bt324)
    same_translation_pairs = {
        pair(indices[0], indices[1])
        for indices in translation_groups.values()
    }
    quotient_edges_by_axis_xor: dict[int, list[tuple[int, int]]] = defaultdict(list)
    quotient_q4_bit_by_axis_xor: dict[int, set[int]] = defaultdict(set)
    for edge, lifts in quotient_edge_lifts.items():
        axis_xor = edge[0] ^ edge[1]
        quotient_edges_by_axis_xor[axis_xor].append(edge)
        quotient_q4_bit_by_axis_xor[axis_xor].update(left ^ right for left, right in lifts)

    quotient_edges_by_axis_xor_json = {
        str(axis_xor): [list(edge) for edge in sorted(edges)]
        for axis_xor, edges in sorted(quotient_edges_by_axis_xor.items())
    }
    quotient_q4_bit_by_axis_xor_json = {
        str(axis_xor): sorted(bits)
        for axis_xor, bits in sorted(quotient_q4_bit_by_axis_xor.items())
    }
    now_matching = set(quotient_edges_by_axis_xor[NOW_AXIS_XOR])

    checks = {
        "bt321_and_bt324_checks_pass": bt321["n_verified"] == len(bt321["checks"])
        and bt324["n_verified"] == len(bt324["checks"]),
        "eight_antipodal_axes_label_F2_3": len(axes) == 2**Q
        and {axis_label_coord(index) for index in range(2**Q)}
        == {
            (0, 0, 0),
            (1, 0, 0),
            (0, 1, 0),
            (1, 1, 0),
            (0, 0, 1),
            (1, 0, 1),
            (0, 1, 1),
            (1, 1, 1),
        },
        "bt321_axis_parity_matches_endpoint_action": even_axes == {
            index for index in range(2**Q) if axis_label_parity(index) == 0
        }
        and odd_axes == {index for index in range(2**Q) if axis_label_parity(index) == 1},
        "bt324_linear_fibers_are_bt321_axis_parity_sheets": fiber_sets == {
            frozenset(even_axes),
            frozenset(odd_axes),
        },
        "bt324_kernel_cosets_are_bt321_even_axes": set(kernel_axis_indices) == even_axes
        and len(kernel_axis_indices) == MU,
        "bt323_two_overlap_graph_is_bt321_reye_quotient_graph": two_overlap_edges == quotient_edges,
        "bt323_disjoint_graph_is_axis_parity_clique_complement": disjoint_edges
        == complete_pairs(even_axes) | complete_pairs(odd_axes),
        "reye_quotient_is_K4_4_between_even_and_odd_axes": all(
            len({edge[0], edge[1]} & even_axes) == 1
            and len({edge[0], edge[1]} & odd_axes) == 1
            for edge in quotient_edges
        )
        and len(quotient_edges) == MU * MU,
        "cross_fiber_edges_split_into_four_perfect_matchings": Counter(
            len(edges) for edges in quotient_edges_by_axis_xor.values()
        )
        == {MU: MU}
        and sorted(quotient_edges_by_axis_xor) == [1, 2, 4, 7],
        "q4_lift_bits_match_axis_xor_generators": quotient_q4_bit_by_axis_xor
        == {1: {1}, 2: {2}, 4: {4}, 7: {8}},
        "translation_groups_pair_even_and_odd_axes": all(
            len(indices) == 2
            and len(set(indices) & even_axes) == 1
            and len(set(indices) & odd_axes) == 1
            for indices in translation_groups.values()
        ),
        "same_translation_pairs_are_coordinate_1_now_matching": same_translation_pairs == now_matching,
        "coordinate_1_now_matching_has_zero_direction_label": DIRECTION_LABELS[1] == (0, 0),
        "now_matching_is_perfect_between_axis_sheets": len(now_matching) == MU
        and {node for edge in now_matching for node in edge} == set(range(2**Q)),
    }

    return {
        "breakthrough": 325,
        "title": "Selector/Reye axis quotient lock",
        "axis_model": {
            "axes": [list(axis) for axis in axes],
            "axis_label_coords": {str(index): list(axis_label_coord(index)) for index in range(2**Q)},
            "even_pointwise_fixed_axes": sorted(even_axes),
            "odd_endpoint_swapped_axes": sorted(odd_axes),
        },
        "selector_axis_lock": {
            "linear_part_fibers": {
                linear_part: sorted(indices)
                for linear_part, indices in sorted(linear_fibers.items())
            },
            "kernel_coset_axis_indices": kernel_axis_indices,
            "kernel_cosets_are_even_axes": sorted(even_axes),
        },
        "graph_lock": {
            "reye_quotient_edges": [list(edge) for edge in sorted(quotient_edges)],
            "bt324_two_overlap_edges": [list(edge) for edge in sorted(two_overlap_edges)],
            "bt324_disjoint_edges": [list(edge) for edge in sorted(disjoint_edges)],
            "reye_quotient_graph": {
                str(node): neighbors for node, neighbors in graph_from_edges(quotient_edges).items()
            },
        },
        "coordinate_matching_decomposition": {
            "axis_xor_to_edges": quotient_edges_by_axis_xor_json,
            "axis_xor_to_q4_lift_bit": quotient_q4_bit_by_axis_xor_json,
            "translation_groups": {
                "".join(map(str, translation)): indices
                for translation, indices in translation_groups.items()
            },
            "same_translation_pairs": [list(edge) for edge in sorted(same_translation_pairs)],
            "now_axis_xor": NOW_AXIS_XOR,
            "now_q4_lift_bit": 1,
            "now_direction_label": list(DIRECTION_LABELS[1]),
        },
        "architectural_reading": (
            "The selector sheets are the Reye axis parity sheets.  BT324's common "
            "<111> kernel quotient is exactly the four pointwise-fixed even axes "
            "from BT321, while the BT323 cross-fiber K4,4 is the BT321 Reye "
            "quotient graph.  Pairing selectors with the same BT324 translation "
            "selects the coordinate-1 perfect matching in that K4,4; in the "
            "BT324 direction plane this is the zero label 00.  This is the exact "
            "finite now-pivot statement, not a continuum retrocausality claim."
        ),
        "boundary": (
            "This packet identifies finite selector/axis/quotient structure.  It "
            "does not assert a physical arrow of time; it only proves which Q4 "
            "coordinate matching synchronizes the two selector sheets."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = selector_reye_axis_quotient_lock_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 325: SELECTOR/REYE AXIS QUOTIENT LOCK")
    print("=" * 78)
    print()
    print(f"axis sheets      = {packet['axis_model']['even_pointwise_fixed_axes']} / {packet['axis_model']['odd_endpoint_swapped_axes']}")
    print(f"kernel axes      = {packet['selector_axis_lock']['kernel_coset_axis_indices']}")
    print(f"now matching     = {packet['coordinate_matching_decomposition']['same_translation_pairs']}")
    print(f"verified         = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = ROOT / "data" / "w33_BREAKTHROUGH_325_selector_reye_axis_quotient_lock.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
