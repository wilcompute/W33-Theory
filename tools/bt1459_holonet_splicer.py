#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "photonic_holonet.tex"
INSERT = ROOT / "analysis" / "BT1457_claim_firewalled_holonet_section.tex"
OUT = ROOT / "data" / "bt1459_holonet_splicer.json"
INPUT_LINE = "\\input{analysis/BT1457_claim_firewalled_holonet_section}"
MARKER = "% BT1459 claim-firewalled closure bridge"
ANCHOR = "%======================================================================\n\\section[The fuel: matter equals magic]{The fuel: matter $=$ magic}"


def main() -> None:
    text = MAIN.read_text(encoding="utf-8")
    before_count = text.count(INPUT_LINE)
    if before_count == 0:
        if ANCHOR not in text:
            raise RuntimeError("fuel-section anchor not found")
        text = text.replace(ANCHOR, f"\n{MARKER}\n{INPUT_LINE}\n\n" + ANCHOR, 1)
        MAIN.write_text(text, encoding="utf-8")
    after = MAIN.read_text(encoding="utf-8")
    after_count = after.count(INPUT_LINE)
    checks = {
        "insert_file_exists": INSERT.exists(),
        "input_present_exactly_once": after_count == 1,
        "idempotent_before_count_ok": before_count in (0, 1),
        "marker_present": MARKER in after,
    }
    result = {
        "bt": 1459,
        "title": "Holonet splicer",
        "verified": all(checks.values()),
        "main_tex": "photonic_holonet.tex",
        "insert_tex": "analysis/BT1457_claim_firewalled_holonet_section.tex",
        "input_line": INPUT_LINE,
        "before_count": before_count,
        "after_count": after_count,
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1459, "verified": result["verified"], "after_count": after_count}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
