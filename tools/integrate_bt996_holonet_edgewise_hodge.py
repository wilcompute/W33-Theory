#!/usr/bin/env python3
"""Idempotently insert BT996 edgewise Hodge pointer into photonic_holonet.tex."""
from __future__ import annotations

from pathlib import Path

TARGET = Path("photonic_holonet.tex")
INSERT = Path("paper/BT996_holonet_edgewise_hodge_pointer.tex")
MARKER = "% BT996_HOLONET_EDGEWISE_HODGE_POINTER"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    if MARKER in text:
        print("BT996 Holonet pointer already present")
        return
    insert = INSERT.read_text(encoding="utf-8")
    needle = "\\end{document}"
    if needle not in text:
        raise SystemExit("Could not find end{document}")
    TARGET.write_text(text.replace(needle, f"\n{MARKER}\n{insert}\n\n{needle}", 1), encoding="utf-8")
    print("Inserted BT996 edgewise Hodge pointer into photonic_holonet.tex")


if __name__ == "__main__":
    main()
