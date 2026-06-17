#!/usr/bin/env python3
"""Idempotently integrate BT1236/BT1249/BT1258 into paper/w33_preprint.tex."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT / "paper" / "w33_preprint.tex"
SECTIONS = [
    {
        "src": ROOT / "analysis" / "BT1236_minimal_clifford_tomography_insert.tex",
        "dst": ROOT / "paper" / "sections" / "sec_bt1236_minimal_clifford_word_metric.tex",
        "input": r"\input{sections/sec_bt1236_minimal_clifford_word_metric}",
    },
    {
        "src": ROOT / "analysis" / "BT1249_bt1236_bt1242_bt1245_paper_addendum.tex",
        "dst": ROOT / "paper" / "sections" / "sec_bt1249_four_transvection_regime_theorem.tex",
        "input": r"\input{sections/sec_bt1249_four_transvection_regime_theorem}",
    },
    {
        "src": ROOT / "analysis" / "BT1258_polar_path_tetrahedron_paper_theorem.tex",
        "dst": ROOT / "paper" / "sections" / "sec_bt1258_polar_path_tetrahedron_theorem.tex",
        "input": r"\input{sections/sec_bt1258_polar_path_tetrahedron_theorem}",
    },
]


def insert_once(text: str, input_line: str) -> tuple[str, bool, str]:
    if input_line in text:
        return text, False, "already_present"
    anchors = [
        r"\input{sections/sec_bt1258_polar_path_tetrahedron_theorem}",
        r"\input{sections/sec_bt1249_four_transvection_regime_theorem}",
        r"\input{sections/sec_bt1236_minimal_clifford_word_metric}",
        r"\input{sections/sec_bt618_physical_propagator_normal_form}",
        r"\input{sections/sec_bt613_folded_hashimoto_hodge_flow}",
        r"\section{Quantum Mechanics}",
        r"\section{TOE Singularity}",
        r"\end{document}",
    ]
    for anchor in anchors:
        if anchor in text and anchor != input_line:
            if anchor == r"\end{document}":
                return text.replace(anchor, input_line + "\n" + anchor, 1), True, anchor
            return text.replace(anchor, anchor + "\n" + input_line, 1), True, anchor
    return text + "\n" + input_line + "\n", True, "end"


def main() -> None:
    for sec in SECTIONS:
        if not sec["src"].exists():
            raise FileNotFoundError(sec["src"])
        sec["dst"].parent.mkdir(parents=True, exist_ok=True)
        sec["dst"].write_text(sec["src"].read_text(encoding="utf-8"), encoding="utf-8")
    if not PRE.exists():
        print("preprint_missing=True")
        return
    text = PRE.read_text(encoding="utf-8")
    changed_any = False
    for sec in SECTIONS:
        text, changed, anchor = insert_once(text, sec["input"])
        changed_any = changed_any or changed
        print(f"input={sec['input']}")
        print(f"status={'inserted' if changed else 'already_present'}")
        print(f"anchor={anchor}")
    if changed_any:
        PRE.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
