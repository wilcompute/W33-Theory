#!/usr/bin/env python3
"""BT614: idempotently add the BT613 folded-Hashimoto/Hodge-flow insert.

This narrow helper keeps the existing insert pipeline conservative while adding
one new managed paper section:

    analysis/BT613_folded_hashimoto_hodge_flow_insert.tex
        -> paper/sections/sec_bt613_folded_hashimoto_hodge_flow.tex

and one preprint line:

    \input{sections/sec_bt613_folded_hashimoto_hodge_flow}

It never duplicates the input line.  It prefers placement near the existing
Symmetry, Phase, and Cubic Leakage section and otherwise falls back to insertion
before the TOE Singularity section.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
SRC = ROOT / "analysis" / "BT613_folded_hashimoto_hodge_flow_insert.tex"
DST = ROOT / "paper" / "sections" / "sec_bt613_folded_hashimoto_hodge_flow.tex"
INPUT_LINE = r"\input{sections/sec_bt613_folded_hashimoto_hodge_flow}"

PRIMARY_MARKERS = [
    r"\input{sections/sec_bt606_cubic_lock_reviewer_lemma}",
    r"\label{sec:symmetry-phase-cubic-leakage}",
    r"\section{Symmetry, Phase, and Cubic Leakage}",
]
FALLBACK_MARKERS = [
    r"\section{The TOE Singularity Theorem}",
    r"\label{sec:toe-singularity}",
]


def copy_insert() -> bool:
    if not SRC.exists():
        raise FileNotFoundError(f"missing source insert: {SRC.relative_to(ROOT)}")
    DST.parent.mkdir(parents=True, exist_ok=True)
    content = SRC.read_text(encoding="utf-8")
    if not DST.exists() or DST.read_text(encoding="utf-8") != content:
        DST.write_text(content, encoding="utf-8")
        return True
    return False


def find_insert_position(text: str) -> int:
    for marker in PRIMARY_MARKERS:
        pos = text.find(marker)
        if pos != -1:
            line_end = text.find("\n", pos)
            return len(text) if line_end == -1 else line_end + 1
    for marker in FALLBACK_MARKERS:
        pos = text.find(marker)
        if pos != -1:
            return pos
    pos = text.rfind(r"\end{document}")
    return len(text) if pos == -1 else pos


def integrate_preprint() -> bool:
    if not PREPRINT.exists():
        raise FileNotFoundError(f"missing preprint: {PREPRINT.relative_to(ROOT)}")
    text = PREPRINT.read_text(encoding="utf-8")
    if INPUT_LINE in text:
        return False
    pos = find_insert_position(text)
    line = INPUT_LINE + "\n"
    if pos > 0 and not text[:pos].endswith("\n"):
        line = "\n" + line
    PREPRINT.write_text(text[:pos] + line + text[pos:], encoding="utf-8")
    return True


def main() -> int:
    try:
        copied = copy_insert()
        preprint_changed = integrate_preprint()
    except Exception as exc:  # noqa: BLE001
        print(f"BT613 insert integration failed: {exc}", file=sys.stderr)
        return 2
    print("BT613 insert integration complete")
    print(f"section copied/updated: {copied}")
    print(f"preprint changed: {preprint_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
