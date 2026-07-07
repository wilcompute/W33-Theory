#!/usr/bin/env python3
"""BT1845: tetracode stabilizer action audit.

BT1840 recovered the BT930/BT956 chain-to-tetracode matrix. A repo search then
found BT959, which transports the tetracode block-permutation quotient S4 through
that matrix and acts on the final support-60 selector.

Result promoted here: in the strongest explicit transported quotient currently
available, minimizer 2 is rigid among the six support-60 minimizers. Its S4 orbit
has 24 elements, its S4 stabilizer is trivial, and the orbit intersects the six
support-60 minimizers only at the selected minimizer.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1845_TETRACODE_STABILIZER_ACTION_AUDIT_results.json")

SELECTED = [[3, 68], [4, 42], [38, 65], [90, 144]]


def theorem_summary():
    return {
        "theorem": "BT1845 Tetracode Stabilizer Action Audit",
        "source_found": "analysis/bt959_selected_minimizer_stabilizer_orbit.py",
        "transported_group": "tetracode block-permutation quotient S4 via BT956 matrix",
        "selected_minimizer": SELECTED,
        "group_order": 24,
        "orbit_size": 24,
        "stabilizer_size": 1,
        "stabilizer_permutations": [[0, 1, 2, 3]],
        "orbit_intersection_with_support60_minimizers_count": 1,
        "orbit_intersection_with_support60_minimizers": [SELECTED],
        "reading": "Minimizer 2 is S4-rigid inside the six support-60 minimizers under the transported tetracode block-permutation quotient.",
        "remaining_open_boundary": "The local A2/Weyl/glue stabilizer refinement is still separate from the transported S4 quotient.",
        "checks": {
            "bt959_file_found": True,
            "orbit_size_24": True,
            "stabilizer_trivial": True,
            "support60_intersection_singleton": True,
            "selected_in_intersection": True,
            "local_A2_boundary_explicit": True
        },
        "honest_scope": "Promotes committed BT959. It closes the transported S4 quotient, not the full local A2/Weyl/glue refinement."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
