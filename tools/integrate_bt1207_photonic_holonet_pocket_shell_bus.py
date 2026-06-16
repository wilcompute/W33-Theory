#!/usr/bin/env python3
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "photonic_holonet.tex"
INSERT = ROOT / "analysis" / "BT1207_photonic_holonet_pocket_shell_bus_insert.tex"
MARKER = "\\begin{thebibliography}{9}"
SENTINEL = "\\label{thm:nonabelian-pocket-shell-bus}"
text = PAPER.read_text(encoding="utf-8")
if SENTINEL not in text:
    ins = INSERT.read_text(encoding="utf-8").strip() + "\n\n"
    PAPER.write_text(text.replace(MARKER, ins + MARKER, 1), encoding="utf-8")
