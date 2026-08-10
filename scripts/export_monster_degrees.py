#!/usr/bin/env python3
"""Export Monster irreducible character *degrees* to data/monster_degrees_full.json

Use when GAP/libgap is installed. This is a convenience helper for maintainers
who want a full offline dump of Monster irreps.

Usage:
    python scripts/export_monster_degrees.py
"""
from __future__ import annotations

import ast
import shutil
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "monster_degrees_full.json"

if __name__ == "__main__":
    if shutil.which("gap") is None:
        raise SystemExit("GAP not found on PATH — install GAP or use libgap in Sage")

    gap_code = (
        't := CharacterTable("M"); '
        "degs := List(Irr(t), chi -> chi[1]); "
        'Print("GAP:MONSTER_DEGREES:", degs, "\n"); '
        "quit;"
    )
    proc = subprocess.run(
        ["gap", "-q"], input=gap_code, text=True, capture_output=True, check=True
    )
    degs = None
    for line in proc.stdout.splitlines():
        if line.startswith("GAP:MONSTER_DEGREES:"):
            payload = line.split(":", 1)[1].strip()
            degs = ast.literal_eval(payload)
            break
    if degs is None:
        raise SystemExit("Failed to obtain Monster degrees from GAP")

    OUT.write_text(str(degs, encoding="utf-8"))
    print(f"Wrote {len(degs)} Monster degrees to {OUT}")
