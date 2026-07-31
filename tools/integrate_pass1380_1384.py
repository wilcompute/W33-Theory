#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSERT = r'\input{analysis/BT1380_BT1384_mackey_selector_decomposition}'
TARGETS = [ROOT / 'w33_paper.tex', ROOT / 'photonic_holonet.tex']


def integrate(path: Path) -> None:
    text = path.read_text()
    count = text.count(INSERT)
    if count > 1:
        raise SystemExit(f'duplicate {INSERT} in {path}')
    if count == 0:
        marker = r'\end{document}'
        if marker not in text:
            raise SystemExit(f'missing end document in {path}')
        path.write_text(text.replace(marker, INSERT + '\n\n' + marker, 1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        for path in TARGETS:
            if path.read_text().count(INSERT) != 1:
                raise SystemExit(f'integration drift: {path}')
    else:
        for path in TARGETS:
            integrate(path)
    print('PASS integration 1380-1384')


if __name__ == '__main__':
    main()
