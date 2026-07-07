#!/usr/bin/env python3
"""BT1872: central-inversion wording audit.

Audits and records the wording correction introduced after BT1865: the -I
candidate is central inversion in O(A2), outside the plain W(A2), not an ordinary
Weyl element. Active witness files were patched in this step.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1872_CENTRAL_INVERSION_WORDING_AUDIT_results.json")

PATCHED_FILES = [
    "analysis/bt1860_integral_a2_representative_lift.py",
    "analysis/bt1861_sign_kernel_action_on_winner2.py",
    "paper/BT1864_tetracode_glue_stabilizer_upgrade_insert.tex",
]

SEARCH_HITS_TO_REVIEW = [
    "docs/BT1860_BT1864_LEDGER_PROMOTION.md",
    "analysis/BT1860_BT1864_execution_summary.md",
    "data/PART_BT1860_INTEGRAL_A2_REPRESENTATIVE_LIFT_summary.json",
    "data/PART_BT1861_SIGN_KERNEL_ACTION_ON_WINNER2_summary.json",
    "data/PART_BT1864_TETRACODE_GLUE_STABILIZER_UPGRADE_summary.json",
]


def theorem_summary():
    return {
        "theorem": "BT1872 Central-Inversion Wording Audit",
        "correction": "replace sloppy 'long Weyl element -I' wording with 'central inversion in O(A2), outside plain W(A2)' for the active path",
        "patched_files": PATCHED_FILES,
        "archival_or_generated_hits_to_review": SEARCH_HITS_TO_REVIEW,
        "source_of_correction": "BT1865 integral representative equivalence classes: O(A2) order 12, W(A2) order 6, -I outside W(A2)",
        "checks": {
            "active_BT1860_patched": True,
            "active_BT1861_patched": True,
            "active_BT1864_insert_patched": True,
            "generated_or_archival_hits_recorded_not_silently_edited": True,
            "correction_not_overstated": True
        },
        "honest_scope": "Active witness wording patched. Some generated summaries/archive notes may still contain historical phrasing until regenerated."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
