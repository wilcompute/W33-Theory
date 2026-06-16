#!/usr/bin/env python3
"""Idempotently integrate BT1201/BT1202 inserts into photonic_holonet.tex.

BT1201: lambda-lock theorem, inserted before the massless-photon subsection.
BT1202: R3 continuum checklist, inserted after the two-continuum subsection and
before the fault-tolerant lattice tower subsection.
"""
from pathlib import Path
import argparse

TARGET = Path("photonic_holonet.tex")
R3_INPUT = "\\input{paper/sections/sec_bt1202_holonet_r3_continuum_checklist}\n"
LAMBDA_INPUT = "\\input{paper/sections/sec_bt1201_holonet_lambda_lock}\n"
R3_MARKER = "\\subsection{The fault-tolerant layer is the substrate's lattice tower}"
LAMBDA_MARKER = "\\subsection{Why the primitive is one \\emph{massless} photon}"


def insert_before(text: str, marker: str, row: str) -> tuple[str, bool]:
    if row.strip() in text:
        return text, False
    if marker not in text:
        raise SystemExit(f"marker not found: {marker}")
    return text.replace(marker, row + marker, 1), True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not TARGET.exists():
        raise SystemExit(f"missing target: {TARGET}")

    text = TARGET.read_text()
    planned = []

    new_text, changed = insert_before(text, R3_MARKER, R3_INPUT)
    if changed:
        planned.append(R3_INPUT.strip())
    new_text, changed = insert_before(new_text, LAMBDA_MARKER, LAMBDA_INPUT)
    if changed:
        planned.append(LAMBDA_INPUT.strip())

    print(f"target={TARGET}")
    print(f"planned_inserts={len(planned)}")
    for row in planned:
        print(row)

    if args.dry_run or not planned:
        return
    TARGET.write_text(new_text)


if __name__ == "__main__":
    main()
