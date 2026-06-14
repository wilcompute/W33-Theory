#!/usr/bin/env python3
"""Idempotently insert BT990 R3 fat-tower update into w33_paper.tex."""
from __future__ import annotations

from pathlib import Path

TARGET = Path("w33_paper.tex")
INSERT = Path("paper/BT990_r3_fat_tower_insert.tex")
MARKER = "% BT990_R3_FAT_TOWER_INSERT"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    if MARKER in text:
        print("BT990 R3 fat-tower insert already present")
        return
    insert = INSERT.read_text(encoding="utf-8")
    needle = "\\end{document}"
    if needle not in text:
        raise SystemExit("Could not find end{document}")
    text = text.replace(needle, f"\n{MARKER}\n{insert}\n\n{needle}", 1)
    TARGET.write_text(text, encoding="utf-8")
    print("Inserted BT990 R3 fat-tower update into w33_paper.tex")


if __name__ == "__main__":
    main()
