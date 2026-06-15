#!/usr/bin/env python3
"""Integrate BT1134 into the real main paper w33_paper.tex.

This deliberately targets w33_paper.tex, not w33_preprint.tex.
It inserts analysis/BT1134_w33_paper_product_heat_insert.tex immediately before
Theorem "The complete spectral action of W(3,3)".
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "w33_paper.tex"
INSERT = ROOT / "analysis" / "BT1134_w33_paper_product_heat_insert.tex"
MARKER = "\\begin{theorem}[The complete spectral action of $W(3,3)$]"
SENTINEL = "\\label{prop:ricci-flat-product-heat-slot}"


def main() -> int:
    paper = PAPER.read_text(encoding="utf-8")
    insert = INSERT.read_text(encoding="utf-8").strip() + "\n\n"

    if SENTINEL in paper:
        print("BT1134 already integrated into w33_paper.tex")
        return 0
    if MARKER not in paper:
        raise SystemExit(f"marker not found: {MARKER}")

    paper = paper.replace(MARKER, insert + MARKER, 1)
    PAPER.write_text(paper, encoding="utf-8")
    print("Integrated BT1134 into w33_paper.tex before complete spectral action theorem")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
