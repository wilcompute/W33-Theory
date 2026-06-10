#!/usr/bin/env python3
"""Integrate the BT716 selector-rank note into the paper notes folder.

This helper is intentionally conservative.  It copies the markdown paper insert
into paper/sections and records the exact target path.  The main TeX preprint can
then either input a TeX conversion later or cite this section note directly.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT716_selector_rank_filter_paper_insert.md"
DST = ROOT / "paper" / "sections" / "sec_bt716_selector_rank_filter.md"


def main() -> None:
    DST.parent.mkdir(parents=True, exist_ok=True)
    text = SRC.read_text(encoding="utf-8")
    if DST.exists() and DST.read_text(encoding="utf-8") == text:
        print(f"unchanged: {DST}")
    else:
        DST.write_text(text, encoding="utf-8")
        print(f"wrote: {DST}")


if __name__ == "__main__":
    main()
