#!/usr/bin/env python3
"""BT1473: prefill Otto transcription packet with visible SCIRP prose."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data" / "bt1473_scirp_prefilled_transcription_packet.json"
OUT_CSV = ROOT / "data" / "bt1473_scirp_prefilled_transcription_packet.csv"
OUT_MD = ROOT / "analysis" / "BT1473_scirp_prefilled_transcription_packet.md"


def main() -> None:
    rows = [
        {
            "eq": 49,
            "visible_prose": "anomalous part of the gyromagnetic factor Delta g_e was given by a simple golden mean representation with sufficient accuracy",
            "line_anchor": "SCIRP lines 281-283",
            "formula_raw": "",
            "parser_expr": "",
            "expected_variables": "phi, Delta_g, a_e, possible denominator 24",
            "target_class": "delta_g or a_e",
            "claim_tier": "blocked_pending_transcription",
        },
        {
            "eq": 50,
            "visible_prose": "a series expansion yields a value more accurate up to the tenth decimal place",
            "line_anchor": "SCIRP lines 285-287",
            "formula_raw": "",
            "parser_expr": "",
            "expected_variables": "series index, phi powers, Delta_g, a_e",
            "target_class": "delta_g or a_e",
            "claim_tier": "blocked_pending_transcription",
        },
        {
            "eq": 64,
            "visible_prose": "icosahedron-based numerical interpretation combining equation 44, the icosahedron equation or golden quartic polynomial, and circumsphere radius",
            "line_anchor": "SCIRP lines 370-372",
            "formula_raw": "",
            "parser_expr": "",
            "expected_variables": "icosahedron radius, quartic coefficient/root, Delta_g",
            "target_class": "delta_g or structural",
            "claim_tier": "blocked_pending_transcription",
        },
        {
            "eq": 65,
            "visible_prose": "power of the ratio of 12 slings to 13 half-turns gives another numerical relation for the anomalous part",
            "line_anchor": "SCIRP lines 374-377",
            "formula_raw": "",
            "parser_expr": "",
            "expected_variables": "12, 13, exponent, Delta_g, ratio_12_13",
            "target_class": "ratio_12_13 or delta_g",
            "claim_tier": "blocked_pending_transcription",
        },
        {
            "eq": 66,
            "visible_prose": "modified Schwinger alpha/pi approximation from the Moebius stripe charge calculation, modified for the Moebius ball structure",
            "line_anchor": "SCIRP lines 378-380",
            "formula_raw": "",
            "parser_expr": "",
            "expected_variables": "alpha, pi, Schwinger, charge correction, Delta_g",
            "target_class": "Schwinger or delta_g",
            "claim_tier": "blocked_pending_transcription",
        },
    ]
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    md = ["# BT1473 SCIRP-prefilled Otto transcription packet", "", "Formula fields remain blank. Visible prose is prefilled from the accessible SCIRP HTML.", "", "| eq | line anchor | visible prose | expected variables | target class | claim tier |", "|---:|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['eq']} | {r['line_anchor']} | {r['visible_prose']} | {r['expected_variables']} | {r['target_class']} | {r['claim_tier']} |")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    checks = {
        "five_rows": len(rows) == 5,
        "eqs_are_targets": [r["eq"] for r in rows] == [49, 50, 64, 65, 66],
        "all_formulas_blank": all(r["formula_raw"] == "" and r["parser_expr"] == "" for r in rows),
        "all_blocked": all(r["claim_tier"] == "blocked_pending_transcription" for r in rows),
        "eq65_mentions_12_13": "12" in rows[3]["visible_prose"] and "13" in rows[3]["visible_prose"],
        "eq66_mentions_schwinger": "Schwinger" in rows[4]["visible_prose"],
        "csv_written": OUT_CSV.exists(),
        "md_written": OUT_MD.exists(),
    }
    result = {
        "bt": 1473,
        "title": "SCIRP-prefilled transcription packet",
        "verified": all(checks.values()),
        "source_url": "https://www.scirp.org/journal/paperinformation?paperid=117540",
        "csv": "data/bt1473_scirp_prefilled_transcription_packet.csv",
        "markdown": "analysis/BT1473_scirp_prefilled_transcription_packet.md",
        "rows": rows,
        "checks": checks,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1473, "verified": result["verified"], "rows": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
