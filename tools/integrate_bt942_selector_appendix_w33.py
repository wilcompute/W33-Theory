#!/usr/bin/env python3
"""Integrate the BT942 E8 selector appendix into w33_paper.tex.

Routing correction: photonic_holonet.tex is the current main narrative / architecture paper,
while w33_paper.tex is the heavy-math manuscript.  E8/SNF/symplectic-selector
math belongs in w33_paper.tex.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "w33_paper.tex"
APPENDIX = ROOT / "paper/BT942_e8_selector_appendix.tex"
MARKER = "% BEGIN BT942 E8 SELECTOR APPENDIX FOR W33_PAPER"
END = "% END BT942 E8 SELECTOR APPENDIX FOR W33_PAPER"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    appendix = APPENDIX.read_text(encoding="utf-8")
    block = f"\n\n{MARKER}\n{appendix}\n{END}\n"
    if MARKER in text:
        print("BT942 selector appendix already integrated into w33_paper.tex")
        return
    anchor = "\\end{document}"
    if anchor not in text:
        raise SystemExit("missing \\end{document} anchor in w33_paper.tex")
    text = text.replace(anchor, block + "\n" + anchor, 1)
    TARGET.write_text(text, encoding="utf-8")
    print("BT942 selector appendix integrated into w33_paper.tex")

if __name__ == "__main__":
    main()
