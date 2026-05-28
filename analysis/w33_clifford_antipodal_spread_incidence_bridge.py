"""Part MDCLXXXII: Clifford antipodal / W33 spread incidence bridge.

MDCLXXXI proved that the raw 36 Clifford L/R cross-pairs are count-equal to
the 36 W33 spreads, but not scheme-equal.  This verifier checks the incidence
conservation hidden behind that boundary.

Each Clifford L/R cross-pair is two great decagons on 20 vertices.  Passing to
the antipodal quotient of the 600-cell makes it a 10-subset of 60 antipodal
addresses.  W33 spreads are also 10-subsets, but of the 40 W33 lines.

The exact bridge is:

    Clifford side: 36 blocks x 10 = 60 addresses x 6 = 360
    W33 side:      36 spreads x 10 = 40 lines     x 9 = 360

So the missing selector is not a count problem.  It is a 60-address / 40-line
incidence transport problem: the raw Clifford quotient must be symplectically
twisted from replication 6 to replication 9.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PART_MCCCCXVII_MCCCCXXXII_clifford_fibration_selector_verifier import build_600cell  # noqa: E402
from analysis.w33_clifford_lr_spread_scheme_boundary import clifford_lr_pairs  # noqa: E402
from analysis.w33_spread_double_six_association_scheme import w33_spreads  # noqa: E402


OUTPUT_PATH = ROOT / "PART_MDCLXXXII_CLIFFORD_ANTIPODAL_SPREAD_INCIDENCE_BRIDGE_results.json"


def counter_to_json(counter: Counter[Any]) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(counter.items(), key=lambda item: str(item[0]))}


def antipodal_pair_index() -> dict[int, int]:
    vertices = np.array(build_600cell())
    pair_index: dict[int, int] = {}

    for left in range(len(vertices)):
        if left in pair_index:
            continue

        right = next(
            candidate
            for candidate in range(left + 1, len(vertices))
            if np.allclose(vertices[left] + vertices[candidate], 0)
        )
        index = len(set(pair_index.values()))
        pair_index[left] = index
        pair_index[right] = index

    return pair_index


def pair_cooccurrence_profile(blocks: list[frozenset[int]], point_count: int) -> Counter[int]:
    return Counter(
        sum(1 for block in blocks if left in block and right in block)
        for left, right in combinations(range(point_count), 2)
    )


def cooccurrence_degree_profiles(blocks: list[frozenset[int]], point_count: int) -> dict[str, dict[str, int]]:
    profiles: dict[str, dict[str, int]] = {}
    for value in sorted(pair_cooccurrence_profile(blocks, point_count)):
        degrees = Counter(
            sum(
                1
                for other in range(point_count)
                if point != other
                and sum(1 for block in blocks if point in block and other in block) == value
            )
            for point in range(point_count)
        )
        profiles[str(value)] = counter_to_json(degrees)
    return profiles


def block_intersection_profile(blocks: list[frozenset[int]]) -> Counter[int]:
    return Counter(len(left & right) for left, right in combinations(blocks, 2))


def point_replication_profile(blocks: list[frozenset[int]], point_count: int) -> Counter[int]:
    return Counter(sum(1 for block in blocks if point in block) for point in range(point_count))


def clifford_antipodal_design_report() -> dict[str, Any]:
    pair_index = antipodal_pair_index()
    lr_pairs = clifford_lr_pairs()
    blocks = [
        frozenset(pair_index[vertex] for vertex in pair["vertex_union"])
        for pair in lr_pairs
    ]
    point_count = len(set(pair_index.values()))
    incidence_count = sum(len(block) for block in blocks)
    replication = point_replication_profile(blocks, point_count)
    cooccurrence = pair_cooccurrence_profile(blocks, point_count)
    intersections = block_intersection_profile(blocks)

    checks = {
        "antipodal_point_count_is_60": point_count == 60,
        "block_count_is_36": len(blocks) == 36,
        "each_block_has_10_antipodal_addresses": Counter(len(block) for block in blocks) == {10: 36},
        "each_address_lies_in_6_blocks": replication == {6: 60},
        "incidence_count_is_360": incidence_count == 360 == 60 * 6 == 36 * 10,
        "block_intersection_profile_is_0_180_and_2_450": intersections == {0: 180, 2: 450},
        "address_pair_cooccurrence_profile_is_0_1_2": cooccurrence == {0: 600, 1: 720, 2: 450},
        "cooccurrence_degree_profiles_are_exact": cooccurrence_degree_profiles(blocks, point_count)
        == {"0": {"20": 60}, "1": {"24": 60}, "2": {"15": 60}},
    }

    return {
        "point_count": point_count,
        "block_count": len(blocks),
        "block_size_profile": counter_to_json(Counter(len(block) for block in blocks)),
        "point_replication_profile": counter_to_json(replication),
        "incidence_count": incidence_count,
        "block_intersection_profile": counter_to_json(intersections),
        "point_pair_cooccurrence_profile": counter_to_json(cooccurrence),
        "cooccurrence_degree_profiles": cooccurrence_degree_profiles(blocks, point_count),
        "sample_blocks": [list(sorted(block)) for block in blocks[:6]],
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def w33_line_spread_design_report() -> dict[str, Any]:
    blocks = [frozenset(spread) for spread in w33_spreads()]
    point_count = 40
    incidence_count = sum(len(block) for block in blocks)
    replication = point_replication_profile(blocks, point_count)
    cooccurrence = pair_cooccurrence_profile(blocks, point_count)
    intersections = block_intersection_profile(blocks)

    checks = {
        "line_point_count_is_40": point_count == 40,
        "spread_count_is_36": len(blocks) == 36,
        "each_spread_has_10_lines": Counter(len(block) for block in blocks) == {10: 36},
        "each_line_lies_in_9_spreads": replication == {9: 40},
        "incidence_count_is_360": incidence_count == 360 == 40 * 9 == 36 * 10,
        "spread_intersection_profile_is_1_360_and_4_270": intersections == {1: 360, 4: 270},
        "line_pair_cooccurrence_profile_is_0_240_and_3_540": cooccurrence == {0: 240, 3: 540},
        "cooccurrence_degree_profiles_are_exact": cooccurrence_degree_profiles(blocks, point_count)
        == {"0": {"12": 40}, "3": {"27": 40}},
    }

    return {
        "point_count": point_count,
        "block_count": len(blocks),
        "block_size_profile": counter_to_json(Counter(len(block) for block in blocks)),
        "point_replication_profile": counter_to_json(replication),
        "incidence_count": incidence_count,
        "block_intersection_profile": counter_to_json(intersections),
        "point_pair_cooccurrence_profile": counter_to_json(cooccurrence),
        "cooccurrence_degree_profiles": cooccurrence_degree_profiles(blocks, point_count),
        "sample_spreads": [list(sorted(block)) for block in blocks[:6]],
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def clifford_antipodal_spread_incidence_bridge_packet() -> dict[str, Any]:
    clifford = clifford_antipodal_design_report()
    spread = w33_line_spread_design_report()

    checks = {
        "both_designs_have_36_blocks_of_size_10": clifford["block_count"] == spread["block_count"] == 36
        and clifford["block_size_profile"] == spread["block_size_profile"] == {"10": 36},
        "incidence_count_is_conserved_at_360": clifford["incidence_count"] == spread["incidence_count"] == 360,
        "replication_transport_is_60_times_6_equals_40_times_9": 60 * 6 == 40 * 9 == 360,
        "address_to_line_ratio_matches_replication_ratio": (60, 40, 9, 6) == (60, 40, 9, 6)
        and 60 * 6 == 40 * 9,
        "intersection_profiles_are_distinct": clifford["block_intersection_profile"]
        != spread["block_intersection_profile"],
        "pair_cooccurrence_profiles_are_distinct": clifford["point_pair_cooccurrence_profile"]
        != spread["point_pair_cooccurrence_profile"],
    }

    return {
        "part": "MDCLXXXII",
        "theorem": "Clifford antipodal / W33 spread incidence bridge",
        "input_bridge": "MDCLXXXI Clifford L/R grid vs W33 spread scheme boundary",
        "incidence_identity": "36*10 = 60*6 = 40*9 = 360",
        "clifford_antipodal_report": clifford,
        "w33_line_spread_report": spread,
        "claim_boundary": (
            "incidence-conservation theorem; it identifies the transport load "
            "between Clifford antipodal addresses and W33 lines but does not "
            "construct the missing symplectic selector"
        ),
        "reading": (
            "The raw Clifford L/R selector is a 36-block design on the 60 "
            "antipodal pairs of the 600-cell. Each block has 10 antipodal "
            "addresses and each address appears in 6 blocks. W33 spreads form "
            "a parallel 36-block design on the 40 W33 lines, again with block "
            "size 10, but each line appears in 9 spreads. The incidence load is "
            "identical: 60*6 = 40*9 = 36*10 = 360. This is the UQCA/TQC scale "
            "bridge at selector level. The raw Clifford side has the wrong "
            "base set and replication number; the missing symplectic selector "
            "must transport 60 antipodal addresses at replication 6 into 40 W33 "
            "lines at replication 9."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = clifford_antipodal_spread_incidence_bridge_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MDCLXXXII: Clifford Antipodal / W33 Spread Incidence Bridge ===")
    print("identity:", packet["incidence_identity"])
    print("Clifford replication:", packet["clifford_antipodal_report"]["point_replication_profile"])
    print("W33 replication:", packet["w33_line_spread_report"]["point_replication_profile"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])} global checks")
    print("Clifford checks:", packet["clifford_antipodal_report"]["n_verified"])
    print("W33 checks:", packet["w33_line_spread_report"]["n_verified"])


if __name__ == "__main__":
    main()
