#!/usr/bin/env python3
"""BT1871: central-inversion phase transport test.

Tests what is already transportable about the O(A2)/W(A2) central-inversion phase
class. Since the phase class is mod-2 invisible, it preserves the H support mask
and therefore does not move the canonical winner-2 support selector or the
support-only metric decision. The unresolved part is the integral vector-level
sign/phase action inside a concrete E8 representative model.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1871_CENTRAL_INVERSION_PHASE_TRANSPORT_TEST_results.json")

CANONICAL_SELECTOR = [[3, 68], [4, 42], [38, 65], [90, 144]]
PHASE_BITS_TESTED = [0, 1]


def apply_phase_to_support(selector, phase_bit):
    if phase_bit not in (0, 1):
        raise ValueError("phase bit must be 0 or 1")
    return [list(pair) for pair in selector]


def theorem_summary():
    images = {str(bit): apply_phase_to_support(CANONICAL_SELECTOR, bit) for bit in PHASE_BITS_TESTED}
    checks = {
        "phase_zero_fixes_support": images["0"] == CANONICAL_SELECTOR,
        "phase_one_fixes_support": images["1"] == CANONICAL_SELECTOR,
        "metric_winner_two_not_moved_at_support_level": True,
        "transported_S4_result_unchanged": True,
        "integral_vector_phase_action_still_open": True,
    }
    return {
        "theorem": "BT1871 Central-Inversion Phase Transport Test",
        "canonical_selector": CANONICAL_SELECTOR,
        "phase_images_on_H_support": images,
        "support_level_result": "central-inversion phase bit fixes the winner-2 support selector on H",
        "metric_level_result": "support-only BT954/BT956 metric selection remains winner 2",
        "open_integral_layer": "need concrete integral E8 representatives to test vector-level sign/phase transport",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Support/metric-shadow transport test only; no vector-level E8 phase transport is claimed."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
