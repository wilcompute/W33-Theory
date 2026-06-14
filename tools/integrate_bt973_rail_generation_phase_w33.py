#!/usr/bin/env python3
"""Integrate BT973 rail generation/phase theorem into w33_paper.tex."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "w33_paper.tex"
INSERT = ROOT / "paper/BT973_rail_generation_phase_theorem_insert.tex"
MARKER = "% BEGIN BT973 RAIL GENERATION PHASE THEOREM"
END = "% END BT973 RAIL GENERATION PHASE THEOREM"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    insert = INSERT.read_text(encoding="utf-8")
    block = f"\n\n{MARKER}\n{insert}\n{END}\n"
    if MARKER in text:
        print("BT973 rail generation/phase theorem already integrated")
        return
    anchor = "\\end{document}"
    if anchor not in text:
        raise SystemExit("missing \\end{document} anchor")
    TARGET.write_text(text.replace(anchor, block + "\n" + anchor, 1), encoding="utf-8")
    print("BT973 rail generation/phase theorem integrated")

if __name__ == "__main__":
    main()
