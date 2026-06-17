#!/usr/bin/env python3
"""BT1222 -- idempotently insert the BT1218 readiness section.

This avoids direct large-file replacement through the connector.  Run from repo
root:

    python tools/integrate_bt1218_holonet_experimental_readiness.py --dry-run
    python tools/integrate_bt1218_holonet_experimental_readiness.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

TARGET = Path("photonic_holonet.tex")
INPUT_LINE = r"\input{paper/sections/sec_bt1218_holonet_experimental_readiness}"
MARKERS = [
    r"\subsection{The fault-tolerant layer is the substrate's lattice tower}",
    r"\subsection{Why the primitive is one \emph{massless} photon}",
    r"\section{Experimental roadmap}",
]


def insert_once(text: str) -> tuple[str, str]:
    if INPUT_LINE in text:
        return text, "already_present"
    for marker in MARKERS:
        idx = text.find(marker)
        if idx != -1:
            return text[:idx] + INPUT_LINE + "\n\n" + text[idx:], f"inserted_before:{marker}"
    raise SystemExit("No insertion marker found for BT1218 readiness section")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=TARGET)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    text = args.target.read_text()
    new_text, status = insert_once(text)
    if args.dry_run:
        print(status)
        return
    if new_text != text:
        args.target.write_text(new_text)
    print(status)


if __name__ == "__main__":
    main()
