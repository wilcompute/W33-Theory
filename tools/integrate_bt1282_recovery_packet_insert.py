#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT1282_recovery_packet_reproducibility_section.tex"
DST = ROOT / "paper" / "sections" / "sec_bt1282_recovery_packet_reproducibility.tex"
PRE = ROOT / "paper" / "w33_preprint.tex"
INPUT = r"\input{sections/sec_bt1282_recovery_packet_reproducibility}"
ANCHORS = [
    r"\input{sections/sec_bt1276_external_candidate_protocol}",
    r"\input{sections/sec_bt1267_tomography_score_vector}",
    r"\input{sections/sec_bt1261_clifford_tomography_ladder}",
    r"\section{Quantum Mechanics}",
    r"\end{document}",
]


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
    for anchor in ANCHORS:
        if anchor in text:
            new = INPUT + "\n" + anchor if anchor == r"\end{document}" else anchor + "\n" + INPUT
            PRE.write_text(text.replace(anchor, new, 1), encoding="utf-8")
            print("inserted=True")
            print(f"anchor={anchor}")
            return
    PRE.write_text(text + "\n" + INPUT + "\n", encoding="utf-8")
    print("inserted=True")
    print("anchor=end")


if __name__ == "__main__":
    main()
