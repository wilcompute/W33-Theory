#!/usr/bin/env python3
"""BT1470: compact UI worksheet for manual Otto equation transcription."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data" / "bt1470_formula_transcription_ui_packet.json"
OUT_CSV = ROOT / "data" / "bt1470_formula_transcription_ui_packet.csv"
OUT_MD = ROOT / "analysis" / "BT1470_formula_transcription_ui_packet.md"


def main() -> None:
    rows = [
        {"eq": 49, "source_context": "g-factor section; golden-mean representation", "formula_image_ref": "Otto paper equation (49)", "formula_raw": "", "parser_expr": "", "target_class": "g_over_2 or delta_g or a_e", "residual": "", "claim_tier": "blocked_pending_transcription"},
        {"eq": 50, "source_context": "g-factor section; series expansion", "formula_image_ref": "Otto paper equation (50)", "formula_raw": "", "parser_expr": "", "target_class": "delta_g or a_e", "residual": "", "claim_tier": "blocked_pending_transcription"},
        {"eq": 64, "source_context": "vortex section; icosahedron/quartic radius relation", "formula_image_ref": "Otto paper equation (64)", "formula_raw": "", "parser_expr": "", "target_class": "delta_g or structural", "residual": "", "claim_tier": "blocked_pending_transcription"},
        {"eq": 65, "source_context": "vortex section; 12/13 half-turn ratio", "formula_image_ref": "Otto paper equation (65)", "formula_raw": "", "parser_expr": "", "target_class": "ratio_12_13 or delta_g", "residual": "", "claim_tier": "blocked_pending_transcription"},
        {"eq": 66, "source_context": "vortex section; modified Schwinger alpha/pi", "formula_image_ref": "Otto paper equation (66)", "formula_raw": "", "parser_expr": "", "target_class": "Schwinger or delta_g", "residual": "", "claim_tier": "blocked_pending_transcription"},
    ]
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    md_lines = [
        "# BT1470 Formula Transcription UI Packet",
        "",
        "Fill `formula_raw` from the rendered equation image, then translate it into `parser_expr` using BT1464 aliases.",
        "",
        "Allowed parser aliases: `Phi`, `phi`, `phi5`, `delta_g`, `a_e`, `Schwinger`, `ratio_12_13`, `alpha`, `pi`, `sqrt`.",
        "",
        "| eq | source context | formula image ref | formula_raw | parser_expr | target_class | residual | claim_tier |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        md_lines.append(f"| {r['eq']} | {r['source_context']} | {r['formula_image_ref']} |  |  | {r['target_class']} |  | {r['claim_tier']} |")
    md_lines.extend([
        "",
        "Audit workflow:",
        "1. Fill `formula_raw` exactly from the equation image.",
        "2. Convert to `parser_expr` using BT1464 aliases.",
        "3. Run `python tools/bt1464_formula_parser_upgrade.py` or the residual runner.",
        "4. Promote claim tier only if residual and derivation checks pass.",
    ])
    OUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    checks = {
        "five_rows": len(rows) == 5,
        "targets_are_49_50_64_65_66": [r["eq"] for r in rows] == [49, 50, 64, 65, 66],
        "csv_written": OUT_CSV.exists(),
        "markdown_written": OUT_MD.exists() and "BT1470" in OUT_MD.read_text(encoding="utf-8"),
        "all_blocked_pending_transcription": all(r["claim_tier"] == "blocked_pending_transcription" for r in rows),
        "eq65_mentions_12_13": "12/13" in rows[3]["source_context"] or "12/13" in rows[3]["target_class"],
    }
    result = {
        "bt": 1470,
        "title": "Formula transcription UI packet",
        "verified": all(checks.values()),
        "csv": "data/bt1470_formula_transcription_ui_packet.csv",
        "markdown": "analysis/BT1470_formula_transcription_ui_packet.md",
        "rows": rows,
        "workflow": [
            "fill formula_raw from rendered equation image",
            "translate to parser_expr using BT1464 aliases",
            "run residual parser",
            "promote claim tier only after audit",
        ],
        "checks": checks,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1470, "verified": result["verified"], "rows": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
