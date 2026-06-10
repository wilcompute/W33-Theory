#!/usr/bin/env python3
"""Idempotently integrate the BT643 endpoint-recurrence insert."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT643_endpoint_recurrence_physical_lift_insert.tex"
DST = ROOT / "paper" / "sections" / "sec_bt643_endpoint_recurrence_physical_lift.tex"
PREPRINT = ROOT / "paper" / "w33_preprint.tex"
INPUT = r"\input{sections/sec_bt643_endpoint_recurrence_physical_lift}"
ANCHOR = r"\section{The TOE Singularity Theorem}"


def main() -> int:
    if not SRC.exists():
        raise FileNotFoundError(SRC)
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(SRC.read_text(encoding="utf-8"), encoding="utf-8")

    text = PREPRINT.read_text(encoding="utf-8")
    if INPUT not in text:
        if ANCHOR in text:
            text = text.replace(ANCHOR, INPUT + "\n\n" + ANCHOR, 1)
        else:
            text += "\n" + INPUT + "\n"
        PREPRINT.write_text(text, encoding="utf-8")
    print(f"integrated {DST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
