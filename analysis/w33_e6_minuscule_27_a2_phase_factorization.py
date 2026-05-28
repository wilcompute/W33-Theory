"""Part MCCCXC: E6 minuscule 27 x A2 phase factorization.

MCCCLXXXIX verified the exact root branching

    E8 -> E6 x A2,     240 = 72 + 6 + 81 + 81.

This verifier resolves each 81-root matter sector.  Project an 81 sector to
the E6 zero-coordinate subspace by deleting the chosen A2 coordinate.  The 81
roots collapse to 27 distinct E6 weights, each with exactly three A2 phases:

    81 = 27_E6 weights x 3_A2 phases.

The 27 projected weights are checked as the E6 minuscule geometry: norm 4/3,
rank 6, zero barycenter, tight Gram G^2 = 6G, Weyl reflection closure under the
72 E6 roots, and the Schlaefli graph srg(27,16,10,8) from the inner product
1/3 relation.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_e8_e6_a2_coordinate_decomposition import (  # noqa: E402
    block_pair,
    sectorize_by_coordinate,
)
from analysis.w33_tetracode_e8_root_system_bridge import (  # noqa: E402
    Vector,
    counter_to_json,
    inner,
    rational_rank,
    scale,
    subtract,
)


OUTPUT_PATH = ROOT / "PART_MCCCXC_E6_MINUSCULE_27_A2_PHASE_FACTORIZATION_results.json"


def project_to_e6(root: Vector, coordinate: int) -> Vector:
    projected = list(root)
    projected[2 * coordinate] = Fraction(0)
    projected[2 * coordinate + 1] = Fraction(0)
    return tuple(projected)


def graph_parameters(weights: list[Vector], adjacency_inner_product: Fraction) -> dict[str, Any]:
    adjacency = {
        idx: {
            jdx
            for jdx, other in enumerate(weights)
            if idx != jdx and inner(weight, other) == adjacency_inner_product
        }
        for idx, weight in enumerate(weights)
    }

    adjacent_common_neighbors: Counter[int] = Counter()
    nonadjacent_common_neighbors: Counter[int] = Counter()
    for idx in range(len(weights)):
        for jdx in range(idx + 1, len(weights)):
            common = len(adjacency[idx] & adjacency[jdx])
            if jdx in adjacency[idx]:
                adjacent_common_neighbors[common] += 1
            else:
                nonadjacent_common_neighbors[common] += 1

    return {
        "vertices": len(weights),
        "degree_profile": counter_to_json(Counter(len(neighbors) for neighbors in adjacency.values())),
        "edge_count": sum(len(neighbors) for neighbors in adjacency.values()) // 2,
        "adjacent_common_neighbor_profile": counter_to_json(adjacent_common_neighbors),
        "nonadjacent_common_neighbor_profile": counter_to_json(nonadjacent_common_neighbors),
    }


def gram_matrix(weights: list[Vector]) -> list[list[Fraction]]:
    return [[inner(left, right) for right in weights] for left in weights]


def gram_square_residual(gram: list[list[Fraction]], scalar: Fraction) -> Fraction:
    max_residual = Fraction(0)
    size = len(gram)
    for row in range(size):
        for col in range(size):
            value = sum(gram[row][idx] * gram[idx][col] for idx in range(size)) - scalar * gram[row][col]
            max_residual = max(max_residual, abs(value))
    return max_residual


def weight_sum_is_zero(weights: list[Vector]) -> bool:
    return all(sum(weight[coordinate] for weight in weights) == 0 for coordinate in range(8))


def reflection_closure_failures(weights: list[Vector], e6_roots: list[Vector]) -> int:
    weight_set = set(weights)
    failures = 0
    for weight in weights:
        for root in e6_roots:
            reflected = subtract(weight, scale(inner(weight, root), root))
            if reflected not in weight_set:
                failures += 1
    return failures


def matter_sector_report(coordinate: int, sector_key: str) -> dict[str, Any]:
    sectors = sectorize_by_coordinate(coordinate)
    matter_roots = sectors[sector_key]
    e6_roots = sectors["E6_zero_coordinate_roots"]

    phase_by_weight: dict[Vector, list[tuple[Fraction, Fraction]]] = defaultdict(list)
    for root in matter_roots:
        phase_by_weight[project_to_e6(root, coordinate)].append(block_pair(root, coordinate))

    weights = sorted(phase_by_weight)
    gram = gram_matrix(weights)
    norm_profile = Counter(inner(weight, weight) for weight in weights)
    local_profile = Counter(tuple(sorted(Counter(inner(weight, other) for other in weights).items())) for weight in weights)
    root_pairing_profile = Counter(inner(weight, root) for weight in weights for root in e6_roots)

    schlaefli = graph_parameters(weights, Fraction(1, 3))
    complement = graph_parameters(weights, Fraction(-2, 3))
    failures = reflection_closure_failures(weights, e6_roots)
    phase_profile = Counter(tuple(sorted(phases)) for phases in phase_by_weight.values())

    checks = {
        "sector_has_81_roots": len(matter_roots) == 81,
        "projection_has_27_weights": len(weights) == 27,
        "each_weight_has_three_a2_phases": Counter(len(phases) for phases in phase_by_weight.values()) == {3: 27},
        "projected_weight_rank_is_6": rational_rank(weights) == 6,
        "projected_weight_norm_profile_is_4_over_3": norm_profile == {Fraction(4, 3): 27},
        "projected_weights_have_zero_barycenter": weight_sum_is_zero(weights),
        "projected_weight_gram_is_6_scaled_projector": gram_square_residual(gram, Fraction(6)) == 0,
        "e6_root_reflections_preserve_27_weights": failures == 0,
        "e6_root_pairing_profile_is_minuscule": root_pairing_profile
        == {Fraction(-1): 432, Fraction(0): 1080, Fraction(1): 432},
        "schlaefli_graph_is_srg_27_16_10_8": schlaefli
        == {
            "vertices": 27,
            "degree_profile": {"16": 27},
            "edge_count": 216,
            "adjacent_common_neighbor_profile": {"10": 216},
            "nonadjacent_common_neighbor_profile": {"8": 135},
        },
        "complement_graph_is_srg_27_10_1_5": complement
        == {
            "vertices": 27,
            "degree_profile": {"10": 27},
            "edge_count": 135,
            "adjacent_common_neighbor_profile": {"1": 135},
            "nonadjacent_common_neighbor_profile": {"5": 216},
        },
    }

    return {
        "coordinate": coordinate,
        "sector": sector_key,
        "matter_root_count": len(matter_roots),
        "projected_weight_count": len(weights),
        "multiplicity_profile": counter_to_json(Counter(len(phases) for phases in phase_by_weight.values())),
        "a2_phase_set_profile": counter_to_json(phase_profile),
        "projected_weight_rank": rational_rank(weights),
        "projected_weight_norm_profile": counter_to_json(norm_profile),
        "projected_weight_local_profile": counter_to_json(local_profile),
        "projected_weight_sum_zero": weight_sum_is_zero(weights),
        "projected_weight_gram_square_minus_6_gram_max_residual": str(gram_square_residual(gram, Fraction(6))),
        "e6_reflection_closure_failures": failures,
        "e6_root_pairing_profile": counter_to_json(root_pairing_profile),
        "schlaefli_graph": schlaefli,
        "complement_graph": complement,
        "sample_projected_weights": [[str(entry) for entry in weight] for weight in weights[:6]],
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def e6_minuscule_27_a2_phase_packet() -> dict[str, Any]:
    reports = [
        matter_sector_report(coordinate, sector_key)
        for coordinate in range(4)
        for sector_key in ("matter_81_coset_1", "matter_81_coset_2")
    ]

    checks = {
        "all_eight_matter_sectors_verify_11_checks": all(report["n_verified"] == 11 for report in reports),
        "all_eight_matter_sectors_are_27_times_3": all(
            report["projected_weight_count"] == 27 and report["multiplicity_profile"] == {"3": 27}
            for report in reports
        ),
        "all_eight_projected_weight_sets_have_rank_6": all(
            report["projected_weight_rank"] == 6 for report in reports
        ),
        "all_eight_schlaefli_graphs_are_srg_27_16_10_8": all(
            report["schlaefli_graph"]["degree_profile"] == {"16": 27}
            and report["schlaefli_graph"]["adjacent_common_neighbor_profile"] == {"10": 216}
            and report["schlaefli_graph"]["nonadjacent_common_neighbor_profile"] == {"8": 135}
            for report in reports
        ),
        "all_eight_weight_sets_are_e6_reflection_closed": all(
            report["e6_reflection_closure_failures"] == 0 for report in reports
        ),
    }

    return {
        "part": "MCCCXC",
        "theorem": "E6 minuscule 27 x A2 phase factorization",
        "input_bridge": "MCCCLXXXIX E8 -> E6 x A2 coordinate decomposition",
        "factorization_identity": "81 = 27_E6 * 3_A2",
        "matter_sector_reports": reports,
        "claim_boundary": (
            "finite representation-geometry theorem; it identifies the exact E6 "
            "minuscule weight and A2 phase factorization inside the W33-derived "
            "E8 roots, without asserting a continuum particle spectrum by itself"
        ),
        "reading": (
            "Each 81-root matter sector in the exact W33-derived E8 -> E6 x A2 "
            "split factors as 27 E6 projected weights times three A2 phase lifts. "
            "The 27 weights are rank 6, norm 4/3, have zero barycenter, satisfy "
            "G^2=6G, are closed under the E6 root reflections, and carry the "
            "Schlaefli graph srg(27,16,10,8). This upgrades the matter-sector "
            "count into the finite E6 minuscule representation geometry."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = e6_minuscule_27_a2_phase_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCCXC: E6 Minuscule 27 x A2 Phase Factorization ===")
    print("identity:", packet["factorization_identity"])
    first = packet["matter_sector_reports"][0]
    print("sector 0 projected weights:", first["projected_weight_count"])
    print("sector 0 Schlaefli:", first["schlaefli_graph"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])} global checks")
    print("per-sector checks:", [report["n_verified"] for report in packet["matter_sector_reports"]])


if __name__ == "__main__":
    main()
