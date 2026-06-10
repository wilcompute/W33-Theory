#!/usr/bin/env python3
"""Idempotently integrate BT682 into paper/w33_preprint.tex."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT682_secondary_g2_synthesis_insert.tex"
DST = ROOT / "paper" / "sections" / "sec_bt682_secondary_g2_synthesis.tex"
PRE = ROOT / "paper" / "w33_preprint.tex"
INPUT = r"\input{sections/sec_bt682_secondary_g2_synthesis}"


def main() -> None:
    if not SRC.exists():
        raise FileNotFoundError(SRC)
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(SRC.read_text(encoding="utf-8"), encoding="utf-8")

    if not PRE.exists():
        print("preprint_missing=True")
        return
    text = PRE.read_text(encoding="utf-8")
    if INPUT in text:
        print("input_already_present=True")
        return

    anchors = [
        r"\input{sections/sec_bt676_k44_k33_frame_chain}",
        r"\input{sections/sec_bt627_external_wg2_packet}",
        r"\section{TOE Singularity}",
    ]
    for anchor in anchors:
        if anchor in text:
            text = text.replace(anchor, anchor + "\n" + INPUT, 1)
            PRE.write_text(text, encoding="utf-8")
            print("inserted=True")
            print(f"anchor={anchor}")
            return
    text += "\n" + INPUT + "\n"
    PRE.write_text(text, encoding="utf-8")
    print("inserted=True")
    print("anchor=end")


if __name__ == "__main__":
    main()
