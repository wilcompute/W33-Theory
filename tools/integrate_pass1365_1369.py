#!/usr/bin/env python3
"""Idempotently integrate the Pass 1365--1369 theorem into both manuscripts."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "w33_paper.tex", ROOT / "photonic_holonet.tex"]
INPUT = r"\input{analysis/BT1365_BT1369_rational_schur_completion}"


def integrate(path: Path) -> bool:
    text = path.read_text()
    count = text.count(INPUT)
    if count > 1:
        raise SystemExit(f"duplicate {INPUT} in {path}")
    if count == 1:
        return False

    anchors = [
        r"\input{analysis/BT1360_BT1364_gelfand_terwilliger}",
        r"\input{analysis/BT1355_BT1359_selector_matching_scheme}",
        r"\end{document}",
    ]
    for anchor in anchors:
        if anchor in text:
            replacement = (
                INPUT + "\n\n" + anchor
                if anchor == r"\end{document}"
                else anchor + "\n" + INPUT
            )
            path.write_text(text.replace(anchor, replacement, 1))
            return True
    raise SystemExit(f"no insertion anchor in {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        for path in TARGETS:
            if path.read_text().count(INPUT) != 1:
                raise SystemExit(f"missing or duplicate {INPUT} in {path}")
        print("PASS 1369: dual-manuscript integration present exactly once")
        return

    changed = [path.name for path in TARGETS if integrate(path)]
    print("PASS 1369: integrated " + (", ".join(changed) if changed else "already current"))


if __name__ == "__main__":
    main()
