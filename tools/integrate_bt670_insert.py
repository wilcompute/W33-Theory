#!/usr/bin/env python3
"""Integrate BT670 K44/K33 frame-chain insert into the W33 preprint.

Conservative and idempotent:
- copies analysis/BT670_k44_k33_frame_chain_insert.md into paper/sections/ as a .md companion;
- inserts a commented pointer into paper/w33_preprint.tex exactly once.

The BT670 artifact is Markdown/TeX-lite because the initial .tex payload was blocked.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "BT670_k44_k33_frame_chain_insert.md"
TARGET = ROOT / "paper" / "sections" / "sec_bt670_k44_k33_frame_chain.md"
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
MARKER = "% BT670 companion insert: paper/sections/sec_bt670_k44_k33_frame_chain.md"


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(SOURCE.read_text(), encoding="utf-8")

    if not PREPRINT.exists():
        raise FileNotFoundError(PREPRINT)
    text = PREPRINT.read_text(encoding="utf-8")
    if MARKER not in text:
        anchor = "\\section{TOE Singularity}"
        if anchor in text:
            text = text.replace(anchor, MARKER + "\n" + anchor, 1)
        else:
            text += "\n" + MARKER + "\n"
        PREPRINT.write_text(text, encoding="utf-8")

    print("BT673 integration: PASS")
    print(f"copied={TARGET.relative_to(ROOT)}")
    print(f"marker_present={MARKER in PREPRINT.read_text(encoding='utf-8')}")


if __name__ == "__main__":
    main()
