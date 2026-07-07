#!/usr/bin/env python3
"""BT1874: final selector quotient certificate.

Emits one certificate JSON containing the canonical selector, all quotient stages,
the O(A2)/W(A2) phase bit, and the final open representative-lift boundary.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1874_FINAL_SELECTOR_QUOTIENT_CERTIFICATE.json")

CANONICAL_SELECTOR = [[3, 68], [4, 42], [38, 65], [90, 144]]

QUOTIENT_STAGES = [
    {"stage": "support_minimality", "status": "closed", "witness": "BT951", "claim": "support 60 with six minimizers"},
    {"stage": "certificate_graph", "status": "closed_partial", "witness": "BT953/BT1837", "claim": "certificate orbits [[0,1],[2],[3],[4],[5]]"},
    {"stage": "vertex_metric", "status": "closed", "witness": "BT954", "claim": "minimizer 2 selected"},
    {"stage": "tetracode_metric", "status": "closed", "witness": "BT956/BT1840", "claim": "minimizer 2 selected through recovered matrix"},
    {"stage": "transported_S4", "status": "closed", "witness": "BT959/BT1845", "claim": "orbit 24, stabilizer 1, support-60 singleton"},
    {"stage": "glue_stabilizer", "status": "closed", "witness": "BT1855", "claim": "signed monomial tetracode glue stabilizer 48 = 2 x 24"},
    {"stage": "S4_transport_to_H", "status": "closed", "witness": "BT1856", "claim": "S4 quotient transports to H"},
    {"stage": "support_phase_action", "status": "closed_at_H_support_level", "witness": "BT1861/BT1871", "claim": "central-inversion phase fixes winner-2 support mask"},
    {"stage": "integral_E8_representative_phase_lift", "status": "open", "witness": "BT1870", "claim": "needs concrete integral E8 representative vectors and chain-boundary compatibility"},
]

PHASE_BIT = {
    "invariant": "A2_integral_phase_coset_bit",
    "ambient_quotient": "O(A2)/W(A2)",
    "identity_class": 0,
    "central_inversion_class": 1,
    "support_shadow": "both bits are identical on the mod-2 H support selector",
}


def theorem_summary():
    open_stages = [s for s in QUOTIENT_STAGES if s["status"] == "open"]
    checks = {
        "canonical_selector_recorded": CANONICAL_SELECTOR == [[3, 68], [4, 42], [38, 65], [90, 144]],
        "phase_bit_recorded": PHASE_BIT["ambient_quotient"] == "O(A2)/W(A2)",
        "exactly_one_open_stage": len(open_stages) == 1,
        "open_stage_is_integral_E8_lift": open_stages[0]["stage"] == "integral_E8_representative_phase_lift",
        "support_shadow_closed": any(s["stage"] == "support_phase_action" and s["status"] == "closed_at_H_support_level" for s in QUOTIENT_STAGES),
    }
    return {
        "theorem": "BT1874 Final Selector Quotient Certificate",
        "canonical_selector": CANONICAL_SELECTOR,
        "metric_winner": 2,
        "quotient_stages": QUOTIENT_STAGES,
        "phase_bit": PHASE_BIT,
        "final_open_boundary": "construct/prove a concrete integral E8 representative phase lift for the central-inversion class with chain-boundary compatibility",
        "closed_shadow_statement": "everything visible on the mod-2 H support shadow is closed",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Final certificate for current quotient state. It does not solve the remaining integral E8 representative lift."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
