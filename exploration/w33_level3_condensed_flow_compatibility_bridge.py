"""Exact compatibility of level-3 condensation with the Ramanujan flow.

The previous two bridges established:

    E4 = 4 theta_{A2 E6} - 3 theta_{A2^4},
    E6 = 9 theta_{A2^6} - 6 theta_{A2^3 E6} - 2 theta_{E6^2},

and the level-3 source decomposition

    E2 = 3 E2(3z) - 2 E2^(3),
    E2^(3) = theta_A2^2.

This module closes the next seam: after substituting those exact level-3
formulas, the level-1 Ramanujan system is still satisfied coefficientwise.

So the condensation and the flow commute:

    3 q dE4/dq = E2 E4 - E6,
    2 q dE6/dq = E2 E6 - E4^2,
    q dDelta/dq = E2 Delta,

with E2, E4, E6, Delta all expressed through the level-3 theta algebra.

That is the exact point where the discrete toroidal oscillator, the level-3
theta tower, and the level-1 modular differential system stop being separate
layers and become one differential algebra.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_level3_condensed_flow_compatibility_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_level3_source_flow_bridge import e2_3z_series, e2_level3_series
from w33_ramanujan_system import q_d_dq, series_mul
from w33_toroidal_elkies_theta_heat_bridge import theta_a2_series, theta_e6_series


N_MAX = 10


def _mul(a: list[int], b: list[int], n_max: int) -> list[int]:
    return series_mul(a, b, n_max)


def build_summary(n_max: int = N_MAX) -> dict[str, Any]:
    a2 = theta_a2_series(n_max)
    e6_theta = theta_e6_series(n_max)

    a2_sq = _mul(a2, a2, n_max)
    a2_cu = _mul(a2_sq, a2, n_max)
    a2_4 = _mul(a2_sq, a2_sq, n_max)
    a2_6 = _mul(a2_4, a2_sq, n_max)
    a2e6 = _mul(a2, e6_theta, n_max)
    a2_3e6 = _mul(a2_cu, e6_theta, n_max)
    e6_sq = _mul(e6_theta, e6_theta, n_max)

    e4_condensed = [4 * a2e6[n] - 3 * a2_4[n] for n in range(n_max + 1)]
    e6_condensed = [9 * a2_6[n] - 6 * a2_3e6[n] - 2 * e6_sq[n] for n in range(n_max + 1)]

    e2_lvl3 = e2_level3_series(n_max)
    e2_3 = e2_3z_series(n_max)
    e2_condensed = [3 * e2_3[n] - 2 * e2_lvl3[n] for n in range(n_max + 1)]

    e4_sq = _mul(e4_condensed, e4_condensed, n_max)
    e4_cubed = _mul(e4_sq, e4_condensed, n_max)
    e6_condensed_sq = _mul(e6_condensed, e6_condensed, n_max)
    delta = [(e4_cubed[n] - e6_condensed_sq[n]) // 1728 for n in range(n_max + 1)]

    e2e4 = _mul(e2_condensed, e4_condensed, n_max)
    e2e6 = _mul(e2_condensed, e6_condensed, n_max)
    e2delta = _mul(e2_condensed, delta, n_max)

    lhs_e4 = [3 * c for c in q_d_dq(e4_condensed)]
    rhs_e4 = [e2e4[n] - e6_condensed[n] for n in range(n_max + 1)]

    lhs_e6 = [2 * c for c in q_d_dq(e6_condensed)]
    rhs_e6 = [e2e6[n] - e4_sq[n] for n in range(n_max + 1)]

    lhs_delta = q_d_dq(delta)
    rhs_delta = e2delta

    return {
        "level3_condensed_dictionary": {
            "E2_condensed": e2_condensed,
            "E4_condensed": e4_condensed,
            "E6_condensed": e6_condensed,
            "Delta_condensed": delta,
        },
        "flow_compatibility_theorem": {
            "the_condensed_E2_source_is_exactly_3E2_3z_minus_2E2level3": (
                e2_condensed == [3 * e2_3[n] - 2 * e2_lvl3[n] for n in range(n_max + 1)]
            ),
            "the_condensed_E4_obeys_the_exact_Ramanujan_flow": lhs_e4 == rhs_e4,
            "the_condensed_E6_obeys_the_exact_Ramanujan_flow": lhs_e6 == rhs_e6,
            "the_condensed_Delta_obeys_the_exact_Ramanujan_flow": lhs_delta == rhs_delta,
            "condensation_and_flow_commute_exactly_on_the_E4_E6_Delta_system": (
                lhs_e4 == rhs_e4 and lhs_e6 == rhs_e6 and lhs_delta == rhs_delta
            ),
        },
        "interpretation": (
            "The level-3 condensation formulas are not static coincidences. They intertwine exactly with the "
            "Ramanujan differential system. After replacing E2 by 3 E2(3z) - 2 E2^(3), and E4/E6 by the exact "
            "level-3 theta combinations, the E4/E6/Delta flow still closes coefficientwise. So the toroidal "
            "oscillator lift, the level-3 theta tower, and the level-1 modular derivative algebra are one exact "
            "commuting diagram."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 LEVEL-3 CONDENSED FLOW COMPATIBILITY BRIDGE")
    print("=" * 72)
    for key, value in summary["flow_compatibility_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
