#!/usr/bin/env python3
"""Idempotently integrate BT1236 into paper/w33_preprint.tex."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT1236_minimal_clifford_tomography_insert.tex"
DST = ROOT / "paper" / "sections" / "sec_bt1236_minimal_clifford_word_metric.tex"
PRE = ROOT / "paper" / "w33_preprint.tex"
INPUT = r"\input{sections/sec_bt1236_minimal_clifford_word_metric}"


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
        r"\input{sections/sec_bt618_physical_propagator_normal_form}",
        r"\input{sections/sec_bt613_folded_hashimoto_hodge_flow}",
        r"\section{Quantum Mechanics}",
        r"\section{TOE Singularity}",
        r"\end{document}",
    ]
    for anchor in anchors:
        if anchor in text:
            if anchor == r"\end{document}":
                text = text.replace(anchor, INPUT + "\n" + anchor, 1)
            else:
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
