#!/usr/bin/env python3
"""Integrate the conservative BT1136 holonet pointer.

This deliberately does not promote BT1134 into a new architecture layer.  It
adds a short inherited-physics paragraph after the three-residual itemization in
photonic_holonet.tex.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "photonic_holonet.tex"
INSERT = ROOT / "analysis" / "BT1136_holonet_product_heat_pointer_insert.tex"
SENTINEL = "Inherited K3 product coefficient split"
MARKER = "\\end{itemize}\nNone of the three is a gap in the machine's \\emph{operation}"
REPLACEMENT = "\\end{itemize}\n\n{insert}\nNone of the three is a gap in the machine's \\emph{{operation}}"


def main() -> int:
    paper = PAPER.read_text(encoding="utf-8")
    insert = INSERT.read_text(encoding="utf-8").strip() + "\n\n"
    if SENTINEL in paper:
        print("BT1136 already integrated into photonic_holonet.tex")
        return 0
    if MARKER not in paper:
        raise SystemExit(f"marker not found: {MARKER}")
    paper = paper.replace(MARKER, REPLACEMENT.format(insert=insert), 1)
    PAPER.write_text(paper, encoding="utf-8")
    print("Integrated BT1136 into photonic_holonet.tex after residual list")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
