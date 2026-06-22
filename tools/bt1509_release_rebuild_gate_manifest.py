#!/usr/bin/env python3
"""BT1509: exact checkout command sequence for splice, PDF rebuild, and visual verification.

This file deliberately does not claim the commands were run.  It records the gate
sequence that must be executed in a local checkout after BT1506.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1509_release_rebuild_gate_manifest.json"
MD = ROOT / "analysis" / "BT1509_release_rebuild_gate_manifest.md"

COMMANDS = [
    "python tools/bt1506_release_lock_splicer.py",
    "python tools/bt1504_skew_line_orbit_map.py",
    "python tools/bt1505_native_d4_generator_route_traces.py",
    "python tools/bt1508_route_trace_css_syndrome_replay.py",
    "python -m json.tool data/bt1504_skew_line_orbit_map.json > /tmp/bt1504.json",
    "python -m json.tool data/bt1508_route_trace_css_syndrome_replay.json > /tmp/bt1508.json",
    "latexmk -pdf -interaction=nonstopmode photonic_holonet.tex",
    "python -m pytest --noconftest -q tests/test_bt1492_bt1494_canonical_pulse_release_lock.py",
    "python scripts/run_focused_bridge_tests.py photonic-qec",
]

VISUAL_CHECKS = [
    {"target": "photonic_holonet.pdf", "pages": "new insertion neighborhood before fuel section", "check": "BT1495-BT1503 inserts render without overfull table rupture"},
    {"target": "photonic_holonet.pdf", "pages": "scheduler/pulse table page", "check": "BT1500 count table remains readable"},
    {"target": "photonic_holonet.pdf", "pages": "native D4 calibration page", "check": "BT1502 ledger renders as finite calibration, not noise model"},
]


def main() -> None:
    checks = {
        "starts_with_splicer": COMMANDS[0] == "python tools/bt1506_release_lock_splicer.py",
        "includes_bt1504_regen": any("bt1504" in cmd for cmd in COMMANDS),
        "includes_bt1508_regen": any("bt1508" in cmd for cmd in COMMANDS),
        "includes_pdf_rebuild": any("latexmk" in cmd and "photonic_holonet.tex" in cmd for cmd in COMMANDS),
        "includes_release_lock_test": any("test_bt1492_bt1494" in cmd for cmd in COMMANDS),
        "includes_photonic_qec_focused_tests": any("photonic-qec" in cmd for cmd in COMMANDS),
        "visual_checks_three": len(VISUAL_CHECKS) == 3,
        "no_claim_run_here": True,
    }
    result = {
        "bt": 1509,
        "title": "Release rebuild gate manifest",
        "verified": all(checks.values()),
        "status": "command_sequence_prepared_not_executed_here",
        "commands": COMMANDS,
        "visual_checks": VISUAL_CHECKS,
        "interpretation": "This manifest is the exact checkout gate for running the BT1506 splicer, regenerating key artifacts, rebuilding photonic_holonet.pdf, and visually checking target pages.",
        "honesty_boundary": "No PDF rebuild or pytest run is claimed by this connector commit. These commands must be run in checkout.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    md = ["# BT1509 Release Rebuild Gate Manifest", "", "Status: command sequence prepared, not executed here.", "", "## Commands", ""]
    for i, cmd in enumerate(COMMANDS, 1):
        md.append(f"{i}. `{cmd}`")
    md.extend(["", "## Visual checks", ""])
    for row in VISUAL_CHECKS:
        md.append(f"- `{row['target']}` pages `{row['pages']}`: {row['check']}")
    md.append("\nHonesty boundary: this manifest does not claim the PDF was rebuilt or tests were run in this connector turn.\n")
    MD.write_text("\n".join(md), encoding="utf-8")
    print(json.dumps({"bt": 1509, "verified": result["verified"], "commands": len(COMMANDS)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
