#!/usr/bin/env python3
"""Integrate BT967 selector rail pointer into photonic_holonet.tex."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "photonic_holonet.tex"
INSERT = ROOT / "paper/BT967_holonet_selector_rail_pointer.tex"
MARKER = "% BEGIN BT967 SELECTOR RAIL POINTER"
END = "% END BT967 SELECTOR RAIL POINTER"
ANCHOR = "\\end{abstract}"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    insert = INSERT.read_text(encoding="utf-8")
    block = f"\n\n{MARKER}\n{insert}\n{END}\n"
    if MARKER in text:
        print("BT967 Holonet pointer already integrated")
        return
    if ANCHOR not in text:
        raise SystemExit("missing abstract anchor")
    TARGET.write_text(text.replace(ANCHOR, ANCHOR + block, 1), encoding="utf-8")
    print("BT967 Holonet pointer integrated")

if __name__ == "__main__":
    main()
