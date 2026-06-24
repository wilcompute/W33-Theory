#!/usr/bin/env python3
"""Idempotently integrate BT1672 projector-hardware falsifier section."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper" / "sections" / "sec_bt1672_projector_hardware_falsifier.tex"
MAIN = ROOT / "photonic_holonet.tex"
INPUT_LINE = r"\input{paper/sections/sec_bt1672_projector_hardware_falsifier}"
ANCHOR = r"\input{paper/sections/sec_bt1657_heawood_clock_homology}"


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    if not MAIN.exists():
        raise FileNotFoundError(MAIN)
    text = MAIN.read_text()
    if INPUT_LINE in text:
        print("BT1672 input already present; no edit needed.")
        return
    if ANCHOR in text:
        text = text.replace(ANCHOR, ANCHOR + "\n" + INPUT_LINE, 1)
    else:
        fallback = r"\subsection{A near-term falsification test: the demonstrator as an experiment on the substrate}"
        if fallback not in text:
            raise RuntimeError("Could not find BT1672 insertion anchor.")
        text = text.replace(fallback, INPUT_LINE + "\n\n" + fallback, 1)
    MAIN.write_text(text)
    print("Integrated BT1672 section into photonic_holonet.tex")


if __name__ == "__main__":
    main()
