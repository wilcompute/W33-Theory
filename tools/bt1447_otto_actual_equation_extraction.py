#!/usr/bin/env python3
"""BT1447: actual extraction ledger for Otto equations 49/50/64/65/66.

The accessible SCIRP HTML exposes equation numbers and surrounding prose, but the
formula bodies are rendered/non-textual.  This script records the extraction
state with enough structure for formula-level auditing once a PDF/image pass is
available.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1447_otto_actual_equation_extraction.json"


def main() -> None:
    slots = [
        {
            "equation": 49,
            "chapter": "6. The Gyromagnetic Correction Factor of the Electron",
            "visible_context": "simple golden mean representation of the anomalous part of the electron gyromagnetic factor",
            "html_body_status": "missing_non_textual_render",
            "formula_text": None,
            "audit_after_transcription": "compute Delta g_e and compare with the experimental g/2 anchor and Schwinger baseline",
        },
        {
            "equation": 50,
            "chapter": "6. The Gyromagnetic Correction Factor of the Electron",
            "visible_context": "series expansion yields a value more accurate up to the tenth decimal place",
            "html_body_status": "missing_non_textual_render",
            "formula_text": None,
            "audit_after_transcription": "compare decimal residuals against experiment and against equation 49",
        },
        {
            "equation": 64,
            "chapter": "7. Proposed Quantum Vortex Structure of the Electron",
            "visible_context": "icosahedron-based numerical interpretation combining equation 44, the icosahedron equation, the golden quartic, and circumsphere radius",
            "html_body_status": "missing_non_textual_render",
            "formula_text": None,
            "audit_after_transcription": "test whether the icosahedral relation is independent or a fitted restatement",
        },
        {
            "equation": 65,
            "chapter": "7. Proposed Quantum Vortex Structure of the Electron",
            "visible_context": "power of the ratio of 12 slings to 13 half-turns for the anomalous part",
            "html_body_status": "missing_non_textual_render",
            "formula_text": None,
            "audit_after_transcription": "compare the 12/13 formula with the BT1439 and BT1442 closure-tick lifts",
        },
        {
            "equation": 66,
            "chapter": "7. Proposed Quantum Vortex Structure of the Electron",
            "visible_context": "modified Schwinger alpha/pi approximation from a Moebius-stripe charge calculation adjusted for the Moebius ball",
            "html_body_status": "missing_non_textual_render",
            "formula_text": None,
            "audit_after_transcription": "compare modified alpha/pi to QED one-loop and the experimental anomalous magnetic moment",
        },
    ]
    checks = {
        "all_target_equations_present": {s["equation"] for s in slots} == {49, 50, 64, 65, 66},
        "all_formula_text_missing": all(s["formula_text"] is None for s in slots),
        "all_marked_non_textual": all(s["html_body_status"] == "missing_non_textual_render" for s in slots),
        "eq65_keeps_12_13_context": "12 slings to 13 half-turns" in slots[3]["visible_context"],
        "eq66_keeps_schwinger_context": "Schwinger" in slots[4]["visible_context"],
    }
    result = {
        "bt": 1447,
        "title": "Otto actual equation extraction ledger",
        "verified": all(checks.values()),
        "source_url": "https://www.scirp.org/journal/paperinformation?paperid=117540",
        "extraction_result": "The HTML source exposes equation numbers and prose contexts but not machine-readable equation bodies for equations 49, 50, 64, 65, and 66.",
        "slots": slots,
        "next_required_action": "Use the PDF or rendered equation images to manually transcribe formulas, then replace formula_text nulls and run the formula residual audit.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1447, "verified": result["verified"], "missing_formula_bodies": len(slots)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
