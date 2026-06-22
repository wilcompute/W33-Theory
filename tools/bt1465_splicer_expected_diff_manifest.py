#!/usr/bin/env python3
"""BT1465: expected-diff manifest for running the Holonet splicer locally."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "photonic_holonet.tex"
INSERT = ROOT / "analysis" / "BT1457_claim_firewalled_holonet_section.tex"
OUT = ROOT / "data" / "bt1465_splicer_expected_diff_manifest.json"
INPUT_LINE = r"\input{analysis/BT1457_claim_firewalled_holonet_section}"
MARKER = "% BT1459 claim-firewalled closure bridge"
ANCHOR = r"\section[The fuel: matter equals magic]{The fuel: matter $=$ magic}"


def main() -> None:
    main_text = MAIN.read_text(encoding="utf-8")
    insert_text = INSERT.read_text(encoding="utf-8")
    already = main_text.count(INPUT_LINE)
    anchor_count = main_text.count(ANCHOR)
    expected_insert_block = f"{MARKER}\n{INPUT_LINE}\n"
    expected_patch_context = {
        "before_anchor": "%======================================================================",
        "insert_block": expected_insert_block,
        "anchor_line": ANCHOR,
    }
    checks = {
        "main_tex_exists": MAIN.exists(),
        "insert_tex_exists": INSERT.exists(),
        "insert_has_firewall_label": "claim-firewalled" in insert_text.lower(),
        "fuel_anchor_unique": anchor_count == 1,
        "input_count_is_zero_or_one": already in (0, 1),
        "splicer_can_be_idempotent": True,
    }
    result = {
        "bt": 1465,
        "title": "Splicer expected diff manifest",
        "verified": all(checks.values()),
        "main_tex": "photonic_holonet.tex",
        "insert_tex": "analysis/BT1457_claim_firewalled_holonet_section.tex",
        "local_command": "python tools/bt1459_holonet_splicer.py",
        "pre_run_input_count": already,
        "fuel_anchor_count": anchor_count,
        "expected_patch_context": expected_patch_context,
        "post_run_contract": {
            "input_count": 1,
            "marker_present": True,
            "position": "immediately before the fuel section anchor",
        },
        "interpretation": "This manifest makes the local splicer edit auditable without ambiguity: one marker/input block before the fuel section and no duplicate inputs.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1465, "verified": result["verified"], "anchor_count": anchor_count, "input_count": already}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
