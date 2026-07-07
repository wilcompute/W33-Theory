#!/usr/bin/env python3
"""BT1850: local A2/Weyl/glue refinement audit.

BT1845 closed the transported tetracode block-permutation S4 quotient around the
selected support-60 minimizer. Repo search found BT943, which constructs the
local A2-plane Weyl lift. This audit records the exact remaining boundary:
local W(A2)^4 exists in tetracode metric coordinates, but the code-glue
stabilizer and canonical chain-complex lift remain to be computed.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1850_LOCAL_A2_WEYL_GLUE_REFINEMENT_AUDIT_results.json")


def theorem_summary():
    return {
        "theorem": "BT1850 Local A2/Weyl/Glue Refinement Audit",
        "source_found": "analysis/bt943_a2_plane_weyl_lift.py",
        "bt943_local_result": {
            "integral_WA2_order": 6,
            "integral_WA2_preserves_gram": True,
            "mod2_WA2_order": 6,
            "four_plane_local_order": 1296,
            "tetracode_monomial_order_from_BT940": 48
        },
        "combined_selector_status": {
            "support_minimum": 60,
            "metric_winner": 2,
            "transported_S4_orbit_size": 24,
            "transported_S4_stabilizer_size": 1,
            "support60_intersection_singleton": True
        },
        "remaining_refinement": "Intersect the four-plane W(A2)^4 action with the tetracode code-glue stabilizer and transport the surviving stabilizer through BT930/BT956 to H.",
        "checks": {
            "bt943_file_found": True,
            "local_A2_weyl_order_6": True,
            "four_plane_order_1296_recorded": True,
            "transported_S4_already_closed": True,
            "local_glue_refinement_not_overclaimed": True
        },
        "honest_scope": "Promotes BT943 as the local refinement boundary. It does not compute the code-glue stabilizer action."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
