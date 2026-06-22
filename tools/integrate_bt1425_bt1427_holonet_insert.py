#!/usr/bin/env python3
"""Idempotently splice the BT1425-BT1427 retwined/Fano pipeline insert into photonic_holonet.tex."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "photonic_holonet.tex"
INSERT = ROOT / "analysis" / "BT1425_BT1427_holonet_insert.tex"
MARKER = "% BT1425-BT1427 retwined/Fano pipeline frontier"
INPUT = "\\input{analysis/BT1425_BT1427_holonet_insert}"
ANCHOR = "%======================================================================\n\\section{The software: braids, teleported gates, universality}"


def main() -> None:
    text = MAIN.read_text(encoding="utf-8")
    if INPUT in text:
        print("BT1425-BT1427 holonet insert already present")
        return
    if not INSERT.exists():
        raise FileNotFoundError(INSERT)
    if ANCHOR not in text:
        raise RuntimeError("software-section anchor not found in photonic_holonet.tex")
    block = f"\n{MARKER}\n{INPUT}\n\n"
    MAIN.write_text(text.replace(ANCHOR, block + ANCHOR, 1), encoding="utf-8")
    print("inserted BT1425-BT1427 holonet subsection")


if __name__ == "__main__":
    main()
