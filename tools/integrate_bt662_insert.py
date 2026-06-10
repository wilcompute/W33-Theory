#!/usr/bin/env python3
"""Idempotently integrate BT662 into the W33 preprint."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT662_secondary_codec_g2_channel_insert.tex"
DST = ROOT / "paper" / "sections" / "sec_bt662_secondary_codec_g2_channel.tex"
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
INPUT = r"\input{sections/sec_bt662_secondary_codec_g2_channel}"
MARKERS = [
    r"\input{sections/sec_bt659_s4_trace_codec_split}",
    r"\input{sections/sec_bt647_synthesis_bridge}",
    r"\section{The TOE Singularity Theorem}",
]


def main() -> int:
    if not SRC.exists():
        raise FileNotFoundError(SRC)
    if not PREPRINT.exists():
        raise FileNotFoundError(PREPRINT)
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(SRC.read_text(encoding="utf-8"), encoding="utf-8")
    text = PREPRINT.read_text(encoding="utf-8")
    if INPUT not in text:
        for marker in MARKERS:
            if marker in text:
                text = text.replace(marker, marker + "\n" + INPUT, 1)
                break
        else:
            text += "\n" + INPUT + "\n"
        PREPRINT.write_text(text, encoding="utf-8")
    print(f"integrated {INPUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
