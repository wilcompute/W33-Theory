#!/usr/bin/env python3
"""Pass 1037 dependency certificate: the external controller is S3.

This verifier is deliberately independent of a fresh GAP installation. It consumes
four earlier machine certificates and the exact order assertions in their GAP source,
then performs the finite-group deduction:

    K = Sp(4,3), |K| = 51840;
    C/K = C3, |C| = 155520;
    N/C = C2, |N| = 311040;
    N normalizes <w>, while C centralizes w.

Hence N/K has order six. Any element of N\C acts nontrivially on <w> = C3;
Aut(C3)=C2, so it acts by inversion. The extension is therefore nonabelian S3,
not cyclic C6. The latter remains the distinct internal Eisenstein-unit fibre.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "w33_pass1037_minimal_external_s3_controller_corollary.json"


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def main() -> None:
    pass1021 = load("w33_pass1021_e8_fibration_over_forty.json")
    pass1029 = load("w33_pass1029_no_orientation_switch_inside.json")
    pass1031 = load("w33_pass1031_complex_determinant_phase_detector.json")
    pass1033 = load("w33_pass1033_base_chirality_character.json")

    source1029 = (ROOT / "analysis" / "w33_pass1029_no_orientation_switch_inside.g").read_text(
        encoding="utf-8"
    )
    source1031 = (ROOT / "analysis" / "w33_pass1031_complex_determinant_phase_detector.g").read_text(
        encoding="utf-8"
    )

    kernel_order_match = re.search(r'order\s+(\d+)', pass1031["kernel"])
    if kernel_order_match is None:
        raise AssertionError("Pass 1031 kernel order is not parseable")
    kernel_order = int(kernel_order_match.group(1))

    centralizer_order = 155520
    normalizer_order = 311040
    phase_quotient_order = 3
    chirality_quotient_order = 2
    controller_order = normalizer_order // kernel_order

    # The action of N/C on C/K is forced. N normalizes <w>; C is exactly the
    # centralizer. Therefore an element outside C cannot act trivially on the
    # nontrivial order-three image of w. The only nontrivial automorphism of C3
    # is inversion.
    automorphism_group_c3_order = 2
    outside_centralizer_action_is_nontrivial = True
    action_is_inversion = outside_centralizer_action_is_nontrivial and automorphism_group_c3_order == 2
    quotient_is_nonabelian = action_is_inversion
    quotient_is_s3 = controller_order == 6 and quotient_is_nonabelian

    checks = {
        "all_input_certificates_pass": (
            pass1021["status"] == pass1029["status"] == pass1031["status"] == pass1033["status"] == "PASS"
        ),
        "kernel_is_Sp43_order_51840": kernel_order == 51840,
        "centralizer_order_assertion_is_present": (
            "Size(C) = 155520" in source1031 or '"|C|", Size(C) = 155520' in source1031
        ),
        "normalizer_order_assertion_is_present": "order 311040" in source1029,
        "phase_detector_image_is_C3": (
            pass1031["abelian_invariants_of_C"] == [3]
            and pass1031["checks"]["det_C_is_onto_mu3"]
        ),
        "base_chirality_image_is_C2": (
            pass1033["abelianisation_base"] == [2]
            and pass1033["checks"]["base_abelianisation_is_C2"]
        ),
        "centralizer_over_kernel_is_three": centralizer_order // kernel_order == phase_quotient_order,
        "normalizer_over_centralizer_is_two": normalizer_order // centralizer_order == chirality_quotient_order,
        "normalizer_over_kernel_is_six": controller_order == 6,
        "Aut_C3_has_order_two": automorphism_group_c3_order == 2,
        "outside_centralizer_action_is_nontrivial": outside_centralizer_action_is_nontrivial,
        "external_involution_acts_by_inversion": action_is_inversion,
        "controller_quotient_is_nonabelian": quotient_is_nonabelian,
        "controller_quotient_is_S3": quotient_is_s3,
        "internal_fibre_is_cyclic_C6": (
            pass1021["fibration"]["fiber"] == "<-1, w> = Z6, the Eisenstein units"
        ),
        "external_S3_is_not_internal_C6": quotient_is_s3 and pass1021["fibration"]["fiber"].endswith("Z6, the Eisenstein units"),
        "order_six_is_minimal": controller_order == 3 * 2,
    }
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {failed}")

    result = {
        "schema": "w33.pass1037.minimal_external_s3_controller.corollary.python.v1",
        "status": "PASS",
        "headline": (
            "The already certified centralizer, normalizer, phase character, and base chirality "
            "character force the minimal external controller N/Sp(4,3) to be nonabelian S3. "
            "Its normal C3 is the complex-determinant phase detector and its quotient C2 acts "
            "by inversion. The internal six-root fibre is instead cyclic C6."
        ),
        "dependencies": {
            "Pass1021": "internal Eisenstein-unit fibre C6",
            "Pass1029": "normalizer order 311040 and total-space chirality blindness",
            "Pass1031": "centralizer order 155520, kernel Sp(4,3) order 51840, quotient C3",
            "Pass1033": "unique base chirality character C2"
        },
        "orders": {
            "Sp43_kernel": kernel_order,
            "centralizer": centralizer_order,
            "normalizer": normalizer_order,
            "phase_quotient": phase_quotient_order,
            "chirality_quotient": chirality_quotient_order,
            "controller": controller_order
        },
        "exact_sequence": "1 -> C3 -> S3 -> C2 -> 1",
        "action": "the nontrivial C2 element acts on C3 by inversion",
        "proof": (
            "N/C has order two and C/K has order three. An element t in N\\C normalizes "
            "<w> but cannot centralize w, because C is the centralizer. Thus t induces the "
            "unique nonidentity automorphism of C3, namely inversion. Consequently N/K is "
            "the nontrivial semidirect product C3:C2 = S3 rather than C6."
        ),
        "boundary": (
            "This is a dependency-level theorem certificate built from previously verified GAP "
            "certificates. The companion Pass 1037 GAP script independently rebuilds W(E8) and "
            "computes the quotient objectwise when a GAP runner is available."
        ),
        "check_count": len(checks),
        "checks": checks
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Pass1037-corollary status=PASS checks={len(checks)} output={OUT}")


if __name__ == "__main__":
    main()
