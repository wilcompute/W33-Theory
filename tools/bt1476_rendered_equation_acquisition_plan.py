#!/usr/bin/env python3
"""BT1476: deterministic acquisition checklist for Otto rendered equations."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data" / "bt1476_rendered_equation_acquisition_plan.json"
OUT_CSV = ROOT / "data" / "bt1476_rendered_equation_acquisition_plan.csv"
OUT_MD = ROOT / "analysis" / "BT1476_rendered_equation_acquisition_plan.md"


def main() -> None:
    rows = [
        {"eq": 49, "section": "gyromagnetic correction factor", "visible_anchor": "golden-mean anomalous factor prose", "image_target": "equation image immediately after anchor prose", "transcription_slot": "formula_raw", "parser_slot": "parser_expr", "residual_targets": "delta_g,a_e,g_over_2", "claim_gate": "blocked until formula image transcribed"},
        {"eq": 50, "section": "gyromagnetic correction factor", "visible_anchor": "series expansion accurate to tenth decimal prose", "image_target": "equation image immediately after series prose", "transcription_slot": "formula_raw", "parser_slot": "parser_expr", "residual_targets": "delta_g,a_e", "claim_gate": "blocked until formula image transcribed"},
        {"eq": 64, "section": "quantum vortex structure", "visible_anchor": "icosahedron/golden-quartic/circumsphere prose", "image_target": "equation image for icosahedral numerical interpretation", "transcription_slot": "formula_raw", "parser_slot": "parser_expr", "residual_targets": "delta_g,structural", "claim_gate": "blocked until formula image transcribed"},
        {"eq": 65, "section": "quantum vortex structure", "visible_anchor": "12 slings to 13 half-turns prose", "image_target": "equation image involving 12/13 ratio and exponent", "transcription_slot": "formula_raw", "parser_slot": "parser_expr", "residual_targets": "ratio_12_13,delta_g", "claim_gate": "blocked until formula image transcribed"},
        {"eq": 66, "section": "quantum vortex structure", "visible_anchor": "modified Schwinger alpha/pi prose", "image_target": "equation image for modified Schwinger relation", "transcription_slot": "formula_raw", "parser_slot": "parser_expr", "residual_targets": "Schwinger,delta_g", "claim_gate": "blocked until formula image transcribed"},
    ]
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    md = ["# BT1476 Rendered Equation Acquisition Plan", "", "This is the deterministic checklist for acquiring Otto equations (49), (50), (64), (65), and (66).", "", "| eq | section | visible anchor | image target | residual targets | claim gate |", "|---:|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['eq']} | {r['section']} | {r['visible_anchor']} | {r['image_target']} | {r['residual_targets']} | {r['claim_gate']} |")
    md.extend(["", "Workflow:", "1. Acquire rendered equation image from PDF or page screenshot.", "2. Transcribe into `formula_raw` exactly.", "3. Convert to `parser_expr` using BT1464 aliases.", "4. Run BT1461/BT1464 residual audit.", "5. Promote only if the BT1469 claim DAG allows the dependency edge."])
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    checks = {
        "five_rows": len(rows) == 5,
        "target_equations": [r["eq"] for r in rows] == [49, 50, 64, 65, 66],
        "eq65_targets_ratio": "ratio_12_13" in rows[3]["residual_targets"],
        "eq66_targets_schwinger": "Schwinger" in rows[4]["residual_targets"],
        "all_claims_blocked": all("blocked" in r["claim_gate"] for r in rows),
        "csv_written": OUT_CSV.exists(),
        "md_written": OUT_MD.exists(),
    }
    result = {
        "bt": 1476,
        "title": "Rendered-equation acquisition plan",
        "verified": all(checks.values()),
        "csv": "data/bt1476_rendered_equation_acquisition_plan.csv",
        "markdown": "analysis/BT1476_rendered_equation_acquisition_plan.md",
        "rows": rows,
        "workflow": ["acquire rendered image", "transcribe formula_raw", "convert parser_expr", "run residual audit", "promote only through DAG"],
        "checks": checks,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1476, "verified": result["verified"], "rows": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
