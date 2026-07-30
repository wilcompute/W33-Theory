#!/usr/bin/env python3
"""Idempotently integrate the Pass-1330--1334 theorem insert into both manuscripts."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = (ROOT / "w33_paper.tex", ROOT / "photonic_holonet.tex")
INPUT = r"\input{analysis/BT1330_BT1334_modular_triality_cycle_atlas}"
MARKER = "% PASS1330_1334_CURRENT_CLAIMS"


def integrate(path: Path) -> bool:
    text = path.read_text()
    if INPUT in text:
        return False
    needle = r"\end{document}"
    if needle not in text:
        raise RuntimeError(f"{path} has no \\end{{document}}")
    replacement = f"\n{MARKER}\n{INPUT}\n\n{needle}"
    path.write_text(text.replace(needle, replacement, 1))
    return True


def main() -> None:
    changed = []
    for target in TARGETS:
        changed.append((target.name, integrate(target)))
    print(changed)


if __name__ == "__main__":
    main()
