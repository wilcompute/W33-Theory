#!/usr/bin/env python3
"""BT1825: validate the BT1820 quartet insert integration.

Run after tools/integrate_bt1820_quartet_insert.py.  This script performs only
read-only checks: source exists, copied section exists, preprint exists, and the
paper input command appears exactly once.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT1820_quartet_law_paper_insert.tex"
DST = ROOT / "paper" / "sections" / "sec_bt1820_quartet_fibre_law.tex"
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
INPUT_LINE = "\\\\input{sections/sec_bt1820_quartet_fibre_law}"


def main() -> int:
    text = PREPRINT.read_text() if PREPRINT.exists() else ""
    result = {
        "source_exists": SRC.exists(),
        "target_section_exists": DST.exists(),
        "preprint_exists": PREPRINT.exists(),
        "input_line_count": text.count(INPUT_LINE),
    }
    result["passes"] = bool(result["source_exists"] and result["target_section_exists"] and result["preprint_exists"] and result["input_line_count"] == 1)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passes"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
