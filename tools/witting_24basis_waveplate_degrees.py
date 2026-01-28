#!/usr/bin/env python3
"""Convert waveplate schedule to degrees with explicit axis convention.

Assumes angles are rotation of fast axis from horizontal (Jones convention).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)


def main():
    in_path = DOCS / "witting_24basis_waveplates.json"
    if not in_path.exists():
        print("Missing docs/witting_24basis_waveplates.json")
        return

    data = json.loads(in_path.read_text())
    out = []

    for entry in data:
        ops = []
        for op in entry["ops"]:
            ops.append({
                "i": op["i"],
                "j": op["j"],
                "qwp1_deg": float(math.degrees(op["qwp1"]) % 180),
                "hwp_deg": float(math.degrees(op["hwp"]) % 180),
                "qwp2_deg": float(math.degrees(op["qwp2"]) % 180),
                "fit_error": op["fit_error"],
            })
        out.append({
            "basis_index": entry["basis_index"],
            "rays": entry["rays"],
            "ops": ops,
        })

    json_path = DOCS / "witting_24basis_waveplates_deg.json"
    json_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = DOCS / "witting_24basis_waveplates_deg.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Witting 24‑Basis Waveplate Schedule (Degrees)\n\n")
        f.write("**Convention:** angles are fast‑axis rotations in degrees, modulo 180°.\n\n")
        for entry in out:
            f.write(f"## Basis B{entry['basis_index']:02d}\n")
            f.write(f"Rays: {entry['rays']}\n\n")
            for op in entry["ops"]:
                f.write(
                    f"- mix({op['i']},{op['j']}): QWP={op['qwp1_deg']:.2f}°, HWP={op['hwp_deg']:.2f}°, QWP={op['qwp2_deg']:.2f}° (err={op['fit_error']:.3e})\n"
                )
            f.write("\n")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
