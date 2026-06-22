#!/usr/bin/env python3
"""BT1441: equation-image transcription gate for Otto's paper.

SCIRP exposes the surrounding prose for equations (49), (50), (64), (65), and
(66), but not the equation bodies as machine-readable text.  This verifier
creates a strict import ledger: equations must be transcribed before their
numerical/physics claims can be credited in W33.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1441_otto_equation_transcription_gate.json"


def main() -> None:
    equation_slots = [
        {
            "equation": 49,
            "visible_context": "simple golden-mean representation of the anomalous part of the electron gyromagnetic factor",
            "import_status": "blocked_until_transcribed",
            "required_audit": "compute Delta g and compare to experimental and QED anchors",
        },
        {
            "equation": 50,
            "visible_context": "series expansion more accurate up to the tenth decimal place",
            "import_status": "blocked_until_transcribed",
            "required_audit": "compute Delta g and compare decimal-by-decimal residual",
        },
        {
            "equation": 64,
            "visible_context": "icosahedron-based numerical interpretation of Delta g using equation 44 and circumsphere radius",
            "import_status": "blocked_until_transcribed",
            "required_audit": "check whether the icosahedral formula is independent or post-hoc",
        },
        {
            "equation": 65,
            "visible_context": "power of the ratio 12 slings to 13 half-turns",
            "import_status": "blocked_until_transcribed",
            "required_audit": "test the 12/13 formula against BT1439 active/guard bus lift",
        },
        {
            "equation": 66,
            "visible_context": "modified Schwinger alpha/pi interpretation from Moebius-stripe charge calculation",
            "import_status": "blocked_until_transcribed",
            "required_audit": "compare modified alpha/pi value to QED and measurement",
        },
    ]
    checks = {
        "five_equation_slots": len(equation_slots) == 5,
        "all_slots_blocked": all(slot["import_status"] == "blocked_until_transcribed" for slot in equation_slots),
        "contains_gminus2_slots": {49, 50, 64, 65, 66} == {slot["equation"] for slot in equation_slots},
        "eq65_mentions_12_13": "12 slings to 13 half-turns" in equation_slots[3]["visible_context"],
        "eq66_mentions_schwinger": "Schwinger" in equation_slots[4]["visible_context"],
    }
    result = {
        "bt": 1441,
        "title": "Otto equation transcription gate",
        "verified": all(checks.values()),
        "source": "Hans Hermann Otto, Golden Quartic Polynomial and Moebius-Ball Electron, JAMP 10 (2022), DOI 10.4236/jamp.2022.105124",
        "equation_slots": equation_slots,
        "decision": "Do not score Otto-specific formulas until equations 49, 50, 64, 65, and 66 are transcribed from the rendered paper equations.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1441, "verified": result["verified"], "slots": len(equation_slots)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
