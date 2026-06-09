#!/usr/bin/env python3
"""BT620: idempotently add BT618/BT619 paper inserts.

This narrow helper integrates the two folded-Hashimoto physical-propagator
paper inserts without touching the older all-in-one integrators.

Managed inserts:

    analysis/BT618_physical_propagator_normal_form_insert.tex
        -> paper/sections/sec_bt618_physical_propagator_normal_form.tex

    analysis/BT619_endpoint_factorial_trace_law_insert.tex
        -> paper/sections/sec_bt619_endpoint_factorial_trace_law.tex

and the corresponding preprint input lines:

    \input{sections/sec_bt618_physical_propagator_normal_form}
    \input{sections/sec_bt619_endpoint_factorial_trace_law}

The script never duplicates input lines.  It prefers placement after the BT613
folded-Hashimoto/Hodge-flow insert and otherwise falls back to the current
symmetry/phase/cubic-leakage section or the TOE Singularity section.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
SECTION_DIR = ROOT / "paper" / "sections"
INSERTS = [
    (
        ROOT / "analysis" / "BT618_physical_propagator_normal_form_insert.tex",
        SECTION_DIR / "sec_bt618_physical_propagator_normal_form.tex",
        r"\input{sections/sec_bt618_physical_propagator_normal_form}",
    ),
    (
        ROOT / "analysis" / "BT619_endpoint_factorial_trace_law_insert.tex",
        SECTION_DIR / "sec_bt619_endpoint_factorial_trace_law.tex",
        r"\input{sections/sec_bt619_endpoint_factorial_trace_law}",
    ),
]

PRIMARY_MARKERS = [
    r"\input{sections/sec_bt613_folded_hashimoto_hodge_flow}",
    r"\input{sections/sec_bt606_cubic_lock_reviewer_lemma}",
    r"\label{sec:symmetry-phase-cubic-leakage}",
    r"\section{Symmetry, Phase, and Cubic Leakage}",
]
FALLBACK_MARKERS = [
    r"\section{The TOE Singularity Theorem}",
    r"\label{sec:toe-singularity}",
]


def copy_inserts() -> list[str]:
    SECTION_DIR.mkdir(parents=True, exist_ok=True)
    changed = []
    for src, dst, _line in INSERTS:
        if not src.exists():
            raise FileNotFoundError(f"missing source insert: {src.relative_to(ROOT)}")
        content = src.read_text(encoding="utf-8")
        if not dst.exists() or dst.read_text(encoding="utf-8") != content:
            dst.write_text(content, encoding="utf-8")
            changed.append(str(dst.relative_to(ROOT)))
    return changed


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
    missing = [line for _src, _dst, line in INSERTS if line not in text]
    if not missing:
        return False
    pos = find_insert_position(text)
    block = "\n".join(missing) + "\n"
    if pos > 0 and not text[:pos].endswith("\n"):
        block = "\n" + block
    PREPRINT.write_text(text[:pos] + block + text[pos:], encoding="utf-8")
    return True


def main() -> int:
    try:
        copied = copy_inserts()
        changed = integrate_preprint()
    except Exception as exc:  # noqa: BLE001
        print(f"BT618/BT619 insert integration failed: {exc}", file=sys.stderr)
        return 2
    print("BT618/BT619 insert integration complete")
    print(f"section files copied/updated: {copied if copied else 'none'}")
    print(f"preprint changed: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
