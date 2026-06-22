#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "photonic_holonet.tex"
INPUT = "\\input{analysis/BT1441_BT1443_holonet_insert}"
MARKER = "% BT1441-BT1443 Otto/Szilassi closure frontier"
ANCHOR = "%======================================================================\n\\section{The software: braids, teleported gates, universality}"


def main() -> None:
    text = MAIN.read_text(encoding="utf-8")
    if INPUT in text:
        print("BT1441-BT1443 insert already present")
        return
    if ANCHOR not in text:
        raise RuntimeError("software-section anchor not found")
    MAIN.write_text(text.replace(ANCHOR, f"\n{MARKER}\n{INPUT}\n\n" + ANCHOR, 1), encoding="utf-8")
    print("inserted BT1441-BT1443 Holonet subsection")


if __name__ == "__main__":
    main()
