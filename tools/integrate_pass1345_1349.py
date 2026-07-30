#!/usr/bin/env python3
"""Idempotently integrate the Passes 1345--1349 theorem insert into both manuscripts."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = r"\input{analysis/BT1345_BT1349_basic_mixed_selector_runtime_fusion}"
SOURCES = ("w33_paper.tex", "photonic_holonet.tex")


def integrate(path: Path) -> str:
    if not path.exists():
        return "SOURCE_UNAVAILABLE"
    text = path.read_text(encoding="utf-8")
    count = text.count(INPUT)
    if count > 1:
        raise SystemExit(f"duplicate Pass-1345--1349 inputs in {path}")
    if count == 1:
        return "UNCHANGED"
    marker = r"\end{document}"
    position = text.rfind(marker)
    if position < 0:
        raise SystemExit(f"missing {marker} in {path}")
    text = text[:position].rstrip() + "\n\n" + INPUT + "\n\n" + text[position:]
    path.write_text(text, encoding="utf-8")
    return "UPDATED"


def main() -> None:
    outcomes = {name: integrate(ROOT / name) for name in SOURCES}
    for name, outcome in outcomes.items():
        print(f"{name}: {outcome}")
    available = [name for name in SOURCES if (ROOT / name).exists()]
    for name in available:
        assert (ROOT / name).read_text(encoding="utf-8").count(INPUT) == 1


if __name__ == "__main__":
    main()
