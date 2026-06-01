"""Part MMCCCLXXIII: golden ordered D4 torsor.

MMCCCLXXII proves that the 108 unique golden-selector failures are

    K2,2_edges x B27.

The draft flatness audit, however, counts ordered quadrangle cycles, not
unoriented quadrangle supports.  This verifier proves the ordered carrier:

    K2,2_edges x B27 x D4_orientations = 4 * 27 * 8 = 864.

For each product coordinate (active pair, bridge line), the forced quadrangle
has a canonical cyclic role order

    (anchor, endpoint_left, bridge, endpoint_right).

The eight ordered failures over that support are exactly the four rotations of
this cycle and the four rotations of its reverse.  Thus the old "times eight"
factor is the dihedral orientation torsor of the square, not an unexplained
multiplicity.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_golden_failure_product_bijection import (  # noqa: E402
    endpoint_line_for_bridge,
    failure_product_records,
)
from analysis.w33_golden_selector_z20_cochain_lift import (  # noqa: E402
    canonical_cycle,
    load_selector_data,
)
from scripts.w33_golden_selector_draft_audit import (  # noqa: E402
    _common_point,
    _line_adjacency,
)


OUTPUT_PATH = ROOT / "PART_MMCCCLXXIII_GOLDEN_ORDERED_D4_TORSOR_results.json"

Q = 3

Cycle = tuple[int, int, int, int]
Pair = tuple[int, int]


def rotate(cycle: Cycle, shift: int) -> Cycle:
    return cycle[shift:] + cycle[:shift]


def d4_orientations(base_cycle: Cycle) -> dict[str, Cycle]:
    roles = ("anchor", "left_endpoint", "bridge", "right_endpoint")
    orientations: dict[str, Cycle] = {}
    for shift, role in enumerate(roles):
        orientations[f"forward_start_{role}"] = rotate(base_cycle, shift)

    reversed_cycle = tuple(reversed(base_cycle))  # type: ignore[assignment]
    reversed_roles = tuple(reversed(roles))
    for shift, role in enumerate(reversed_roles):
        orientations[f"reverse_start_{role}"] = rotate(reversed_cycle, shift)
    return orientations


def ordered_failure_cycles() -> list[tuple[Cycle, tuple[int, int, int, int]]]:
    lines, sigma = load_selector_data()
    adjacency = _line_adjacency(lines)
    ordered: list[tuple[Cycle, tuple[int, int, int, int]]] = []

    for line0, neighbours0 in enumerate(adjacency):
        for line1, is_adjacent01 in enumerate(neighbours0):
            if not is_adjacent01:
                continue
            point01 = _common_point(lines[line0], lines[line1])

            for line2, is_adjacent12 in enumerate(adjacency[line1]):
                if line2 == line0 or not is_adjacent12:
                    continue
                point12 = _common_point(lines[line1], lines[line2])
                if point12 == point01:
                    continue

                for line3, is_adjacent23 in enumerate(adjacency[line2]):
                    if line3 == line1 or not is_adjacent23 or not adjacency[line3][line0]:
                        continue
                    point23 = _common_point(lines[line2], lines[line3])
                    point30 = _common_point(lines[line3], lines[line0])
                    points = (point01, point12, point23, point30)
                    if len(set(points)) < 4:
                        continue

                    holonomy = (
                        sigma[(point01, line0, line1)]
                        * sigma[(point12, line1, line2)]
                        * sigma[(point23, line2, line3)]
                        * sigma[(point30, line3, line0)]
                    )
                    if holonomy == -1:
                        ordered.append(((line0, line1, line2, line3), points))

    return ordered


def expected_product_orientations() -> dict[tuple[Pair, int, str], Cycle]:
    records = failure_product_records()
    geometry = records["geometry"]
    anchor_line = geometry["anchor_line"]
    expected: dict[tuple[Pair, int, str], Cycle] = {}

    for pair, bridge_line in sorted(records["expected_keys"]):
        left_line = endpoint_line_for_bridge(geometry, pair[0], bridge_line)
        right_line = endpoint_line_for_bridge(geometry, pair[1], bridge_line)
        base_cycle = (anchor_line, left_line, bridge_line, right_line)
        for orientation_label, cycle in d4_orientations(base_cycle).items():
            expected[(pair, bridge_line, orientation_label)] = cycle
    return expected


def golden_ordered_d4_torsor_packet() -> dict[str, Any]:
    ordered = ordered_failure_cycles()
    actual_cycles = [cycle for cycle, _points in ordered]
    actual_cycle_set = set(actual_cycles)
    canonical_profile = Counter(canonical_cycle(cycle) for cycle in actual_cycles)
    expected = expected_product_orientations()
    expected_cycle_set = set(expected.values())

    orientation_profile: Counter[str] = Counter()
    pair_profile: Counter[Pair] = Counter()
    bridge_profile: Counter[int] = Counter()
    support_orientation_profile: Counter[tuple[Pair, int]] = Counter()
    collisions: Counter[Cycle] = Counter(expected.values())

    for pair, bridge_line, orientation_label in expected:
        orientation_profile[orientation_label] += 1
        pair_profile[pair] += 1
        bridge_profile[bridge_line] += 1
        support_orientation_profile[(pair, bridge_line)] += 1

    sample_records = [
        {
            "pair": list(pair),
            "bridge_line": bridge_line,
            "orientation": orientation_label,
            "cycle": list(cycle),
            "canonical_cycle": list(canonical_cycle(cycle)),
        }
        for (pair, bridge_line, orientation_label), cycle in list(sorted(expected.items()))[:12]
    ]

    checks = {
        "ordered_failure_count_is_864": len(actual_cycles) == 864,
        "unique_support_count_is_108": len(canonical_profile) == 108,
        "each_unique_support_has_8_orderings": Counter(canonical_profile.values()) == {8: 108},
        "expected_product_orientation_count_is_864": len(expected) == 4 * 27 * 8 == 864,
        "expected_cycles_are_distinct": Counter(collisions.values()) == {1: 864},
        "expected_cycles_equal_actual_ordered_failures": expected_cycle_set == actual_cycle_set,
        "orientation_labels_each_have_108_cycles": Counter(orientation_profile.values()) == {108: 8},
        "each_active_pair_has_216_ordered_cycles": Counter(pair_profile.values()) == {27 * 8: 4},
        "each_bridge_has_32_ordered_cycles": Counter(bridge_profile.values()) == {4 * 8: 27},
        "each_pair_bridge_support_has_d4_orbit": Counter(support_orientation_profile.values()) == {8: 108},
        "ordered_count_is_2q_times_unique": len(actual_cycles) == 2**Q * len(canonical_profile),
        "ordered_count_is_k22_b27_d4": len(actual_cycles) == 4 * 27 * 8,
    }

    return {
        "part": "MMCCCLXXIII",
        "theorem": "Golden ordered D4 torsor",
        "input_packets": [
            "MMCCCLXXII golden failure product bijection",
            "MCCXLVI golden selector Z20 cochain lift",
        ],
        "ordered_failure_count": len(actual_cycles),
        "unique_support_count": len(canonical_profile),
        "orientation_labels": sorted(orientation_profile),
        "orientation_count_profile": {key: int(orientation_profile[key]) for key in sorted(orientation_profile)},
        "pair_count_profile": {f"{pair[0]}-{pair[1]}": int(value) for pair, value in sorted(pair_profile.items())},
        "bridge_count_profile": {str(key): int(value) for key, value in sorted(bridge_profile.items())},
        "support_orientation_profile": {str(key): int(value) for key, value in sorted(Counter(support_orientation_profile.values()).items())},
        "product_identity": {
            "unique": "K2,2_edges * B27 = 4*27 = 108",
            "ordered": "K2,2_edges * B27 * D4 = 4*27*8 = 864",
            "d4_roles": "four rotations of (anchor,left,bridge,right) and four rotations of the reverse cycle",
        },
        "sample_records": sample_records,
        "reading": (
            "The ordered obstruction shell is the dihedral lift of the product "
            "carrier. The support-level product K2,2 x B27 gives 108 failed "
            "quadrangles. The flatness loop counts every square in its four "
            "cyclic rotations and two directions, giving the D4 orientation "
            "torsor and the full 864 ordered failures."
        ),
        "claim_boundary": (
            "This proves the ordered carrier inside the draft golden selector. "
            "It still does not identify these ordered product coordinates with "
            "signed AGL(2,3) candidates or O^-(6,2)/A5 cosets."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = golden_ordered_d4_torsor_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MMCCCLXXIII: Golden Ordered D4 Torsor ===")
    print("ordered failures:", packet["ordered_failure_count"])
    print("unique supports:", packet["unique_support_count"])
    print("product:", packet["product_identity"])
    print("verified:", packet["n_verified"], "/", len(packet["checks"]))


if __name__ == "__main__":
    main()
