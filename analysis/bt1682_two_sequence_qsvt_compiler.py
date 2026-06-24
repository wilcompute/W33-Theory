#!/usr/bin/env python3
"""BT1682 — two-sequence even/odd QSVT compiler route.

BT1679 proves endpoint selectors are not single parity-QSVT polynomials in the
centered signal x=2(L/Lambda)-1.  BT1682 gives explicit bounded even/odd
polynomial decompositions for those endpoint selectors.
"""
from __future__ import annotations

import json
from pathlib import Path

RESULT = {
    "theorem": "BT1682 Two-Sequence Even/Odd QSVT Compiler",
    "signal_model": "x = 2(L/Lambda)-1",
    "clock_spectrum": ["-1", "-sqrt(2)/3", "sqrt(2)/3", "1"],
    "matter_spectrum": ["-1", "3/5", "1"],
    "clock_endpoint_decomposition": {
        "a_squared": "2/9",
        "even_component": {
            "formula_power": "e_c(x)=(9/14)x^2-1/7",
            "formula_chebyshev": "e_c(x)=5/28*T0 + 9/28*T2",
            "sup_norm": "1/2",
            "chebyshev_l1": 0.5
        },
        "odd_component": {
            "formula_power": "o_c(x)=(9/14)x^3-(1/7)x",
            "formula_chebyshev": "o_c(x)=19/56*T1 + 9/56*T3",
            "sup_norm": "1/2",
            "chebyshev_l1": 0.5
        },
        "P_clock_6": "e_c + o_c; values 0 at -1 and +-sqrt(2)/3, 1 at +1",
        "P_clock_0": "e_c - o_c; values 1 at -1, 0 at +-sqrt(2)/3 and +1",
        "two_sequence_l1_each": 1.0
    },
    "matter_30_endpoint_decomposition": {
        "even_component": {
            "formula_power": "e_30(x)=(5/4)x^2-3/4",
            "formula_chebyshev": "e_30(x)=-1/8*T0 + 5/8*T2",
            "sup_norm": "3/4",
            "chebyshev_l1": 0.75
        },
        "odd_component": {
            "formula_power": "o_30(x)=x/2",
            "formula_chebyshev": "o_30(x)=1/2*T1",
            "sup_norm": "1/2",
            "chebyshev_l1": 0.5
        },
        "P_matter_30": "e_30 + o_30; values 0 at -1 and 3/5, 1 at +1",
        "two_sequence_l1": 1.25
    },
    "matter_24_single_sequence": {
        "source": "BT1680 even quartic",
        "formula_power": "p_24(x)=-(625/256)x^4+(225/128)x^2+175/256",
        "chebyshev_l1": 1.2939453125,
        "sup_norm": 1,
        "parity": "even"
    },
    "two_port_logical_lcu_cost": {
        "resonance_Pc6_tensor_Pm24": 1.2939453125,
        "companion_Pc0_tensor_Pm30": 1.25,
        "combined": 2.5439453125,
        "previous_BT1676_sampled_chebyshev_combined": 215.6020503790747,
        "ratio_to_BT1676": 0.011799264886933462
    },
    "interpretation": "The parity obstruction from BT1679 is not fatal. Endpoint selectors require a two-sequence even/odd LCU or ancilla-selected QSVT route. In that model the bounded logical polynomial masses are small.",
    "boundary": "This gives exact bounded scalar polynomials and an LCU routing rule. It still does not list hardware QSP phase angles for each bounded component."
}


def main() -> None:
    out = Path("data/PART_BT1682_TWO_SEQUENCE_QSVT_COMPILER_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(RESULT, indent=2) + "\n")
    print(json.dumps(RESULT, indent=2))


if __name__ == "__main__":
    main()
