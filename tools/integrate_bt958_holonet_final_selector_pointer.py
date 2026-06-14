#!/usr/bin/env python3
"""Integrate the BT958 final selector pointer into photonic_holonet.tex."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "photonic_holonet.tex"
INSERT = ROOT / "paper/BT958_holonet_final_selector_pointer.tex"
MARKER = "% BEGIN BT958 FINAL E8 SELECTOR POINTER"
END = "% END BT958 FINAL E8 SELECTOR POINTER"
ANCHOR = "\\end{abstract}"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    insert = INSERT.read_text(encoding="utf-8")
    block = f"\n\n{MARKER}\n{insert}\n{END}\n"
    if MARKER in text:
        print("BT958 final selector pointer already integrated into photonic_holonet.tex")
        return
    if ANCHOR not in text:
        raise SystemExit("missing abstract anchor in photonic_holonet.tex")
    text = text.replace(ANCHOR, ANCHOR + block, 1)
    TARGET.write_text(text, encoding="utf-8")
    print("BT958 final selector pointer integrated into photonic_holonet.tex")

if __name__ == "__main__":
    main()
