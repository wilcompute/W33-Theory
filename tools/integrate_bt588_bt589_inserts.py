#!/usr/bin/env python3
"""BT591: idempotent integrator for BT588/BT589 paper inserts.

This script copies the standalone LaTeX inserts from analysis/ into paper/sections/
and inserts the corresponding \input lines into paper/w33_preprint.tex exactly once.

It is intentionally conservative:
- it never duplicates an existing input line;
- it prefers insertion after the Symmetry, Phase, and Cubic Leakage section;
- if that marker is missing, it inserts immediately before the TOE Singularity section;
- it prints a small report of what changed.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
SECTION_DIR = ROOT / "paper" / "sections"
SOURCES = [
    (
        ROOT / "analysis" / "BT588_leakage_table_latex_insert.tex",
        SECTION_DIR / "sec_bt588_raw_cubic_leakage_ratios.tex",
        r"\input{sections/sec_bt588_raw_cubic_leakage_ratios}",
    ),
    (
        ROOT / "analysis" / "BT589_homology_separation_latex_insert.tex",
        SECTION_DIR / "sec_bt589_levi_vs_fiber_homology.tex",
        r"\input{sections/sec_bt589_levi_vs_fiber_homology}",
    ),
]

PRIMARY_MARKERS = [
    r"\label{sec:symmetry-phase-cubic-leakage}",
    r"\section{Symmetry, Phase, and Cubic Leakage}",
    r"\input{sections/sec_symmetry_phase_cubic_leakage}",
]
FALLBACK_MARKERS = [
    r"\section{The TOE Singularity Theorem}",
    r"\label{sec:toe-singularity}",
]


def copy_section_files() -> list[str]:
    SECTION_DIR.mkdir(parents=True, exist_ok=True)
    changed = []
    for src, dst, _input_line in SOURCES:
        if not src.exists():
            raise FileNotFoundError(f"missing source insert: {src.relative_to(ROOT)}")
        content = src.read_text(encoding="utf-8")
        if not dst.exists() or dst.read_text(encoding="utf-8") != content:
            dst.write_text(content, encoding="utf-8")
            changed.append(str(dst.relative_to(ROOT)))
    return changed


def find_insert_position(text: str) -> int:
    # Prefer after the symmetry-phase-cubic section marker.
    best = -1
    for marker in PRIMARY_MARKERS:
        pos = text.find(marker)
        if pos != -1:
            line_end = text.find("\n", pos)
            return len(text) if line_end == -1 else line_end + 1
    # Otherwise insert before TOE Singularity.
    for marker in FALLBACK_MARKERS:
        pos = text.find(marker)
        if pos != -1:
            return pos
    # Last safe fallback: before \end{document}.
    pos = text.rfind(r"\end{document}")
    return len(text) if pos == -1 else pos


def integrate_preprint() -> bool:
    if not PREPRINT.exists():
        raise FileNotFoundError(f"missing preprint: {PREPRINT.relative_to(ROOT)}")
    text = PREPRINT.read_text(encoding="utf-8")
    missing = [input_line for *_rest, input_line in SOURCES if input_line not in text]
    if not missing:
        return False
    insert_block = "\n".join(missing) + "\n"
    pos = find_insert_position(text)
    if pos > 0 and not text[:pos].endswith("\n"):
        insert_block = "\n" + insert_block
    new_text = text[:pos] + insert_block + text[pos:]
    PREPRINT.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    try:
        copied = copy_section_files()
        preprint_changed = integrate_preprint()
    except Exception as exc:  # noqa: BLE001 - command-line reporting
        print(f"BT591 integration failed: {exc}", file=sys.stderr)
        return 2
    print("BT591 integration complete")
    print(f"section files copied/updated: {copied if copied else 'none'}")
    print(f"preprint changed: {preprint_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
