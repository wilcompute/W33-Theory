#!/usr/bin/env python3
"""Idempotently install the Passes 1500--1504 TeX insert in the W33 preprint."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "BT1500_BT1504_five_frontiers.tex"
DESTINATION = ROOT / "paper" / "sections" / "sec_bt1500_bt1504_five_frontiers.tex"
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
INPUT_LINE = r"\input{sections/sec_bt1500_bt1504_five_frontiers}"


def integrate(check: bool = False) -> bool:
    assert SOURCE.exists(), SOURCE
    assert PREPRINT.exists(), PREPRINT
    destination_matches = DESTINATION.exists() and DESTINATION.read_bytes() == SOURCE.read_bytes()
    text = PREPRINT.read_text()
    input_present = INPUT_LINE in text
    if check:
        assert destination_matches
        assert text.count(INPUT_LINE) == 1
        return False
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    if not destination_matches:
        shutil.copyfile(SOURCE, DESTINATION)
    if not input_present:
        marker = r"\end{document}"
        assert marker in text
        text = text.replace(marker, INPUT_LINE + "\n\n" + marker, 1)
        PREPRINT.write_text(text)
    assert PREPRINT.read_text().count(INPUT_LINE) == 1
    return not (destination_matches and input_present)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = integrate(args.check)
    print("PASS integrate 1500-1504", "changed" if changed else "stable")


if __name__ == "__main__":
    main()
