#!/usr/bin/env python3
"""Idempotently integrate the Passes 1355--1359 theorem into both root manuscripts."""
from __future__ import annotations

import argparse
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
INPUT = r"\input{analysis/BT1355_BT1359_selector_matching_scheme}"


def targets(root: Path) -> tuple[Path, Path]:
    return root / "w33_paper.tex", root / "photonic_holonet.tex"


def integrate(path: Path) -> bool:
    text = path.read_text()
    count = text.count(INPUT)
    if count > 1:
        raise RuntimeError(f"duplicate integration marker in {path}: {count}")
    if count == 1:
        return False
    marker = r"\end{document}"
    if marker not in text:
        raise RuntimeError(f"missing {marker} in {path}")
    path.write_text(text.replace(marker, f"\n{INPUT}\n\n{marker}", 1))
    return True


def check(path: Path) -> None:
    count = path.read_text().count(INPUT)
    if count != 1:
        raise RuntimeError(f"expected one integration marker in {path}, found {count}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    manuscript_targets = targets(root)
    if args.check:
        for path in manuscript_targets:
            check(path)
        print("PASS 1359: both manuscript markers are unique")
        return
    changed = [str(path.relative_to(root)) for path in manuscript_targets if integrate(path)]
    for path in manuscript_targets:
        check(path)
    print("PASS 1359: integrated " + (", ".join(changed) if changed else "already current"))


if __name__ == "__main__":
    main()
