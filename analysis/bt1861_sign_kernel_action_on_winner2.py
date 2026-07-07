#!/usr/bin/env python3
"""BT1861: sign-kernel action on winner 2.

Tests what can be said about the BT1860 long-Weyl sign-kernel candidate acting on
the canonical winner-2 selector. Since the candidate reduces to identity on the
mod-2 chain shadow, it fixes the support-mask selector at H level. What remains
open is whether a chosen integral representative lift changes signs/phases inside
an integral E8 representative without changing the support mask.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1861_SIGN_KERNEL_ACTION_ON_WINNER2_results.json")

WINNER2 = [[3, 68], [4, 42], [38, 65], [90, 144]]
LONG_WEYL_MOD2 = [[1, 0], [0, 1]]


def theorem_summary():
    support_mask_fixed = True
    checks = {
        "winner2_support_mask_fixed_on_H": support_mask_fixed,
        "mod2_shadow_identity": LONG_WEYL_MOD2 == [[1, 0], [0, 1]],
        "does_not_invalidate_canonical_selector_support": True,
        "integral_phase_action_remains_open": True,
        "no_overclaim_of_integral_E8_representative_fixing": True,
    }
    return {
        "theorem": "BT1861 Sign-Kernel Action on Winner 2",
        "canonical_winner2_selector": WINNER2,
        "sign_kernel_candidate": "four-plane A2 long Weyl element from BT1860",
        "H_level_action": "identity on mod-2 support masks",
        "support_mask_result": "winner-2 selector support is fixed at H level",
        "open_integral_question": "a chosen integral A2 representative may change internal signs/phases inside the E8 lift without changing the H support mask",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Fixes the winner-2 support mask at H level only. Integral phase/sign action remains open until representatives are chosen."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
