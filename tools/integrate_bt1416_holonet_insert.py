#!/usr/bin/env python3
"""Idempotently splice the BT1416 even-Q4 guard insert into photonic_holonet.tex."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "photonic_holonet.tex"
INSERT = ROOT / "analysis" / "BT1416_even_q4_demicube_guard_holonet_insert.tex"
MARKER = "% BT1416 even-Q4 demicube guard ledger"
INPUT = "\\input{analysis/BT1416_even_q4_demicube_guard_holonet_insert}"
ANCHOR = "%======================================================================\n\\section{The software: braids, teleported gates, universality}"


def main() -> None:
    text = MAIN.read_text()
    if INPUT in text:
        print("BT1416 holonet insert already present")
        return
    if not INSERT.exists():
        raise FileNotFoundError(INSERT)
    block = f"\n{MARKER}\n{INPUT}\n\n"
    if ANCHOR not in text:
        raise RuntimeError("software-section anchor not found in photonic_holonet.tex")
    text = text.replace(ANCHOR, block + ANCHOR, 1)
    MAIN.write_text(text)
    print("inserted BT1416 holonet subsection")


if __name__ == "__main__":
    main()
