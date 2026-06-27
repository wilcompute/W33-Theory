#!/usr/bin/env python3
"""BT1902 — idempotent Holonet insert integrator for BT1899.

Default use:
  python tools/integrate_bt1899_holonet_insert.py

The script is non-destructive.  It reads a Holonet TeX source, splits
papers/BT1899_holonet_residual_and_guard_insert.tex into residual and guard blocks,
then inserts them at the best available marker locations and writes a new output file.
"""
from __future__ import annotations

from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "papers" / "BT1347_photonic_holonet_journal.tex"
PATCH = ROOT / "papers" / "BT1899_holonet_residual_and_guard_insert.tex"
DEFAULT_OUT = ROOT / "papers" / "BT1347_photonic_holonet_journal_with_BT1899.tex"

RESIDUAL_LABEL = "% BT1902 residual block inserted"
GUARD_LABEL = "% BT1902 guard block inserted"
GUARD_MARK = r"\paragraph{Fano time-bin guard envelope.}"
RESIDUAL_MARKERS = [
    r"\section{Architecture Completeness and the Three Physical Residuals}",
    r"\appendix",
    r"\section{Discussion and Open Questions}",
]
GUARD_MARKERS = [
    "Witting transaction",
    "time-bin",
    "Build sheet",
    r"\section{Discussion and Open Questions}",
]


def split_patch(text: str) -> tuple[str, str]:
    if GUARD_MARK not in text:
        raise SystemExit("BT1899 patch does not contain guard paragraph marker")
    before, after = text.split(GUARD_MARK, 1)
    residual = before.strip()
    guard = (GUARD_MARK + after).strip()
    return residual, guard


def insert_after_marker(source: str, block: str, label: str, markers: list[str]) -> str:
    if label in source:
        return source
    labelled = label + "\n" + block.strip() + "\n"
    for marker in markers:
        idx = source.find(marker)
        if idx >= 0:
            line_end = source.find("\n", idx)
            if line_end < 0:
                line_end = idx + len(marker)
            return source[: line_end + 1] + "\n" + labelled + "\n" + source[line_end + 1 :]
    raise SystemExit(f"no insertion marker found for {label}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args()

    source_path = Path(args.source)
    out_path = Path(args.out)
    source = source_path.read_text(encoding="utf-8")
    patch = PATCH.read_text(encoding="utf-8")
    residual, guard = split_patch(patch)

    integrated = insert_after_marker(source, residual, RESIDUAL_LABEL, RESIDUAL_MARKERS)
    integrated = insert_after_marker(integrated, guard, GUARD_LABEL, GUARD_MARKERS)

    if RESIDUAL_LABEL not in integrated or GUARD_LABEL not in integrated:
        raise SystemExit("BT1902 insertion labels missing after integration")
    if "[nosep]" in integrated:
        raise SystemExit("enumitem-only [nosep] detected")

    out_path.write_text(integrated, encoding="utf-8")
    print(f"wrote {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
