#!/usr/bin/env python3
"""Pass 1028: primary obstruction syndrome and residual-carrier theorem.

This certificate consumes three already verified artifacts and proves a conservative
cross-track synthesis:

* subgroup restrictions realize all four presence/absence syndromes of the
  independent C2 chirality and C3 phase obstructions;
* four named probes form a rank-two decoder over F2;
* the 120-element intermediate carrier is the sign-quotiented, residual-C3
  carrier (40 x 3), whereas the 80-element carrier is the phase-quotiented,
  residual-C2 carrier (40 x 2);
* the 120-sheet golden selector therefore has the correct *carrier signature*
  for the residual ternary phase bundle, not for the binary chirality bundle;
* its 108/864 failure data are decorations on one sheet, not the obstruction
  cocycle itself; and the Pass-341 selector-sign Bockstein remains a distinct,
  local H2(C2) class that does not globalize.

No G-set isomorphism is claimed here.  That requires the separate degree-120
permutation-action diagnostic.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "w33_pass1028_primary_obstruction_syndrome.json"


def load(name: str) -> dict[str, Any]:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def rank_mod2(rows: list[list[int]]) -> int:
    matrix = [row[:] for row in rows]
    rank = 0
    col_count = len(matrix[0]) if matrix else 0
    for col in range(col_count):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][col] & 1), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for i in range(len(matrix)):
            if i != rank and (matrix[i][col] & 1):
                matrix[i] = [(a ^ b) for a, b in zip(matrix[i], matrix[rank])]
        rank += 1
    return rank


def main() -> None:
    primary = load("w33_pass1023_chirality_and_phase_halves.json")
    golden = load("w33_BREAKTHROUGH_363_golden_failure_single_phase_sheet.json")
    h2 = load("w33_pass341_selector_extension_cohomology.json")

    require(primary["status"] == "PASS", "Pass 1023 primary split is not certified")
    require(golden["summary"]["all_identities_hold"], "BT363 selector identities failed")
    require(h2["status"] == "PASS", "Pass 341 cohomology is not certified")

    rows = primary["subgroup_table"]
    syndrome_rows = []
    by_name: dict[str, dict[str, Any]] = {}
    for row in rows:
        syndrome = [int(not row["sign_section"]), int(not row["phase_section"])]
        record = {
            "name": row["name"],
            "order": row["order"],
            "syndrome": syndrome,
            "chirality_obstructed": bool(syndrome[0]),
            "phase_obstructed": bool(syndrome[1]),
            "full_section": row["full_section"],
        }
        syndrome_rows.append(record)
        by_name[row["name"]] = record

    realized = {tuple(row["syndrome"]) for row in syndrome_rows}
    multiplicities = Counter(tuple(row["syndrome"]) for row in syndrome_rows)

    probes = [
        by_name["Z(G) = C2"],
        by_name["Sylow 3"],
        by_name["Sylow 5"],
        by_name["whole group Sp(4,3)"],
    ]
    decoder_matrix = [row["syndrome"] for row in probes]

    roots = 240
    base = 40
    sign_quotient = roots // 2
    phase_quotient = roots // 3
    residual_phase_fibre = sign_quotient // base
    residual_sign_fibre = phase_quotient // base
    selector_sheets = golden["summary"]["sheet_count"]

    checks = {
        "all_four_primary_syndromes_are_realized": realized == {(0, 0), (1, 0), (0, 1), (1, 1)},
        "center_is_chirality_only_probe": by_name["Z(G) = C2"]["syndrome"] == [1, 0],
        "sylow3_is_phase_only_probe": by_name["Sylow 3"]["syndrome"] == [0, 1],
        "sylow5_is_clean_control": by_name["Sylow 5"]["syndrome"] == [0, 0],
        "whole_group_activates_both": by_name["whole group Sp(4,3)"]["syndrome"] == [1, 1],
        "decoder_has_rank_two_over_F2": rank_mod2(decoder_matrix) == 2,
        "full_section_is_boolean_and_of_primary_sections": all(
            row["full_section"] == (not record["chirality_obstructed"] and not record["phase_obstructed"])
            for row, record in zip(rows, syndrome_rows)
        ),
        "sign_quotient_is_120_with_residual_C3": sign_quotient == 120 and residual_phase_fibre == 3,
        "phase_quotient_is_80_with_residual_C2": phase_quotient == 80 and residual_sign_fibre == 2,
        "golden_selector_has_residual_C3_carrier_signature": selector_sheets == sign_quotient == base * 3,
        "golden_selector_does_not_have_residual_C2_carrier_size": selector_sheets != phase_quotient,
        "single_failure_is_one_sheet_decoration": golden["summary"]["selected_sheet_supports"] == 108,
        "ordered_failure_is_D4_decoration": golden["summary"]["ordered_failures"] == 108 * 8,
        "selector_sign_Bockstein_is_local_H2_not_global_H1": (
            h2["dimensions"]["H2_line_stabilizer"] == 2
            and "not globalizable" in h2["restriction_verdict"]
        ),
    }
    require(all(checks.values()), f"failed checks: {[k for k, v in checks.items() if not v]}")

    result = {
        "schema": "w33.pass1028.primary_obstruction_syndrome.python.v1",
        "status": "PASS",
        "headline": (
            "The C6 obstruction has a complete two-bit restriction decoder: the center isolates "
            "chirality, Sylow-3 isolates ternary phase, Sylow-5 is the clean control, and Sp(4,3) "
            "activates both.  The 120-element intermediate carrier is 40x3 after quotienting sign, "
            "so the 120-sheet golden selector has the correct residual-C3 phase signature, while "
            "binary chirality lives on the distinct 80=40x2 carrier."
        ),
        "syndrome_convention": {
            "coordinates": ["chirality_C2_obstructed", "phase_C3_obstructed"],
            "zero_means": "an equivariant section exists for that primary half",
            "one_means": "that primary half is obstructed",
        },
        "subgroup_syndromes": syndrome_rows,
        "syndrome_multiplicities": {
            f"{key[0]}{key[1]}": multiplicities[key] for key in sorted(multiplicities)
        },
        "minimal_decoder": {
            "probe_order": [row["name"] for row in probes],
            "matrix_over_F2": decoder_matrix,
            "rank": rank_mod2(decoder_matrix),
            "interpretation": [
                "Z(G)=C2 reads the chirality bit without phase contamination",
                "Sylow-3 reads the phase bit without chirality contamination",
                "Sylow-5 is a clean negative control",
                "Sp(4,3) is the both-obstructed positive control",
            ],
        },
        "residual_carrier_square": {
            "roots": roots,
            "base_points": base,
            "sign_quotient": {
                "total": sign_quotient,
                "formula": "240/C2 = 120 = 40*3",
                "remaining_fibre": "C3",
                "correct_target_type": "ternary phase carrier",
            },
            "phase_quotient": {
                "total": phase_quotient,
                "formula": "240/C3 = 80 = 40*2",
                "remaining_fibre": "C2",
                "correct_target_type": "binary chirality carrier",
            },
            "golden_selector": {
                "total": selector_sheets,
                "formula": "120 = 40 anchor lines * 3 phase sheets",
                "verdict": "carrier-signature match to residual C3 only; G-set identity remains unproved",
            },
        },
        "selector_layering": {
            "carrier": "120 selector sheets = 40*3",
            "failure_decoration": "one selected sheet carries 108 failed minimal-Z supports",
            "orientation_decoration": "864 = 108*8 adds the D4 ordering torsor",
            "missing_independent_controller": (
                "the binary C2 chirality coordinate is not encoded by the 3-sheet selector fibre; "
                "a full C6 device needs an independent sign controller"
            ),
        },
        "cohomology_firewall": {
            "global_primary_phase_target": "action-groupoid H1 with C3 coefficients",
            "local_selector_sign_class": "Pass341 H2(K,F2) Bockstein",
            "verdict": (
                "different coefficient prime, different cohomological degree, and non-globalizable; "
                "no identity claim is permitted without an explicit transgression"
            ),
        },
        "experimental_falsifier": {
            "claim_under_test": "a 120-sheet selector realizes the full C6 holonomy",
            "required_observations": [
                "a ternary 3-cycle among sheets over one anchor",
                "an independent binary sign inversion not generated by that 3-cycle",
                "commuting composition with six distinct CRT-labelled responses",
            ],
            "failure_mode": (
                "if only the ternary cycle is observed, the device realizes the residual C3 carrier, "
                "not the full C6 bundle"
            ),
        },
        "boundary": (
            "This proves syndrome independence and carrier-type compatibility from verified artifacts. "
            "It does not prove that the E8 antipodal-pair 120-set and golden-selector 120-set are "
            "conjugate permutation actions; that is a separate objectwise test."
        ),
        "check_count": len(checks),
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Pass1028 status=PASS checks={len(checks)} output={OUT}")


if __name__ == "__main__":
    main()
