#!/usr/bin/env python3
"""Integrate BT1142 a4 convention table into w33_paper.tex."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "w33_paper.tex"
INSERT = ROOT / "analysis" / "BT1142_w33_paper_a4_convention_table_insert.tex"
MARKER = "\\begin{theorem}[The complete spectral action of $W(3,3)$]"
SENTINEL = "\\label{rem:k3-a4-convention-table}"
PREREQ = "\\label{prop:k3-a4-normalized-closure}"


def main() -> int:
    paper = PAPER.read_text(encoding="utf-8")
    insert = INSERT.read_text(encoding="utf-8").strip() + "\n\n"
    if SENTINEL in paper:
        print("BT1142 already present")
        return 0
    if PREREQ not in paper:
        raise RuntimeError("BT1139 label missing")
    if MARKER not in paper:
        raise RuntimeError("complete spectral action marker missing")
    PAPER.write_text(paper.replace(MARKER, insert + MARKER, 1), encoding="utf-8")
    print("BT1142 integrated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
