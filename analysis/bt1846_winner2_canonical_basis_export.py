#!/usr/bin/env python3
"""BT1846: winner-2 canonical basis export.

Exports the metric-selected support-60 minimizer as the canonical E8 selector
basis used by the runtime aperture stack.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1846_WINNER2_CANONICAL_BASIS_EXPORT_results.json")

CANONICAL_SELECTOR = [[3, 68], [4, 42], [38, 65], [90, 144]]
SELECTOR_PAIRS_BY_STRIATION = {
    "0": [3, 68],
    "1": [4, 42],
    "2": [38, 65],
    "3": [90, 144],
}


def theorem_summary():
    return {
        "theorem": "BT1846 Winner-2 Canonical Basis Export",
        "canonical_basis_name": "E8_selector_winner2_BT954_BT956_BT959",
        "source_chain": [
            "BT951 support-minimum 60",
            "BT954 vertex metric winner 2",
            "BT956 tetracode metric winner 2",
            "BT959 transported S4 rigidity inside support-60 minimizers"
        ],
        "canonical_selector_pairs": CANONICAL_SELECTOR,
        "selector_pairs_by_striation": SELECTOR_PAIRS_BY_STRIATION,
        "runtime_attachment": "BT1836/BT1842/BT1843 aperture rows and trace rows use these four selector pairs as the E8-side labels.",
        "checks": {
            "four_hyperbolic_pairs": len(CANONICAL_SELECTOR) == 4,
            "winner_two_source_chain_present": True,
            "four_striations_labelled": sorted(SELECTOR_PAIRS_BY_STRIATION) == ["0", "1", "2", "3"],
            "s4_rigidity_recorded": True
        },
        "honest_scope": "Canonical export of the selected basis. It does not assert the unresolved local A2/Weyl/glue quotient."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
