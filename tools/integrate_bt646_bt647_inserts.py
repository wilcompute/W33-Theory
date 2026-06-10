#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
SECTIONS = ROOT / "paper" / "sections"

INPUTS = [
    "\\input{sections/sec_bt646_internal_s4_hodge_clock}",
    "\\input{sections/sec_bt647_synthesis_bridge}",
]


def main() -> int:
    text = PREPRINT.read_text(encoding="utf-8")
    marker = "\\section{The TOE Singularity Theorem}"
    insert = "\n".join(INPUTS) + "\n\n"
    for line in INPUTS:
        if line not in text:
            if marker in text:
                text = text.replace(marker, insert + marker, 1)
            else:
                text = text.rstrip() + "\n\n" + line + "\n"
    PREPRINT.write_text(text, encoding="utf-8")
    for required in [
        SECTIONS / "sec_bt646_internal_s4_hodge_clock.tex",
        SECTIONS / "sec_bt647_synthesis_bridge.tex",
    ]:
        if not required.exists():
            raise FileNotFoundError(required)
    print("BT646/BT647 inputs integrated or already present.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
