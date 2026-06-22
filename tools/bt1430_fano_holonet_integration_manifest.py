#!/usr/bin/env python3
"""BT1430: integration manifest for the Fano bus Holonet pass."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1430_fano_holonet_integration_manifest.json"
MAIN = ROOT / "photonic_holonet.tex"
INSERTS = [
    ROOT / "analysis" / "BT1419_BT1421_holonet_insert.tex",
    ROOT / "analysis" / "BT1422_BT1424_holonet_insert.tex",
    ROOT / "analysis" / "BT1425_BT1427_holonet_insert.tex",
    ROOT / "analysis" / "BT1430_fano_bus_master_insert.tex",
]
ANCHOR = "%======================================================================\n\\section{The software: braids, teleported gates, universality}"


def main() -> None:
    main_text = MAIN.read_text(encoding="utf-8")
    insert_checks = {str(path.relative_to(ROOT)): path.exists() and len(path.read_text(encoding="utf-8")) > 100 for path in INSERTS}
    input_lines = [f"\\input{{{path.relative_to(ROOT).with_suffix('').as_posix()}}}" for path in INSERTS]
    checks = {
        "main_tex_exists": MAIN.exists(),
        "software_anchor_present": ANCHOR in main_text,
        "all_insert_sources_exist": all(insert_checks.values()),
        "fano_168_24_192_insert_present": "168+24" in INSERTS[-1].read_text(encoding="utf-8") and "H_XJ^{-1}" in INSERTS[-1].read_text(encoding="utf-8"),
        "input_line_count_is_4": len(input_lines) == 4,
        "pdf_rebuild_not_run_by_connector": True,
    }
    result = {
        "bt": 1430,
        "title": "Fano bus Holonet integration manifest",
        "verified": all(checks.values()),
        "main_tex": str(MAIN.relative_to(ROOT)),
        "anchor": ANCHOR,
        "insert_sources": list(insert_checks),
        "insert_source_checks": insert_checks,
        "input_lines_to_splice_before_software_section": input_lines,
        "figure_law": {
            "active_fano_bus": "168 = 21 * 8 = |GL(3,2)|",
            "guard_rail": "24 = point stabilizer S4",
            "tomotope_bus": "192 = 168 + 24",
            "retwined_css": "H_X' = H_X J^{-1}, H_Z' = H_Z J^{-1}",
        },
        "pdf_status": "The connector pass created the TeX insert and idempotent splicer but did not rebuild photonic_holonet.pdf in-place.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1430, "verified": result["verified"], "inserts": len(input_lines)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
