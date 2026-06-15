#!/usr/bin/env python3
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "w33_paper.tex"
INSERT = ROOT / "analysis" / "BT1186_w33_paper_voltage_chirality_obstruction_insert.tex"
MARKER = "\\begin{theorem}[The complete spectral action of $W(3,3)$]"
SENTINEL = "\\label{rem:voltage-chirality-obstruction}"
PREREQ = "\\label{rem:z2-cover-centralizer96}"

def main():
    text = PAPER.read_text(encoding="utf-8")
    if SENTINEL in text:
        return 0
    if PREREQ not in text:
        raise RuntimeError("BT1183 missing")
    insert = INSERT.read_text(encoding="utf-8").strip() + "\n\n"
    PAPER.write_text(text.replace(MARKER, insert + MARKER, 1), encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
