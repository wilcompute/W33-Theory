#!/usr/bin/env python3
"""BT1512: template to fill after running the BT1509 checkout gate."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data" / "bt1512_checkout_execution_report_template.json"
OUT_MD = ROOT / "analysis" / "BT1512_checkout_execution_report_template.md"

SECTIONS = [
    "splicer_diff_summary",
    "artifact_regeneration_results",
    "json_validation_results",
    "pdf_rebuild_result",
    "visual_page_checks",
    "pytest_release_lock_result",
    "focused_bridge_test_result",
    "dirty_file_list",
    "honesty_notes",
]


def main() -> None:
    template = {
        "bt": 1512,
        "title": "Checkout execution report template",
        "status": "template_only_not_executed",
        "commands_from": "data/bt1509_release_rebuild_gate_manifest.json",
        "sections": {name: "PENDING_LOCAL_CHECKOUT_RUN" for name in SECTIONS},
        "required_visual_checks": [
            "new insertion neighborhood before fuel section",
            "scheduler/pulse table page",
            "native D4 calibration page",
        ],
        "required_tests": [
            "python -m pytest --noconftest -q tests/test_bt1492_bt1494_canonical_pulse_release_lock.py",
            "python scripts/run_focused_bridge_tests.py photonic-qec",
        ],
        "honesty_boundary": "This file is a report template. It does not claim the checkout gate was run.",
    }
    checks = {
        "nine_sections": len(SECTIONS) == 9,
        "all_sections_pending": all(v == "PENDING_LOCAL_CHECKOUT_RUN" for v in template["sections"].values()),
        "visual_checks_three": len(template["required_visual_checks"]) == 3,
        "tests_two": len(template["required_tests"]) == 2,
        "status_template_only": template["status"] == "template_only_not_executed",
    }
    template["verified"] = all(checks.values())
    template["checks"] = checks
    OUT_JSON.write_text(json.dumps(template, indent=2, sort_keys=True) + "\n")
    lines = ["# BT1512 Checkout Execution Report Template", "", "Status: template only; not executed here.", ""]
    for section in SECTIONS:
        lines.extend([f"## {section}", "", "PENDING_LOCAL_CHECKOUT_RUN", ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"bt": 1512, "verified": template["verified"], "sections": len(SECTIONS)}, indent=2))
    if not template["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
