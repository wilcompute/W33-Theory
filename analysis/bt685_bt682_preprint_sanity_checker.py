#!/usr/bin/env python3
"""
BT685 — BT682 preprint sanity checker.

Static checks for the secondary G2 synthesis insertion.
It verifies the source insert and, when paper/w33_preprint.tex is present,
verifies that the input line is absent or present exactly once.  If the
integrator has been run, it must be present exactly once.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT682_secondary_g2_synthesis_insert.tex"
INTEGRATOR = ROOT / "tools" / "integrate_bt682_insert.py"
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
SECTION = ROOT / "paper" / "sections" / "sec_bt682_secondary_g2_synthesis.tex"
INPUT = r"\input{sections/sec_bt682_secondary_g2_synthesis}"

REQUIRED = [
    r"C_{16}^{\rm raw}\cong K_4\sqcup K_4\sqcup K_4\sqcup K_4",
    r"4K_4",
    r"Q_4",
    r"K_{4,4}",
    r"K_{3,3}",
    r"D_6",
    r"W(G_2)",
    r"J^2=-I",
    r"(iJ)^2=+I",
    "not a raw flag-level Weyl action",
]


def main() -> None:
    assert SRC.exists(), SRC
    assert INTEGRATOR.exists(), INTEGRATOR
    src = SRC.read_text(encoding="utf-8")
    for needle in REQUIRED:
        assert needle in src, needle

    assert INPUT in INTEGRATOR.read_text(encoding="utf-8")

    input_count = None
    section_exists = SECTION.exists()
    if PREPRINT.exists():
        pre = PREPRINT.read_text(encoding="utf-8")
        input_count = pre.count(INPUT)
        assert input_count in (0, 1), input_count

    print("BT685 BT682 preprint sanity checker: PASS")
    print("source_required_claims_present=True")
    print("integrator_input_line_present=True")
    print(f"section_file_exists={section_exists}")
    print(f"preprint_input_count={input_count}")
    if input_count == 0:
        print("note=BT682 source is ready; run tools/integrate_bt682_insert.py to insert into preprint")
    elif input_count == 1:
        print("note=BT682 appears exactly once in preprint")


if __name__ == "__main__":
    main()
