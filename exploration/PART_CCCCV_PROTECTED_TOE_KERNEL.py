#!/usr/bin/env python3
"""PART CCCCV -- Protected W33 / H1 / E8 TOE Kernel.

This is a synthesis certificate for the currently solved finite kernel:

    W33 photonic runtime
    -> H1 = Z^81 matter memory
    -> E8 Z3 operation gate
    -> W33 CSS [[240,81,3]] core
    -> Steane/Phi6 protection stack [[82320,81,>=81]]

The claim is deliberately bounded.  This proves an executable protected
information architecture inside the repository; it is not an empirical final
theory of all measured physics.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

Q = 3
V = 40
K = 12
E = 240
H1 = Q**4
PHI6 = Q * Q - Q + 1

PHOTONIC = ROOT / "PART_CCCXCVI_photonic_life_runtime_architecture_results.json"
CSS_CORE = ROOT / "PART_CCCCIII_w33_css_distance_results.json"
CSS_LIFT = ROOT / "PART_CCCCIV_w33_css_steane_lift_results.json"
H1_CERT = ROOT / "PART_CCCLXXXIII_complete_snf_h1_certificate_results.json"
E8_Z3 = ROOT / "artifacts" / "verify_e8_z3grading_from_structure_constants.json"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ok(name: str, cond: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(cond), "value": value}


def build_results() -> Dict[str, Any]:
    photonic = load_json(PHOTONIC)
    css_core = load_json(CSS_CORE)
    css_lift = load_json(CSS_LIFT)
    h1_cert = load_json(H1_CERT)
    e8_z3 = load_json(E8_Z3)

    core_params = css_core["css_parameters"]
    lift_ft = css_lift["fault_tolerance_read"]
    e8_counts = e8_z3["counts"]
    photonic_constants = photonic["constants"]
    photonic_e8 = photonic["e8_operation_audit"]

    checks: List[Dict[str, Any]] = []
    checks.append(ok("photonic runtime verified", photonic["verified"] is True, photonic["checks_passed"]))
    checks.append(ok("photonic runtime has 63 checks", photonic["checks_passed"] == photonic["checks_total"] == 63, photonic["checks_total"]))
    checks.append(ok("W33 constants match 40/12/240", (photonic_constants["v"], photonic_constants["k"], photonic_constants["edges"]) == (V, K, E), photonic_constants))
    checks.append(ok("H1 certificate is complete", h1_cert["complete_certificate"] is True, h1_cert))
    checks.append(ok("H1 free rank = 81", h1_cert["free_rank"] == H1, h1_cert["free_rank"]))
    checks.append(ok("photonic E8 audit sees H1 = 81", photonic_e8["h1_free_rank"] == H1, photonic_e8))
    checks.append(ok("E8 Z3 verifier status ok", e8_z3["status"] == "ok", e8_z3["status"]))
    checks.append(ok("E8 Z3 verifier checked 8347 terms", e8_counts["bracket_terms_checked"] == 8347, e8_counts))
    checks.append(ok("E8 Z3 grade violations zero", e8_counts["grade_term_violations"] == 0, e8_counts))
    checks.append(ok("CSS core is [[240,81,3]]", core_params == {"n": 240, "k": 81, "d": 3, "d_X": 3, "d_Z": 4, "notation": "[[240,81,3]]"}, core_params))
    checks.append(ok("CSS lift verified", css_lift["verified"] is True, css_lift["checks_passed"]))
    checks.append(ok("Steane length = Phi6 = 7", css_lift["inner_code"]["n"] == PHI6, css_lift["inner_code"]))
    checks.append(ok("three-lift code is [[82320,81,>=81]]", lift_ft["three_lift_code"] == "[[82320,81,>=81]]", lift_ft))
    checks.append(ok("protected distance lower bound equals H1", css_lift["lift_table"][3]["distance_lower_bound"] == H1, css_lift["lift_table"][3]))
    checks.append(ok("protected correctable weight equals V", lift_ft["guaranteed_correctable_weight"] == V, lift_ft))
    checks.append(ok("classical record trits equals V", photonic["classical_layer"]["measurement_word_trits"] == V, photonic["classical_layer"]))
    checks.append(ok("logical sector equals protected distance equals H1", core_params["k"] == css_lift["lift_table"][3]["distance_lower_bound"] == H1, {"k": core_params["k"], "d3": css_lift["lift_table"][3]["distance_lower_bound"]}))

    verified = all(c["passed"] for c in checks)
    return {
        "part": "CCCCV",
        "title": "Protected W33 / H1 / E8 TOE Kernel",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(c["passed"] for c in checks),
        "kernel_stack": [
            "W33 projective two-qutrit carrier: 40 points, 240 edges",
            "photonic runtime: probabilistic assembly -> deterministic MBQC -> 40-trit record",
            "topological memory: H1(W33;Z)=Z^81",
            "E8 operation gate: Z3 grading verified on 8347 bracket terms",
            "bare CSS core: [[240,81,3]]",
            "protected Steane/Phi6 lift: [[82320,81,>=81]]",
        ],
        "closure_equalities": {
            "logical_sector": H1,
            "protected_distance_lower_bound": css_lift["lift_table"][3]["distance_lower_bound"],
            "correctable_weight": lift_ft["guaranteed_correctable_weight"],
            "w33_vertices": V,
            "steane_length": PHI6,
            "e8_z3_terms_checked": e8_counts["bracket_terms_checked"],
        },
        "architecture_upgrade": (
            "Promotes the scattered photonic, H1/E8, CSS, and Steane-lift artifacts "
            "into one protected finite TOE-kernel certificate."
        ),
        "theorem": (
            "The current finite W33 kernel has a verified protected information stack: "
            "a 40-point photonic carrier, H1=Z^81 matter memory, an E8 Z3 operation "
            "gate verified on 8347 bracket terms, and a protected CSS architecture "
            "[[82320,81,>=81]] whose correctable weight is 40."
        ),
        "honesty_boundary": (
            "This is the solved finite protected information kernel. It does not "
            "claim that every empirical Standard Model or gravitational observable "
            "has been derived or fit from data."
        ),
        "checks": checks,
    }


def main() -> int:
    results = build_results()
    out = ROOT / "PART_CCCCV_protected_toe_kernel_results.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "part": results["part"],
                "verified": results["verified"],
                "checks_passed": results["checks_passed"],
                "checks_total": results["checks_total"],
                "out_path": str(out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
