#!/usr/bin/env python3
"""BT942 paper patch integrator.

Idempotently inserts the BT942 E8 selector appendix into W36_PAPER.tex before
\end{document}.  The inserted source is maintained separately at
paper/BT942_e8_selector_appendix.tex.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "W36_PAPER.tex"
APPENDIX = ROOT / "paper/BT942_e8_selector_appendix.tex"
MARKER = "% BEGIN BT942 E8 SELECTOR APPENDIX"
END = "% END BT942 E8 SELECTOR APPENDIX"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    appendix = APPENDIX.read_text(encoding="utf-8")
    block = f"\n\n{MARKER}\n{appendix}\n{END}\n"
    if MARKER in text:
        print("BT942 appendix already integrated")
        return
    if "\\end{document}" not in text:
        raise SystemExit("missing end{document} anchor")
    text = text.replace("\\end{document}", block + "\n\\end{document}", 1)
    TARGET.write_text(text, encoding="utf-8")
    print("BT942 appendix integrated into W36_PAPER.tex")

if __name__ == "__main__":
    main()
