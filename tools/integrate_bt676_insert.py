#!/usr/bin/env python3
"""Integrate BT676's compilable K44/K33 frame-chain insert.

This supersedes the BT673 markdown-pointer path with a real LaTeX section.
It is conservative and idempotent.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "BT676_k44_k33_frame_chain_insert.tex"
TARGET = ROOT / "paper" / "sections" / "sec_bt676_k44_k33_frame_chain.tex"
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
INPUT_LINE = r"\input{sections/sec_bt676_k44_k33_frame_chain}"


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    if not PREPRINT.exists():
        raise FileNotFoundError(PREPRINT)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(SOURCE.read_text(encoding="utf-8"), encoding="utf-8")

    text = PREPRINT.read_text(encoding="utf-8")
    if INPUT_LINE not in text:
        anchors = [
            r"\input{sections/sec_bt667_codec_g2}",
            r"\input{sections/sec_bt627_external_wg2_packet}",
            r"\section{TOE Singularity}",
        ]
        for anchor in anchors:
            if anchor in text:
                text = text.replace(anchor, anchor + "\n" + INPUT_LINE, 1)
                break
        else:
            text += "\n" + INPUT_LINE + "\n"
        PREPRINT.write_text(text, encoding="utf-8")

    print("BT676 integration: PASS")
    print(f"copied={TARGET.relative_to(ROOT)}")
    print(f"input_present={INPUT_LINE in PREPRINT.read_text(encoding='utf-8')}")


if __name__ == "__main__":
    main()
