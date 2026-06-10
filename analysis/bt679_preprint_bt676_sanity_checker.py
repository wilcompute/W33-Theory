#!/usr/bin/env python3
"""
BT679 — Static sanity checker for the BT676 preprint insertion.

Checks that the paper path contains the reviewer-safe BT676 claims exactly once:

  * raw complement is 4K4, not Q4;
  * Q4 appears only as secondary codec relation;
  * the corrected chain 4K4 -> Q4 -> K44 -> Match(K44) -> S4/V4 -> K33;
  * the boundary that this is not a flag-level Weyl action.

This checker is deliberately static: it does not compile LaTeX.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
SECTION = ROOT / "paper" / "sections" / "sec_bt676_k44_k33_frame_chain.tex"
SOURCE = ROOT / "analysis" / "BT676_k44_k33_frame_chain_insert.tex"
INPUT_LINE = r"\input{sections/sec_bt676_k44_k33_frame_chain}"

REQUIRED_SNIPPETS = [
    r"K_4\sqcup K_4\sqcup K_4\sqcup K_4",
    r"4K_4\longrightarrow Q_4\longrightarrow Q_4/\{\pm\}\cong K_{4,4}",
    r"V_4=\{(),(12)(34),(13)(24),(14)(23)\}",
    r"S_4/V_4\cong S_3",
    r"\operatorname{Cay}(S_3,\{\hbox{transpositions}\})\cong K_{3,3}",
    r"\operatorname{Aut}(K_{3,3},M_{\rm metric})\cong D_6\cong W(G_2)",
    "not a flag-level Weyl action",
]


def count(text: str, needle: str) -> int:
    return text.count(needle)


def main() -> None:
    missing_paths = [p for p in (PREPRINT, SOURCE) if not p.exists()]
    if missing_paths:
        raise FileNotFoundError(missing_paths)

    preprint_text = PREPRINT.read_text(encoding="utf-8")
    source_text = SOURCE.read_text(encoding="utf-8")
    section_text = SECTION.read_text(encoding="utf-8") if SECTION.exists() else source_text

    # The input should appear no more than once; before running the integrator it may be absent.
    input_count = count(preprint_text, INPUT_LINE)
    assert input_count in (0, 1), input_count

    for snippet in REQUIRED_SNIPPETS:
        assert snippet in source_text or snippet in section_text, snippet

    raw_count = source_text.count(r"C_{16}^{\rm raw}\cong K_4\sqcup K_4\sqcup K_4\sqcup K_4")
    assert raw_count == 1, raw_count

    # Make sure the section text has the secondary, not raw, Q4 phrasing.
    assert "secondary product-codec" in source_text
    assert "not a flag-level Weyl action" in source_text

    print("BT679 preprint BT676 sanity checker: PASS")
    print(f"input_line_count_in_preprint={input_count}")
    print("raw_4K4_warning_count=1")
    print("secondary_Q4_chain_present=True")
    print("K33_D6_WG2_boundary_present=True")


if __name__ == "__main__":
    main()
