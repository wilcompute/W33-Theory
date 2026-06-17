#!/usr/bin/env python3
"""BT1214 -- encoded Clifford/gate-tomography invariance verifier.

BT1211 checked q-invariance through encoding.  BT1214 checks the next invariant:
the target Clifford closure signature should remain Sp(4,3) of order 51840 from
bare demonstrator through D4-GKP inner code and Steinberg outer code.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SP43_ORDER = 51840
SINGLE_QUTRIT_HOLONOMY_ORDER = 24
STEINBERG_CODE = "[[240,81,4]]_3"

LAYERS = [
    {
        "layer": "bare_demonstrator",
        "q": 3,
        "tomography_target": "single-qutrit 2T fingerprint plus generated two-qutrit Sp(4,3)",
        "single_qutrit_holonomy_order": 24,
        "two_qutrit_clifford_order": 51840,
        "alphabet_preserved": True,
        "requires_gkp_threshold": False,
    },
    {
        "layer": "inner_D4_GKP",
        "q": 3,
        "tomography_target": "encoded Gaussian/Clifford action on GKP qutrit displacement cosets",
        "single_qutrit_holonomy_order": 24,
        "two_qutrit_clifford_order": 51840,
        "alphabet_preserved": True,
        "requires_gkp_threshold": True,
    },
    {
        "layer": "outer_Steinberg_logical",
        "q": 3,
        "tomography_target": "logical Clifford action preserving Steinberg code space",
        "single_qutrit_holonomy_order": 24,
        "two_qutrit_clifford_order": 51840,
        "alphabet_preserved": True,
        "requires_gkp_threshold": True,
    },
]

TESTS = [
    {
        "id": "T1",
        "name": "single-qutrit holonomy fingerprint",
        "expected": "2T = SL(2,3), order 24, element-order spectrum {1,1,8,6,8}",
    },
    {
        "id": "T2",
        "name": "two-qutrit Clifford closure",
        "expected": "Sp(4,3), order 51840 modulo Pauli/frame conventions",
    },
    {
        "id": "T3",
        "name": "encoded alphabet preservation",
        "expected": "all measured logical Paulis close over F3/qutrit displacement classes",
    },
    {
        "id": "T4",
        "name": "logical-code preservation",
        "expected": "outer operations preserve the [[240,81,4]]_3 codespace and act on 81 logical qutrits",
    },
]


def build_result() -> dict:
    layer_checks = []
    for layer in LAYERS:
        layer_checks.append({
            "layer": layer["layer"],
            "q_is_3": layer["q"] == 3,
            "single_qutrit_order_ok": layer["single_qutrit_holonomy_order"] == SINGLE_QUTRIT_HOLONOMY_ORDER,
            "two_qutrit_clifford_order_ok": layer["two_qutrit_clifford_order"] == SP43_ORDER,
            "alphabet_preserved": layer["alphabet_preserved"],
            "passes_static_signature": layer["q"] == 3 and layer["single_qutrit_holonomy_order"] == 24 and layer["two_qutrit_clifford_order"] == 51840 and layer["alphabet_preserved"],
        })
    return {
        "bt": 1214,
        "title": "Encoded Clifford/gate-tomography invariance theorem",
        "layers": LAYERS,
        "tests": TESTS,
        "layer_checks": layer_checks,
        "all_layers_preserve_static_clifford_signature": all(x["passes_static_signature"] for x in layer_checks),
        "tomography_protocol": [
            "Estimate single-qutrit 2T closure and order spectrum at the bare layer.",
            "Lift to generated two-qutrit Sp(4,3) closure and check order 51840 modulo Pauli/frame conventions.",
            "Repeat on encoded GKP qutrit displacement cosets after syndrome recovery.",
            "Repeat on Steinberg logical operators and require preservation of the [[240,81,4]]_3 codespace."
        ],
        "honesty_boundary": "This is a static target-signature verifier and protocol map. It does not claim encoded hardware has achieved the closure until gate tomography/RB data populate the tests.",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=Path("data/bt1214_encoded_clifford_tomography_invariance.json"))
    args = p.parse_args()
    result = build_result()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1214, "passes": result["all_layers_preserve_static_clifford_signature"], "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
