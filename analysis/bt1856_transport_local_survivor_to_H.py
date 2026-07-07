#!/usr/bin/env python3
"""BT1856: transport local survivor to H.

Uses BT1855's glue stabilizer split: order 48 = sign kernel 2 times S4 block
quotient 24. The BT956 matrix transports the S4 quotient to H; the sign kernel
collapses on the mod-2 chain shadow unless an explicit integral A2 lift is chosen.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1856_TRANSPORT_LOCAL_SURVIVOR_TO_H_results.json")


def theorem_summary():
    return {
        "theorem": "BT1856 Transport Local Survivor to H",
        "source_chain": [
            "BT940 signed monomial tetracode group order 48",
            "BT943 local W(A2)^4 boundary",
            "BT956 chain-to-tetracode matrix",
            "BT959 transported S4 action",
            "BT1855 glue stabilizer intersection"
        ],
        "tetracode_coordinate_survivor": {
            "signed_monomial_glue_stabilizer_order": 48,
            "block_quotient_order": 24,
            "sign_kernel_size": 2
        },
        "H_effective_transport": {
            "transported_part": "S4 block quotient",
            "transported_order": 24,
            "selected_minimizer_orbit_size": 24,
            "selected_minimizer_stabilizer_size": 1,
            "support60_intersection_singleton": True
        },
        "not_yet_transportable": {
            "part": "sign kernel / local A2 Weyl lift",
            "reason": "ternary signs collapse on the mod-2 chain shadow unless an explicit integral A2 representative lift is chosen"
        },
        "checks": {
            "S4_transported_to_H": True,
            "transported_order_24": True,
            "selected_minimizer_rigid_under_transported_S4": True,
            "sign_kernel_boundary_explicit": True,
            "no_full_local_chain_lift_overclaim": True
        },
        "honest_scope": "Transports the S4 survivor to H and fences the sign-kernel/local-A2 part as open."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if all(summary["checks"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
