#!/usr/bin/env python3
"""BT1877: regenerate corrected summaries audit.

Records the generated/static summaries updated after BT1865/BT1872 corrected the
terminology from sloppy long-Weyl wording to central inversion in O(A2), outside
plain W(A2).
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1877_REGENERATE_CORRECTED_SUMMARIES_AUDIT_results.json")

UPDATED_FILES = [
    "data/PART_BT1860_INTEGRAL_A2_REPRESENTATIVE_LIFT_summary.json",
    "data/PART_BT1861_SIGN_KERNEL_ACTION_ON_WINNER2_summary.json",
    "data/PART_BT1864_TETRACODE_GLUE_STABILIZER_UPGRADE_summary.json",
    "docs/BT1860_BT1864_LEDGER_PROMOTION.md",
    "analysis/BT1860_BT1864_execution_summary.md",
]


def theorem_summary():
    return {
        "theorem": "BT1877 Regenerate Corrected Summaries Audit",
        "correction": "central inversion in O(A2), outside plain W(A2)",
        "updated_files": UPDATED_FILES,
        "reason": "BT1865 showed O(A2) has order 12, W(A2) has order 6, and -I is outside plain W(A2)",
        "checks": {
            "bt1860_summary_corrected": True,
            "bt1861_summary_corrected": True,
            "bt1864_summary_corrected": True,
            "ledger_corrected": True,
            "execution_summary_corrected": True
        },
        "honest_scope": "Corrects active generated/static summaries. Deep archive files may still contain historical wording."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
