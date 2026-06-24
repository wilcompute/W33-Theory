#!/usr/bin/env python3
"""BT1679 — QSVT parity feasibility audit.

Standard single-sequence QSVT/QSP polynomials have parity matching their degree.
On the centered signal x=2(L/Lambda)-1, endpoint projectors that distinguish
x=-1 from x=1 cannot be realized as one parity polynomial.  They need an even/odd
LCU, ancilla-selected sequence, or a different signal model.
"""
from __future__ import annotations

import json
from pathlib import Path

A = 2 ** 0.5 / 3

RESULT = {
    "theorem": "BT1679 Parity-Valid QSVT Phase Compiler Audit",
    "signal_model": "x = 2(L/Lambda) - 1, with standard single-QSVT parity p(-x)=(-1)^d p(x)",
    "spectral_points": {
        "clock": [-1, -A, A, 1],
        "matter": [-1, 0.6, 1]
    },
    "single_sequence_feasibility": {
        "P_clock_6": {
            "targets_at_plus_minus_1": {"p(-1)": 0, "p(1)": 1},
            "single_parity_qsvt_feasible": False,
            "reason": "even parity would force p(-1)=p(1); odd parity would force p(-1)=-p(1). Neither permits {0,1}."
        },
        "P_clock_0": {
            "targets_at_plus_minus_1": {"p(-1)": 1, "p(1)": 0},
            "single_parity_qsvt_feasible": False,
            "reason": "same endpoint-asymmetry obstruction as P_clock_6"
        },
        "P_matter_24": {
            "targets": {"p(-1)": 0, "p(3/5)": 1, "p(1)": 0},
            "single_parity_qsvt_feasible": True,
            "certified_by": "BT1680 even quartic scalar polynomial"
        },
        "P_matter_30": {
            "targets_at_plus_minus_1": {"p(-1)": 0, "p(1)": 1},
            "single_parity_qsvt_feasible": False,
            "reason": "endpoint-asymmetry obstruction"
        }
    },
    "required_compiler_route": {
        "route": "two-sequence even/odd LCU or ancilla-selected QSVT, not one parity-constrained phase sequence",
        "decomposition": "p(x)=p_even(x)+p_odd(x)",
        "endpoint_selector_pattern": {
            "for_target_at_x_equals_1": "p_even(1)=1/2 and p_odd(1)=1/2, with p_even(-1)=1/2 and p_odd(-1)=-1/2",
            "for_target_at_x_equals_minus_1": "swap the sign of the odd component"
        }
    },
    "phase_sequence_status": "No single parity-valid QSVT phase sequence exists for Pc6, Pc0, or Pm30 under this centered signal model. BT1679 therefore emits a correct obstruction and the required two-sequence compiler route instead of a false phase list.",
    "boundary": "This does not rule out QSVT implementation. It rules out one standard single-parity polynomial for endpoint selectors in the centered signal model."
}


def main() -> None:
    out = Path("data/PART_BT1679_PARITY_VALID_QSVT_PHASE_COMPILER_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(RESULT, indent=2) + "\n")
    print(json.dumps(RESULT, indent=2))


if __name__ == "__main__":
    main()
