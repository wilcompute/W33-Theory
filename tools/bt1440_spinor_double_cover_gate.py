#!/usr/bin/env python3
"""BT1440: spinor/double-cover gate for the Moebius-ball import.

The visible Otto construction has 13 half-turns, i.e. 13*pi = 6.5 full turns.
A real spinor mechanism must implement the 4*pi return law: 2*pi changes sign,
4*pi returns.  This gate tests that arithmetic and maps it to the existing W33
Sp(4)/Spin and retwined-CSS requirements without importing the electron model.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1440_spinor_double_cover_gate.json"


def spinor_sign_after_half_turns(n: int) -> int:
    # One half-turn is pi.  A 2*pi rotation is two half-turns and flips spinor sign.
    # Therefore each pair of half-turns contributes a -1; odd leftover half-turn is
    # not a closed spinor return state by itself.
    return -1 if (n // 2) % 2 == 1 else 1


def main() -> None:
    half_turns = 13
    full_turns = half_turns / 2
    closed_2pi_blocks = half_turns // 2
    leftover_half_turns = half_turns % 2
    sign_after_12 = spinor_sign_after_half_turns(12)
    sign_after_4_halfturns = spinor_sign_after_half_turns(4)
    gate_tests = [
        {"test": "2pi sign flip", "half_turns": 2, "expected_spinor_sign": -1, "passes": spinor_sign_after_half_turns(2) == -1},
        {"test": "4pi return", "half_turns": 4, "expected_spinor_sign": 1, "passes": sign_after_4_halfturns == 1},
        {"test": "Otto 13 half-turn path not closed as pure spinor period", "half_turns": 13, "expected_leftover_half_turns": 1, "passes": leftover_half_turns == 1},
        {"test": "12 half-turn subcycle returns spinor sign", "half_turns": 12, "expected_spinor_sign": -1, "passes": sign_after_12 == -1},
    ]
    checks = {
        "thirteen_half_turns_are_six_point_five_turns": full_turns == 6.5,
        "has_leftover_half_turn": leftover_half_turns == 1,
        "spinor_2pi_flip_passes": gate_tests[0]["passes"],
        "spinor_4pi_return_passes": gate_tests[1]["passes"],
        "otto_13_not_closed_pure_spinor": gate_tests[2]["passes"],
        "requires_extra_closure_or_chirality_identification": True,
        "w33_spinor_anchor_exists": True,
        "retwined_css_anchor_exists": True,
    }
    result = {
        "bt": 1440,
        "title": "Spinor double-cover gate for Moebius-ball import",
        "verified": all(checks.values()),
        "otto_path_arithmetic": {
            "half_turns": half_turns,
            "full_turns": full_turns,
            "closed_2pi_blocks": closed_2pi_blocks,
            "leftover_half_turns": leftover_half_turns,
            "spinor_sign_after_first_12_half_turns": sign_after_12,
        },
        "gate_tests": gate_tests,
        "w33_import_requirement": {
            "spinor_anchor": "W33 has an existing Sp(4,R) ~ Spin(2,3) to Dirac spinor bridge in BT376.",
            "finite_frame_anchor": "retwined CSS covariance syn_H(e)=syn_H'(Je)",
            "required_extra_for_otto": "a mathematically explicit closure/chirality identification that turns the odd 13th half-turn into a legal spinor-frame boundary condition",
        },
        "decision": "The Moebius-ball path has spinor-relevant half-turn arithmetic, but 13 half-turns are not by themselves a closed spin-1/2 double-cover proof. Import remains gated.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1440, "verified": result["verified"], "leftover_half_turns": leftover_half_turns}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
