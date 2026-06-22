#!/usr/bin/env python3
"""Idempotently splice the Fano-bus Holonet insert stack into photonic_holonet.tex."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "photonic_holonet.tex"
INPUTS = [
    "\\input{analysis/BT1419_BT1421_holonet_insert}",
    "\\input{analysis/BT1422_BT1424_holonet_insert}",
    "\\input{analysis/BT1425_BT1427_holonet_insert}",
    "\\input{analysis/BT1430_fano_bus_master_insert}",
]
MARKER = "% BT1430 Fano-bus integrated frontier stack"
ANCHOR = "%======================================================================\n\\section{The software: braids, teleported gates, universality}"


def main() -> None:
    text = MAIN.read_text(encoding="utf-8")
    missing = [line for line in INPUTS if line not in text]
    if not missing:
        print("BT1430 Fano-bus insert stack already present")
        return
    if ANCHOR not in text:
        raise RuntimeError("software-section anchor not found")
    block = "\n" + MARKER + "\n" + "\n".join(missing) + "\n\n"
    MAIN.write_text(text.replace(ANCHOR, block + ANCHOR, 1), encoding="utf-8")
    print(f"inserted {len(missing)} BT1430 Fano-bus input lines")


if __name__ == "__main__":
    main()
