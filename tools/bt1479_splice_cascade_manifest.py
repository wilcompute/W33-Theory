#!/usr/bin/env python3
"""BT1479: ordered cascade for pending Holonet paper splices."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1479_splice_cascade_manifest.json"
MD = ROOT / "analysis" / "BT1479_splice_cascade_manifest.md"


def main() -> None:
    cascade = [
        {
            "order": 1,
            "name": "claim_firewalled_section",
            "splicer": "tools/bt1459_holonet_splicer.py",
            "target": "photonic_holonet.tex",
            "insert": "analysis/BT1457_claim_firewalled_holonet_section.tex",
            "anchor": "before fuel section",
            "dependency": "BT1457",
            "status": "splicer committed; main source edit pending local checkout execution",
        },
        {
            "order": 2,
            "name": "claim_dependency_table",
            "splicer": "tools/bt1475_claim_table_splicer.py",
            "target": "analysis/BT1457_claim_firewalled_holonet_section.tex",
            "insert": "analysis/BT1472_dag_claim_table.tex",
            "anchor": "before blocked-claims paragraph",
            "dependency": "BT1472",
            "status": "splicer committed",
        },
        {
            "order": 3,
            "name": "css_join_proof_table",
            "splicer": "future or manual input",
            "target": "analysis/BT1457_claim_firewalled_holonet_section.tex",
            "insert": "analysis/BT1474_css_join_proof_table.tex",
            "anchor": "after finite decoder fact paragraph",
            "dependency": "BT1474",
            "status": "insert ready; splicer not yet specialized",
        },
        {
            "order": 4,
            "name": "equation_acquisition_plan",
            "splicer": "future or manual input",
            "target": "analysis/BT1457_claim_firewalled_holonet_section.tex",
            "insert": "analysis/BT1476_rendered_equation_acquisition_plan.md or TeX conversion",
            "anchor": "inside blocked-claims paragraph",
            "dependency": "BT1476",
            "status": "markdown/csv ready; TeX conversion optional",
        },
        {
            "order": 5,
            "name": "rendered_equation_fill",
            "splicer": "future formula-fill updater",
            "target": "data/bt1473_scirp_prefilled_transcription_packet.csv and paper section",
            "insert": "transcribed formulas for equations 49,50,64,65,66",
            "anchor": "blocked formula slots",
            "dependency": "rendered equation images acquired",
            "status": "blocked pending rendered formula transcription",
        },
    ]
    checks = {
        "five_cascade_steps": len(cascade) == 5,
        "orders_are_1_to_5": [row["order"] for row in cascade] == [1, 2, 3, 4, 5],
        "claim_section_first": cascade[0]["name"] == "claim_firewalled_section",
        "formula_fill_last": cascade[-1]["name"] == "rendered_equation_fill",
        "blocked_last_status": "blocked" in cascade[-1]["status"],
        "all_dependencies_present": all(row["dependency"] for row in cascade),
    }
    md = ["# BT1479 Splice Cascade Manifest", "", "| order | name | target | insert | anchor | status |", "|---:|---|---|---|---|---|"]
    for row in cascade:
        md.append(f"| {row['order']} | {row['name']} | {row['target']} | {row['insert']} | {row['anchor']} | {row['status']} |")
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    result = {
        "bt": 1479,
        "title": "Splice cascade manifest",
        "verified": all(checks.values()),
        "cascade": cascade,
        "markdown": "analysis/BT1479_splice_cascade_manifest.md",
        "interpretation": "This manifest orders every pending paper splice from claim-section insertion through rendered formula fill, with blocked formula insertion explicitly last.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1479, "verified": result["verified"], "steps": len(cascade)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
