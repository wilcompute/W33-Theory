#!/usr/bin/env python3
"""BT1821: idempotently integrate the BT1820 quartet fibre-law insert.

This helper copies

  analysis/BT1820_quartet_law_paper_insert.tex

to

  paper/sections/sec_bt1820_quartet_fibre_law.tex

and inserts

  \input{sections/sec_bt1820_quartet_fibre_law}

exactly once into paper/w33_preprint.tex.  It is intentionally narrow and safe:
no duplicate inputs, no global rewrite beyond the insertion marker/fallback.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT1820_quartet_law_paper_insert.tex"
DST = ROOT / "paper" / "sections" / "sec_bt1820_quartet_fibre_law.tex"
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
INPUT_LINE = r"\input{sections/sec_bt1820_quartet_fibre_law}"
ANCHORS = [
    r"\input{sections/sec_bt619_endpoint_factorial_trace_law}",
    r"\input{sections/sec_bt618_physical_propagator_normal_form}",
    r"\input{sections/sec_bt613_folded_hashimoto_hodge_flow}",
]


def main() -> int:
    if not SRC.exists():
        raise FileNotFoundError(SRC)
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(SRC.read_text())

    if not PREPRINT.exists():
        print(f"copied {SRC.relative_to(ROOT)} -> {DST.relative_to(ROOT)}; preprint missing")
        return 0
    text = PREPRINT.read_text()
    if INPUT_LINE in text:
        print(f"already integrated: {INPUT_LINE}")
        return 0
    for anchor in ANCHORS:
        if anchor in text:
            text = text.replace(anchor, anchor + "\n" + INPUT_LINE, 1)
            PREPRINT.write_text(text)
            print(f"inserted after {anchor}")
            return 0
    marker = r"\begin{document}"
    if marker in text:
        text = text.replace(marker, marker + "\n" + INPUT_LINE, 1)
        PREPRINT.write_text(text)
        print("inserted after begin{document} fallback")
        return 0
    raise RuntimeError("could not find insertion anchor or fallback marker")


if __name__ == "__main__":
    raise SystemExit(main())
