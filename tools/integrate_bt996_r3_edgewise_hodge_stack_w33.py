#!/usr/bin/env python3
"""Idempotently insert BT996 R3 edgewise Hodge stack into w33_paper.tex."""
from __future__ import annotations

from pathlib import Path

TARGET = Path("w33_paper.tex")
INSERT = Path("paper/BT996_r3_edgewise_hodge_stack_insert.tex")
MARKER = "% BT996_R3_EDGEWISE_HODGE_STACK_INSERT"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    if MARKER in text:
        print("BT996 insert already present")
        return
    insert = INSERT.read_text(encoding="utf-8")
    needle = "\\end{document}"
    if needle not in text:
        raise SystemExit("Could not find end{document}")
    TARGET.write_text(text.replace(needle, f"\n{MARKER}\n{insert}\n\n{needle}", 1), encoding="utf-8")
    print("Inserted BT996 R3 edgewise Hodge stack into w33_paper.tex")


if __name__ == "__main__":
    main()
