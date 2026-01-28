#!/usr/bin/env python3
"""Convert Reck decomposition into MZI-friendly parameters.

For each 2x2 rotation (c,s) we report:
- theta (mixing angle)
- phi (relative phase)
- R = sin^2(theta), T = cos^2(theta)
This maps to a beam splitter with reflectivity R and an internal phase phi.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)


def main():
    in_path = DOCS / "witting_24basis_reck.json"
    if not in_path.exists():
        print("Missing docs/witting_24basis_reck.json")
        return

    data = json.loads(in_path.read_text())
    out = []
    for entry in data:
        ops = []
        for op in entry["ops"]:
            theta = float(op["theta"])
            phi = float(op["phi"])
            R = float((__import__('math').sin(theta))**2)
            T = float((__import__('math').cos(theta))**2)
            ops.append({
                "i": op["i"],
                "j": op["j"],
                "theta": theta,
                "phi": phi,
                "R": R,
                "T": T,
            })
        out.append({
            "basis_index": entry["basis_index"],
            "rays": entry["rays"],
            "ops": ops,
            "diag_phases": entry["diag_phases"],
        })

    json_path = DOCS / "witting_24basis_mzi_schedule.json"
    json_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = DOCS / "witting_24basis_mzi_schedule.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Witting 24‑Basis MZI Schedule\n\n")
        f.write("Each op is a 2×2 mixing on modes (i,j) with reflectivity R and phase phi.\n\n")
        for entry in out:
            f.write(f"## Basis B{entry['basis_index']:02d}\n")
            f.write(f"Rays: {entry['rays']}\n\n")
            for op in entry["ops"]:
                f.write(
                    f"- mix({op['i']},{op['j']}): R={op['R']:.6f}, T={op['T']:.6f}, phi={op['phi']:.6f}\n"
                )
            f.write("\n")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
