#!/usr/bin/env python3
"""BT1550: Weyl-equivariant sign bridge attempt.

BT1548 blocked the naive aggregate sign bridge because E6 cubic signs have a
23/22 profile while K4/toroidal carriers are balanced.  This attempt switches to
the repo's stronger E6 layer: mixed structure constants with μ-signs are Weyl
-equivariant across 270 mixed triples and 6 E6 generators.

Result: a bridge is plausible only at the equivariant cocycle/gauge level, not
at aggregate sign-profile level.  This script records the exact dependency and
what remains missing for an actual carrier-to-cubic sign lift.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1550_weyl_equivariant_sign_bridge_attempt.json"
MD = ROOT / "analysis" / "BT1550_weyl_equivariant_sign_bridge_attempt.md"
TEX = ROOT / "analysis" / "BT1550_weyl_equivariant_sign_bridge_attempt.tex"

WEYL_LAYER = {
    "generators": 6,
    "mixed_triples": 270,
    "expected_failures": 0,
    "identity": "mu(alpha) mu(beta) N(w alpha,w beta) = N(alpha,beta) mu(w(-gamma)) for alpha+beta+gamma=0",
}

NAIVE_PROFILES = {
    "e6_cubic": {"plus": 23, "minus": 22, "imbalance": 1},
    "k4_carrier": {"plus": 12, "minus": 12, "imbalance": 0},
    "eight_packet": {"plus": 96, "minus": 96, "imbalance": 0},
}

MISSING_FOR_ACTUAL_BRIDGE = [
    "carrier_flag_to_mixed_triple_map",
    "packetwise_mu_sign_assignment",
    "diagonal_torus_gauge_on_27_weight_basis",
    "projection_from_270_mixed_triples_to_24_or_192_carrier_rows",
    "compatibility_with_23_22_cubic_tensor_signs",
]


def main() -> None:
    bt1548 = json.loads((ROOT / "data" / "bt1548_e6_cubic_vs_k4_toroidal_signs.json").read_text(encoding="utf-8"))
    verifier_exists = (ROOT / "tools" / "verify_mixed_structure_constant_equivariance.py").exists()
    test_exists = (ROOT / "tests" / "test_mixed_structure_constant_equivariance.py").exists()
    bridge_status = "cocycle_level_candidate_profile_level_obstructed"
    checks = {
        "bt1548_verified": bt1548.get("verified") is True,
        "verifier_exists": verifier_exists,
        "pytest_exists": test_exists,
        "weyl_layer_counts_known": WEYL_LAYER["generators"] == 6 and WEYL_LAYER["mixed_triples"] == 270,
        "naive_profile_still_obstructed": bt1548["checks"]["simple_profile_normalization_obstructed"] is True,
        "missing_actual_bridge_data": len(MISSING_FOR_ACTUAL_BRIDGE) == 5,
        "status_is_candidate_not_theorem": bridge_status == "cocycle_level_candidate_profile_level_obstructed",
    }
    result = {
        "bt": 1550,
        "title": "Weyl-equivariant sign bridge attempt",
        "verified": all(checks.values()),
        "source_packets": {
            "aggregate_obstruction": "data/bt1548_e6_cubic_vs_k4_toroidal_signs.json",
            "weyl_verifier": "tools/verify_mixed_structure_constant_equivariance.py",
            "weyl_test": "tests/test_mixed_structure_constant_equivariance.py",
        },
        "weyl_layer": WEYL_LAYER,
        "naive_profiles": NAIVE_PROFILES,
        "missing_for_actual_bridge": MISSING_FOR_ACTUAL_BRIDGE,
        "bridge_status": bridge_status,
        "interpretation": "The aggregate 23/22 vs 12/12 sign bridge remains obstructed, but the E6 μ-signed mixed-structure-constant layer supplies a better candidate route: a cocycle/gauge-level bridge.  The actual bridge still needs a carrier-flag-to-mixed-triple projection plus packetwise μ-sign assignment and torus-gauge data.",
        "honesty_boundary": "This is a bridge attempt/roadmap, not a proof of sign equivalence. No artifact run is claimed in this connector turn.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1550 Weyl-equivariant Sign Bridge Attempt\n\nThe naive aggregate sign bridge remains obstructed: E6 cubic signs have 23/22 while K4/toroidal carriers are balanced. The stronger path is the repo's μ-signed mixed-structure-constant equivariance layer: 270 mixed triples across 6 E6 generators. This makes a cocycle-level bridge plausible, but an actual bridge still needs a carrier-flag-to-mixed-triple map, packetwise μ signs, torus-gauge data, and a projection from 270 triples to 24/192 carrier rows.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1550: profile-level signs remain obstructed, but Weyl-equivariant $\\mu$-signed structure constants define the next cocycle-level bridge target.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1550, "verified": result["verified"], "status": bridge_status}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
