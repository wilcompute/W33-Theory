"""Part MCCCXCVII: E6 240 Steiner trihedra / E8 count resonance.

MCCCXCVI reconstructed 120 finite Steiner trihedral pairs in each W33-derived
E6 matter chart.  Each pair contains two complementary trihedra.  This verifier
promotes the individual-trihedron layer:

    120 Steiner trihedral pairs -> 240 Steiner trihedra.

The count is the E8 root/kissing count and the W33 oriented-corner count.  The
claim is only a finite incidence theorem: it does not identify the trihedra with
continuum E8 roots.  It checks that the E6 cubic-surface layer has a 240-object
incidence carrier with exact tritangent, weight, and partner-pair profiles.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_e6_120_steiner_trihedral_pairs import (  # noqa: E402
    counter_to_json,
    steiner_trihedral_pairs,
    trihedra_partition_pairs,
)


OUTPUT_PATH = ROOT / "PART_MCCCXCVII_E6_240_STEINER_TRIHEDRA_E8_COUNT_results.json"


Trihedron = tuple[int, int, int]


def steiner_trihedra(coordinate: int, sector_key: str) -> dict[str, Any]:
    pair_data = steiner_trihedral_pairs(coordinate, sector_key)
    tritangents = [frozenset(tritangent) for tritangent in pair_data["tritangents"]]

    trihedron_covers: dict[Trihedron, frozenset[int]] = {}
    partner_pairs: list[tuple[Trihedron, Trihedron]] = []

    for witness in pair_data["witnesses"]:
        contained = witness["contained_tritangents"]
        local_tritangents = [tritangents[index] for index in contained]
        partitions = trihedra_partition_pairs(local_tritangents)
        if len(partitions) != 1:
            continue

        global_pair: list[Trihedron] = []
        for local_trihedron in partitions[0]:
            trihedron = tuple(sorted(contained[index] for index in local_trihedron))
            cover = frozenset().union(*(tritangents[index] for index in trihedron))
            trihedron_covers[trihedron] = cover
            global_pair.append(trihedron)

        partner_pairs.append(tuple(sorted(global_pair)))

    return {
        "coordinate": coordinate,
        "sector": sector_key,
        "tritangents": tritangents,
        "trihedron_covers": trihedron_covers,
        "partner_pairs": sorted(set(partner_pairs)),
    }


def trihedra_report(coordinate: int, sector_key: str) -> dict[str, Any]:
    data = steiner_trihedra(coordinate, sector_key)
    tritangents = data["tritangents"]
    trihedron_covers: dict[Trihedron, frozenset[int]] = data["trihedron_covers"]
    trihedra = sorted(trihedron_covers)
    partner_pairs = data["partner_pairs"]

    cover_groups: dict[frozenset[int], list[Trihedron]] = defaultdict(list)
    for trihedron, cover in trihedron_covers.items():
        cover_groups[cover].append(trihedron)

    cover_partner_pairs = {
        tuple(sorted(members))
        for members in cover_groups.values()
        if len(members) == 2
    }
    partner_participation = Counter(trihedron for pair in partner_pairs for trihedron in pair)
    tritangent_participation = Counter(tritangent for trihedron in trihedra for tritangent in trihedron)
    weight_participation = Counter(weight for cover in trihedron_covers.values() for weight in cover)
    tritangent_overlap_profile = Counter(
        len(set(left) & set(right)) for left, right in combinations(trihedra, 2)
    )
    weight_intersection_profile = Counter(
        len(trihedron_covers[left] & trihedron_covers[right])
        for left, right in combinations(trihedra, 2)
    )
    same_cover_tritangent_overlap = Counter(
        len(set(members[0]) & set(members[1]))
        for members in cover_groups.values()
        if len(members) == 2
    )
    disjoint_tritangent_cover_profile = Counter(
        len(frozenset().union(*(tritangents[index] for index in trihedron)))
        for trihedron in trihedra
    )

    checks = {
        "trihedron_count_is_240": len(trihedra) == 240,
        "each_trihedron_uses_three_tritangents": Counter(len(trihedron) for trihedron in trihedra)
        == {3: 240},
        "each_trihedron_covers_nine_weights": Counter(len(cover) for cover in trihedron_covers.values())
        == {9: 240},
        "each_trihedron_is_three_disjoint_tritangents": disjoint_tritangent_cover_profile == {9: 240},
        "trihedra_group_into_120_partner_pairs_by_cover": Counter(len(members) for members in cover_groups.values())
        == {2: 120},
        "partner_pairs_match_cover_groups": set(partner_pairs) == cover_partner_pairs,
        "each_trihedron_has_one_partner": partner_participation == {trihedron: 1 for trihedron in trihedra},
        "same_cover_partners_share_no_tritangents": same_cover_tritangent_overlap == {0: 120},
        "each_tritangent_lies_in_16_trihedra": tritangent_participation
        == {tritangent: 16 for tritangent in range(len(tritangents))},
        "each_weight_lies_in_80_trihedra": weight_participation == {weight: 80 for weight in range(27)},
        "trihedron_tritangent_overlap_profile_is_exact": tritangent_overlap_profile == {0: 23280, 1: 5400},
        "trihedron_weight_intersection_profile_is_exact": weight_intersection_profile
        == {0: 480, 2: 12960, 3: 8640, 5: 6480, 9: 120},
    }

    return {
        "coordinate": coordinate,
        "sector": sector_key,
        "trihedron_count": len(trihedra),
        "partner_pair_count": len(partner_pairs),
        "trihedron_size_profile": counter_to_json(Counter(len(trihedron) for trihedron in trihedra)),
        "trihedron_cover_size_profile": counter_to_json(Counter(len(cover) for cover in trihedron_covers.values())),
        "cover_group_size_profile": counter_to_json(Counter(len(members) for members in cover_groups.values())),
        "partner_participation_profile": counter_to_json(Counter(partner_participation.values())),
        "same_cover_tritangent_overlap_profile": counter_to_json(same_cover_tritangent_overlap),
        "tritangent_participation_profile": counter_to_json(Counter(tritangent_participation.values())),
        "weight_participation_profile": counter_to_json(Counter(weight_participation.values())),
        "trihedron_tritangent_overlap_profile": counter_to_json(tritangent_overlap_profile),
        "trihedron_weight_intersection_profile": counter_to_json(weight_intersection_profile),
        "sample_trihedra": [
            {
                "tritangents": list(trihedron),
                "cover_weights": list(sorted(trihedron_covers[trihedron])),
            }
            for trihedron in trihedra[:8]
        ],
        "sample_partner_pairs": [
            [list(left), list(right)]
            for left, right in partner_pairs[:6]
        ],
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def e6_240_steiner_trihedra_e8_count_packet() -> dict[str, Any]:
    reports = [
        trihedra_report(coordinate, sector_key)
        for coordinate in range(4)
        for sector_key in ("matter_81_coset_1", "matter_81_coset_2")
    ]

    checks = {
        "all_eight_reports_verify_12_checks": all(report["n_verified"] == 12 for report in reports),
        "all_eight_reports_have_240_trihedra": all(report["trihedron_count"] == 240 for report in reports),
        "all_eight_reports_have_120_partner_pairs": all(report["partner_pair_count"] == 120 for report in reports),
        "all_eight_reports_have_weight_participation_80": all(
            report["weight_participation_profile"] == {"80": 27} for report in reports
        ),
        "all_eight_reports_have_tritangent_participation_16": all(
            report["tritangent_participation_profile"] == {"16": 45} for report in reports
        ),
        "all_eight_reports_have_e8_root_count_resonance": all(
            report["trihedron_count"] == 240 for report in reports
        ),
    }

    return {
        "part": "MCCCXCVII",
        "theorem": "E6 240 Steiner trihedra / E8 count resonance",
        "input_bridge": "MCCCXCVI E6 120 Steiner trihedral pairs",
        "trihedron_identity": "120 Steiner trihedral pairs -> 240 individual Steiner trihedra",
        "e8_count_resonance": "240 = E8 root count = W33 oriented-corner count",
        "matter_sector_reports": reports,
        "claim_boundary": (
            "finite E6 cubic-surface incidence theorem and count resonance; it "
            "does not identify the finite trihedra with continuum E8 roots"
        ),
        "reading": (
            "Each W33-derived E6 matter chart contains 240 individual Steiner "
            "trihedra. They group into 120 partner pairs by common 9-weight cover, "
            "and each partner pair is exactly the trihedral pair reconstructed in "
            "MCCCXCVI. Every tritangent lies in 16 trihedra and every weight lies "
            "in 80. The object count is the E8 root count and the W33 oriented-corner "
            "count, giving a finite cubic-surface carrier for the 240-shell without "
            "collapsing the claim into a continuum E8 identification."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = e6_240_steiner_trihedra_e8_count_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCCXCVII: E6 240 Steiner Trihedra / E8 Count ===")
    print("identity:", packet["trihedron_identity"])
    print("count resonance:", packet["e8_count_resonance"])
    first = packet["matter_sector_reports"][0]
    print("sector 0 trihedra:", first["trihedron_count"])
    print("sector 0 partner pairs:", first["partner_pair_count"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])} global checks")
    print("per-sector checks:", [report["n_verified"] for report in packet["matter_sector_reports"]])


if __name__ == "__main__":
    main()
