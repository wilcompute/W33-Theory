#!/usr/bin/env python3
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "w33_paper.tex"
INSERT = ROOT / "analysis" / "BT1193_w33_paper_s3_shadow_obstruction_insert.tex"
MARKER = "\\begin{theorem}[The complete spectral action of $W(3,3)$]"
SENTINEL = "\\label{rem:s3-shadow-carrier-obstruction}"
PREREQ = "\\label{rem:correlation-block-s3-route}"
text = PAPER.read_text(encoding="utf-8")
if SENTINEL not in text:
    if PREREQ not in text:
        raise RuntimeError("BT1190 missing")
    ins = INSERT.read_text(encoding="utf-8").strip() + "\n\n"
    PAPER.write_text(text.replace(MARKER, ins + MARKER, 1), encoding="utf-8")
