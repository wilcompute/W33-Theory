#!/usr/bin/env python3
"""Idempotently splice the BT1431-BT1434 insert into photonic_holonet.tex."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "photonic_holonet.tex"
INPUT = "\\input{analysis/BT1431_BT1434_holonet_insert}"
MARKER = "% BT1431-BT1434 defect/golden-Moebius frontier"
ANCHOR = "%======================================================================\n\\section{The software: braids, teleported gates, universality}"


def main() -> None:
    text = MAIN.read_text(encoding="utf-8")
    if INPUT in text:
        print("BT1431-BT1434 insert already present")
        return
    if ANCHOR not in text:
        raise RuntimeError("software-section anchor not found")
    MAIN.write_text(text.replace(ANCHOR, f"\n{MARKER}\n{INPUT}\n\n" + ANCHOR, 1), encoding="utf-8")
    print("inserted BT1431-BT1434 Holonet subsection")


if __name__ == "__main__":
    main()
