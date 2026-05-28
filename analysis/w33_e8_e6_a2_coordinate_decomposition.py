"""Part MCCCLXXXIX: W33 tetracode E8 -> E6 x A2 coordinate split.

MCCCLXXXVIII built the exact 240-root E8 system from the W33-derived
tetracode.  The standard E8 -> E6 x A2 decomposition should now be visible
without representation-theory assumptions:

    240 = 72_E6 + 6_A2 + 81 + 81.

The four A2 coordinates are the four lines through the chosen W33 anchor point
from MCCCLXXXVII.  For each coordinate, this verifier splits the exact E8 roots
by that coordinate and checks:

    * the zero-coordinate roots form a rank-6, 72-root E6 subsystem;
    * the coordinate's local roots form a rank-2, 6-root A2 subsystem;
    * the two subsystems are orthogonal;
    * the remaining roots split as 81 + 81 conjugate matter sectors.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_tetracode_e8_root_system_bridge import (  # noqa: E402
    A2_COSET_ONE_MINIMA,
    Vector,
    counter_to_json,
    e8_roots_from_w33_tetracode,
    inner,
    rational_rank,
    reflection_closure_failure_count,
    scale,
)


OUTPUT_PATH = ROOT / "PART_MCCCLXXXIX_E8_E6_A2_COORDINATE_DECOMPOSITION_results.json"

E6_LOCAL_PROFILE = {
    Fraction(-2): 1,
    Fraction(-1): 20,
    Fraction(0): 30,
    Fraction(1): 20,
    Fraction(2): 1,
}


def block_pair(root: Vector, coordinate: int) -> tuple[Fraction, Fraction]:
    return (root[2 * coordinate], root[2 * coordinate + 1])


def sectorize_by_coordinate(coordinate: int) -> dict[str, list[Vector]]:
    roots = e8_roots_from_w33_tetracode()
    coset_one = set(A2_COSET_ONE_MINIMA)
    coset_two = {(-left, -right) for left, right in A2_COSET_ONE_MINIMA}
    sectors: dict[str, list[Vector]] = {
        "E6_zero_coordinate_roots": [],
        "A2_coordinate_roots": [],
        "matter_81_coset_1": [],
        "matter_81_coset_2": [],
    }

    for root, source in roots.items():
        pair = block_pair(root, coordinate)
        if source == f"A2_block_{coordinate}":
            sectors["A2_coordinate_roots"].append(root)
        elif pair == (0, 0):
            sectors["E6_zero_coordinate_roots"].append(root)
        elif pair in coset_one:
            sectors["matter_81_coset_1"].append(root)
        elif pair in coset_two:
            sectors["matter_81_coset_2"].append(root)
        else:
            raise AssertionError((coordinate, root, source, pair))

    return sectors


def root_local_profile(roots: list[Vector]) -> Counter[Fraction]:
    return Counter(inner(roots[0], other) for other in roots)


def unique_local_profile_count(roots: list[Vector]) -> int:
    return len(Counter(tuple(sorted(Counter(inner(root, other) for other in roots).items())) for root in roots))


def sector_report(coordinate: int) -> dict[str, Any]:
    sectors = sectorize_by_coordinate(coordinate)
    e6_roots = sectors["E6_zero_coordinate_roots"]
    a2_roots = sectors["A2_coordinate_roots"]
    matter_1 = sectors["matter_81_coset_1"]
    matter_2 = sectors["matter_81_coset_2"]
    e6_set = set(e6_roots)

    e6_norm_profile = Counter(inner(root, root) for root in e6_roots)
    a2_norm_profile = Counter(inner(root, root) for root in a2_roots)
    e6_reflection_failures = reflection_closure_failure_count(e6_roots, e6_set)
    a2_e6_orthogonality_max = max(abs(inner(a2, e6)) for a2 in a2_roots for e6 in e6_roots)
    matter_negation_matches = {scale(Fraction(-1), root) for root in matter_1} == set(matter_2)

    checks = {
        "sector_counts_are_72_6_81_81": {
            key: len(value) for key, value in sectors.items()
        }
        == {
            "E6_zero_coordinate_roots": 72,
            "A2_coordinate_roots": 6,
            "matter_81_coset_1": 81,
            "matter_81_coset_2": 81,
        },
        "e6_rank_is_6": rational_rank(e6_roots) == 6,
        "a2_rank_is_2": rational_rank(a2_roots) == 2,
        "e6_norm_profile_is_72_norm2": e6_norm_profile == {Fraction(2): 72},
        "a2_norm_profile_is_6_norm2": a2_norm_profile == {Fraction(2): 6},
        "e6_local_profile_matches_e6": root_local_profile(e6_roots) == E6_LOCAL_PROFILE
        and unique_local_profile_count(e6_roots) == 1,
        "e6_reflection_closure_holds": e6_reflection_failures == 0,
        "a2_is_orthogonal_to_e6": a2_e6_orthogonality_max == 0,
        "matter_sectors_are_negatives": matter_negation_matches,
        "matter_sectors_have_rank_8": rational_rank(matter_1) == 8 and rational_rank(matter_2) == 8,
    }

    return {
        "coordinate": coordinate,
        "sector_counts": {key: len(value) for key, value in sectors.items()},
        "sector_ranks": {key: rational_rank(value) for key, value in sectors.items()},
        "E6_zero_coordinate": {
            "norm_profile": counter_to_json(e6_norm_profile),
            "representative_local_profile": counter_to_json(root_local_profile(e6_roots)),
            "unique_local_profile_count": unique_local_profile_count(e6_roots),
            "reflection_closure_failures": e6_reflection_failures,
        },
        "A2_coordinate": {
            "norm_profile": counter_to_json(a2_norm_profile),
            "orthogonality_to_E6_max": str(a2_e6_orthogonality_max),
        },
        "matter": {
            "coset_1_count": len(matter_1),
            "coset_2_count": len(matter_2),
            "coset_1_rank": rational_rank(matter_1),
            "coset_2_rank": rational_rank(matter_2),
            "coset_2_is_negative_of_coset_1": matter_negation_matches,
        },
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def e8_e6_a2_coordinate_decomposition_packet() -> dict[str, Any]:
    reports = [sector_report(coordinate) for coordinate in range(4)]
    checks = {
        "all_four_coordinates_verify_10_checks": all(report["n_verified"] == 10 for report in reports),
        "all_four_coordinates_have_same_sector_counts": {
            tuple(sorted(report["sector_counts"].items())) for report in reports
        }
        == {
            (
                ("A2_coordinate_roots", 6),
                ("E6_zero_coordinate_roots", 72),
                ("matter_81_coset_1", 81),
                ("matter_81_coset_2", 81),
            )
        },
        "all_four_coordinates_have_e6_rank_6_a2_rank_2": all(
            report["sector_ranks"]["E6_zero_coordinate_roots"] == 6
            and report["sector_ranks"]["A2_coordinate_roots"] == 2
            for report in reports
        ),
        "all_four_coordinates_have_orthogonal_e6_a2": all(
            report["A2_coordinate"]["orthogonality_to_E6_max"] == "0" for report in reports
        ),
        "all_four_coordinates_have_conjugate_81_sectors": all(
            report["matter"]["coset_2_is_negative_of_coset_1"] is True for report in reports
        ),
    }

    return {
        "part": "MCCCLXXXIX",
        "theorem": "E8 -> E6 x A2 coordinate decomposition from W33 tetracode roots",
        "input_bridge": "MCCCLXXXVIII exact tetracode E8 root-system bridge",
        "coordinate_reading": (
            "The four A2 coordinates are the four W33 anchor-line coordinates used "
            "to read the affine tetracode. Choosing any one coordinate splits the "
            "exact E8 roots into E6 roots, A2 roots, and two conjugate 81-root "
            "matter sectors."
        ),
        "decomposition_identity": "240 = 72_E6 + 6_A2 + 81 + 81",
        "coordinate_reports": reports,
        "claim_boundary": (
            "finite root-system decomposition theorem; it verifies the E8 -> E6 x A2 "
            "branching at the root-set level and does not by itself choose a physical "
            "compactification or gauge-breaking dynamics"
        ),
        "reading": (
            "The exact E8 roots built from the W33 tetracode do not merely have the "
            "right total count. Each of the four W33 anchor-line coordinates gives "
            "the canonical E8 -> E6 x A2 split: 72 rank-6 E6 roots orthogonal to "
            "6 rank-2 A2 roots, plus two conjugate 81-root matter sectors. This "
            "turns the earlier symbolic 72+6+81+81 match into an exact coordinate "
            "decomposition."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = e8_e6_a2_coordinate_decomposition_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCCLXXXIX: E8 -> E6 x A2 Coordinate Decomposition ===")
    print("identity:", packet["decomposition_identity"])
    print("coordinate 0 sectors:", packet["coordinate_reports"][0]["sector_counts"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])} global checks")
    print("per-coordinate checks:", [report["n_verified"] for report in packet["coordinate_reports"]])


if __name__ == "__main__":
    main()
