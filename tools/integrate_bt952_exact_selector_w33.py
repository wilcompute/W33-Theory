#!/usr/bin/env python3
"""Integrate the BT952 exact E8 selector theorem into w33_paper.tex."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "w33_paper.tex"
INSERT = ROOT / "paper/BT952_exact_e8_selector_theorem_insert.tex"
MARKER = "% BEGIN BT952 EXACT E8 SELECTOR THEOREM"
END = "% END BT952 EXACT E8 SELECTOR THEOREM"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    insert = INSERT.read_text(encoding="utf-8")
    block = f"\n\n{MARKER}\n{insert}\n{END}\n"
    if MARKER in text:
        print("BT952 exact selector theorem already integrated into w33_paper.tex")
        return
    anchor = "\\end{document}"
    if anchor not in text:
        raise SystemExit("missing \\end{document} anchor in w33_paper.tex")
    text = text.replace(anchor, block + "\n" + anchor, 1)
    TARGET.write_text(text, encoding="utf-8")
    print("BT952 exact selector theorem integrated into w33_paper.tex")

if __name__ == "__main__":
    main()
