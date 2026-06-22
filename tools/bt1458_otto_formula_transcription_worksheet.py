#!/usr/bin/env python3
"""BT1458: manual worksheet for Otto equations 49, 50, 64, 65, 66."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data" / "bt1458_otto_formula_transcription_worksheet.json"
OUT_CSV = ROOT / "data" / "bt1458_otto_formula_transcription_worksheet.csv"


def main() -> None:
    rows = [
        {
            "equation": 49,
            "section": "Gyromagnetic correction factor",
            "nearby_prose": "simple golden-mean representation for anomalous electron g-factor",
            "expected_variables": "phi, alpha, Delta_g or a_e",
            "transcribed_formula": "",
            "audit_expression": "evaluate formula, compare to measured g/2 and BT1438 residual ledger",
            "status": "awaiting_rendered_formula",
        },
        {
            "equation": 50,
            "section": "Gyromagnetic correction factor",
            "nearby_prose": "series expansion claimed accurate to tenth decimal place",
            "expected_variables": "series index, phi powers, alpha or Delta_g",
            "transcribed_formula": "",
            "audit_expression": "evaluate series truncations and decimal residuals",
            "status": "awaiting_rendered_formula",
        },
        {
            "equation": 64,
            "section": "Quantum vortex structure",
            "nearby_prose": "icosahedron, golden quartic, circumsphere radius, anomalous part",
            "expected_variables": "icosahedron radius, golden quartic root, Delta_g",
            "transcribed_formula": "",
            "audit_expression": "check independence from fitted g value and compare to BT1454 coefficient bridge",
            "status": "awaiting_rendered_formula",
        },
        {
            "equation": 65,
            "section": "Quantum vortex structure",
            "nearby_prose": "power of ratio of 12 slings to 13 half-turns",
            "expected_variables": "12, 13, exponent, Delta_g or alpha/pi",
            "transcribed_formula": "",
            "audit_expression": "compare 12/13 expression to BT1448 closure map and BT1454 active/guard arithmetic",
            "status": "awaiting_rendered_formula",
        },
        {
            "equation": 66,
            "section": "Quantum vortex structure",
            "nearby_prose": "modified Schwinger alpha/pi approximation from Moebius calculation",
            "expected_variables": "alpha, pi, charge correction, Delta_g",
            "transcribed_formula": "",
            "audit_expression": "compare to Schwinger alpha/pi and Fan/Gabrielse measured g/2 anchor",
            "status": "awaiting_rendered_formula",
        },
    ]
    checks = {
        "five_rows": len(rows) == 5,
        "targets_are_49_50_64_65_66": [r["equation"] for r in rows] == [49, 50, 64, 65, 66],
        "all_have_expected_variables": all(r["expected_variables"] for r in rows),
        "all_have_audit_expression": all(r["audit_expression"] for r in rows),
        "all_status_awaiting": all(r["status"] == "awaiting_rendered_formula" for r in rows),
        "eq65_has_12_13": "12" in rows[3]["expected_variables"] and "13" in rows[3]["expected_variables"],
    }
    result = {
        "bt": 1458,
        "title": "Otto formula transcription worksheet",
        "verified": all(checks.values()),
        "worksheet_csv": "data/bt1458_otto_formula_transcription_worksheet.csv",
        "rows": rows,
        "usage": "Fill transcribed_formula from rendered PDF/equation images, then run formula residual audit against the listed audit_expression fields.",
        "checks": checks,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"bt": 1458, "verified": result["verified"], "rows": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
