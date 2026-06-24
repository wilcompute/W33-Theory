#!/usr/bin/env python3
"""Idempotently integrate BT1657 Heawood clock homology into photonic_holonet.tex."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "BT1657_heawood_clock_homology_insert.tex"
TARGET = ROOT / "paper" / "sections" / "sec_bt1657_heawood_clock_homology.tex"
MAIN = ROOT / "photonic_holonet.tex"
INPUT_LINE = r"\input{paper/sections/sec_bt1657_heawood_clock_homology}"
ANCHOR = r"(Witness: \texttt{analysis/w33\_machine\_clock\_is\_mass.py}.)"


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    if not MAIN.exists():
        raise FileNotFoundError(MAIN)

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    source_text = SOURCE.read_text()
    TARGET.write_text(source_text)

    main_text = MAIN.read_text()
    if INPUT_LINE in main_text:
        print("BT1657 input already present; no main-file edit needed.")
        return

    if ANCHOR not in main_text:
        raise RuntimeError(
            "Could not find BT1657 insertion anchor after the clock-is-mass witness."
        )

    replacement = ANCHOR + "\n\n" + INPUT_LINE
    main_text = main_text.replace(ANCHOR, replacement, 1)
    MAIN.write_text(main_text)
    print(f"Integrated {TARGET.relative_to(ROOT)} into photonic_holonet.tex")


if __name__ == "__main__":
    main()
