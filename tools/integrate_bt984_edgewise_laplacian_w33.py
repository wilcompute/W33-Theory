#!/usr/bin/env python3
"""Idempotently insert BT984 fat-tower spectral check into w33_paper.tex."""
from __future__ import annotations

from pathlib import Path

TARGET = Path("w33_paper.tex")
INSERT = Path("paper/BT984_edgewise_laplacian_insert.tex")
MARKER = "% BT984_EDGEWISE_LAPLACIAN_INSERT"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    if MARKER in text:
        print("BT984 insert already present")
        return
    insert = INSERT.read_text(encoding="utf-8")
    needle = "\\end{remark}\n"
    idx = text.rfind(needle)
    if idx < 0:
        raise SystemExit("Could not find final remark boundary for BT984 insert")
    idx += len(needle)
    patched = text[:idx] + "\n" + MARKER + "\n" + insert + "\n" + text[idx:]
    TARGET.write_text(patched, encoding="utf-8")
    print("Inserted BT984 fat-tower spectral check into w33_paper.tex")


if __name__ == "__main__":
    main()
