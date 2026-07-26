#!/usr/bin/env python3
"""Pass 1058: a second point-versus-dual experimental discriminator."""
from __future__ import annotations

import json
from pathlib import Path

from sympy.combinatorics import Permutation, PermutationGroup

from w33_pass1054_1059_core import build_w33_bundle, cycle_partition, permutation_images

POINT_GENERATOR_IMAGES = [
    [0, 28, 30, 29, 32, 31, 33, 18, 16, 17, 8, 7, 9, 15, 13, 14, 11, 10, 12, 35, 34, 36, 5, 6, 4, 21, 20, 19, 38, 39, 37, 22, 24, 23, 25, 26, 27, 1, 3, 2],
    [0, 8, 9, 7, 32, 33, 31, 18, 16, 17, 28, 29, 30, 23, 24, 22, 36, 34, 35, 19, 20, 21, 14, 13, 15, 37, 39, 38, 27, 26, 25, 4, 6, 5, 2, 3, 1, 12, 10, 11],
]
LINE_GENERATOR_IMAGES = [
    [6, 38, 30, 19, 5, 0, 4, 21, 37, 29, 28, 39, 20, 36, 17, 25, 3, 10, 8, 31, 23, 15, 26, 34, 18, 7, 2, 11, 14, 33, 22, 16, 27, 35, 12, 9, 1, 24, 13, 32],
    [6, 2, 11, 7, 4, 5, 0, 12, 9, 1, 8, 10, 3, 17, 25, 36, 13, 24, 32, 21, 29, 37, 26, 34, 18, 22, 33, 14, 30, 38, 19, 35, 16, 27, 31, 15, 23, 39, 20, 28],
]


def commutator(left: Permutation, right: Permutation) -> Permutation:
    return left**-1 * right**-1 * left * right


def moved_points(permutation: Permutation, degree: int = 40) -> int:
    return sum(permutation(index) != index for index in range(degree))


def analyze(subgroup: PermutationGroup, generator_images: list[list[int]]) -> dict[str, object]:
    generators = [Permutation(images) for images in generator_images]
    generated = PermutationGroup(generators)
    if generated.order() != subgroup.order() or not generated.is_subgroup(subgroup):
        raise AssertionError("stored generator pair does not generate the intended stabilizer")
    elements = list(subgroup.generate_schreier_sims())
    order_three = [element for element in elements if element.order() == 3]
    commuting = [element for element in order_three if all(element * generator == generator * element for generator in generators)]
    score_rows = []
    for candidate in order_three:
        mismatch_by_generator = [moved_points(commutator(candidate, generator)) for generator in generators]
        score_rows.append({
            "total_mismatches": sum(mismatch_by_generator),
            "mismatches_by_generator": mismatch_by_generator,
            "candidate_images": permutation_images(candidate, 40),
            "candidate_cycle_partition": list(cycle_partition(candidate, 40)),
        })
    score_rows.sort(key=lambda row: (row["total_mismatches"], row["mismatches_by_generator"], row["candidate_images"]))
    return {
        "order": int(subgroup.order()),
        "center_order": int(subgroup.center().order()),
        "generator_orders": [int(generator.order()) for generator in generators],
        "generator_images": generator_images,
        "order_three_candidates": len(order_three),
        "commuting_order_three_candidates": len(commuting),
        "commuting_candidates": [{"images": permutation_images(element, 40), "cycle_partition": list(cycle_partition(element, 40)), "fixed_points": cycle_partition(element, 40).count(1)} for element in sorted(commuting, key=lambda item: tuple(permutation_images(item, 40)))],
        "best_scores": score_rows[:5],
        "minimum_mismatch_score": score_rows[0]["total_mismatches"] if score_rows else None,
    }


def main() -> dict[str, object]:
    bundle = build_w33_bundle()
    point = analyze(bundle.point_stabilizer, POINT_GENERATOR_IMAGES)
    line = analyze(bundle.line_stabilizer, LINE_GENERATOR_IMAGES)
    checks = {
        "point_pair_generates_648": point["order"] == 648,
        "line_pair_generates_648": line["order"] == 648,
        "point_has_exactly_two_nonidentity_central_order3_elements": point["commuting_order_three_candidates"] == 2,
        "point_central_elements_have_13_fixed_and_nine_3cycles": all(item["fixed_points"] == 13 and item["cycle_partition"].count(3) == 9 for item in point["commuting_candidates"]),
        "dual_has_no_central_order3_element": line["commuting_order_three_candidates"] == 0,
        "dual_best_false_candidate_has_gap_27": line["minimum_mismatch_score"] == 27,
        "point_perfect_candidates_score_zero": point["minimum_mismatch_score"] == 0,
    }
    if not all(checks.values()):
        raise AssertionError([name for name, passed in checks.items() if not passed])
    return {
        "schema": "w33.pass1058.central_c3_discriminator.v1",
        "status": "PASS",
        "headline": "A two-generator commutator test separates the two order-648 sides. The Hessian point stabilizer has exactly two nontrivial central order-3 operations, each fixing 13 modes and cycling the other 27 in nine triples. The dual stabilizer has none; its closest order-3 impostor produces 27 mode mismatches.",
        "point_side": point,
        "dual_line_side": line,
        "protocol": {"preparation": "Calibrate the displayed two generator permutations a and b on the 40 modes.", "candidate": "Implement an order-3 operation c and perform permutation/process tomography.", "tests": ["compare c a with a c", "compare c b with b c"], "point_verdict": "exactly two nonidentity c pass both tests; cycle type 1^13 3^9", "dual_verdict": "no nonidentity order-3 c passes; minimum exact mismatch score is 27"},
        "check_count": len(checks),
        "checks": checks,
        "scope": "This is an exact finite design and noise-margin count, not a physical run. It is independent of the contextual-fraction discriminator and probes the selected local stabilizer class directly.",
    }


if __name__ == "__main__":
    result = main()
    output = Path(__file__).resolve().parents[1] / "data" / "w33_pass1058_central_c3_discriminator.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "headline": result["headline"], "point_commuting_C3": result["point_side"]["commuting_order_three_candidates"], "dual_commuting_C3": result["dual_line_side"]["commuting_order_three_candidates"], "dual_gap": result["dual_line_side"]["minimum_mismatch_score"], "check_count": result["check_count"]}, indent=2))
