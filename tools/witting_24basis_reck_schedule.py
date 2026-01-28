#!/usr/bin/env python3
"""Convert Reck decomposition JSON into a human-readable schedule."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def main():
    in_path = DOCS / "witting_24basis_reck.json"
    if not in_path.exists():
        print("Missing docs/witting_24basis_reck.json")
        return

    data = json.loads(in_path.read_text())

    md_path = DOCS / "witting_24basis_reck_schedule.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Witting 24‑Basis Reck Schedule\n\n")
        f.write("Each operation is a 2×2 complex Givens rotation acting on modes (i,j).\n")
        f.write("Parameters: theta (mixing), phi (relative phase).\n\n")
        for entry in data:
            bi = entry["basis_index"]
            f.write(f"## Basis B{bi:02d}\n")
            f.write(f"Rays: {entry['rays']}\n\n")
            for op in entry["ops"]:
                f.write(
                    f"- mix({op['i']},{op['j']}): theta={op['theta']:.6f}, phi={op['phi']:.6f}\n"
                )
            f.write("\n")

    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
