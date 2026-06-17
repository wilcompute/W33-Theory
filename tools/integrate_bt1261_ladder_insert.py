#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT1261_clifford_tomography_ladder_section.tex"
DST = ROOT / "paper" / "sections" / "sec_bt1261_clifford_tomography_ladder.tex"
PRE = ROOT / "paper" / "w33_preprint.tex"
INPUT = r"\input{sections/sec_bt1261_clifford_tomography_ladder}"
ANCHORS = [
    r"\input{sections/sec_bt1258_polar_path_tetrahedron_theorem}",
    r"\input{sections/sec_bt1249_four_transvection_regime_theorem}",
    r"\input{sections/sec_bt1236_minimal_clifford_word_metric}",
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
            if anchor == r"\end{document}":
                text = text.replace(anchor, INPUT + "\n" + anchor, 1)
            else:
                text = text.replace(anchor, anchor + "\n" + INPUT, 1)
            PRE.write_text(text, encoding="utf-8")
            print("inserted=True")
            print(f"anchor={anchor}")
            return
    PRE.write_text(text + "\n" + INPUT + "\n", encoding="utf-8")
    print("inserted=True")
    print("anchor=end")


if __name__ == "__main__":
    main()
