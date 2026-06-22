#!/usr/bin/env python3
"""BT1475: splice the BT1472 claim table into the BT1457 claim-firewalled section."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTION = ROOT / "analysis" / "BT1457_claim_firewalled_holonet_section.tex"
TABLE = ROOT / "analysis" / "BT1472_dag_claim_table.tex"
OUT = ROOT / "data" / "bt1475_claim_table_splicer.json"
INPUT_LINE = r"\input{analysis/BT1472_dag_claim_table}"
MARKER = "% BT1475 claim dependency table"
ANCHOR = r"\paragraph{Blocked claims.}"


def main() -> None:
    text = SECTION.read_text(encoding="utf-8")
    before = text.count(INPUT_LINE)
    anchor_count = text.count(ANCHOR)
    if before == 0:
        if anchor_count != 1:
            raise RuntimeError("blocked-claims anchor must occur exactly once")
        text = text.replace(ANCHOR, f"{MARKER}\n{INPUT_LINE}\n\n" + ANCHOR, 1)
        SECTION.write_text(text, encoding="utf-8")
    after = SECTION.read_text(encoding="utf-8")
    checks = {
        "section_exists": SECTION.exists(),
        "table_exists": TABLE.exists(),
        "anchor_unique_before_splice": anchor_count == 1,
        "input_present_once_after": after.count(INPUT_LINE) == 1,
        "marker_present_after": MARKER in after,
        "idempotent_before_count_ok": before in (0, 1),
    }
    result = {
        "bt": 1475,
        "title": "Claim table splicer",
        "verified": all(checks.values()),
        "section": "analysis/BT1457_claim_firewalled_holonet_section.tex",
        "table": "analysis/BT1472_dag_claim_table.tex",
        "input_line": INPUT_LINE,
        "before_count": before,
        "after_count": after.count(INPUT_LINE),
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1475, "verified": result["verified"], "after_count": result["after_count"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
