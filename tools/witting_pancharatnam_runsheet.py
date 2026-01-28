#!/usr/bin/env python3
"""Generate a run-sheet for the Pancharatnam phase measurement.

Uses explicit triangle examples (±π/6, ±π/2) and the ray amplitude/phase table.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def load_ray_table():
    path = DOCS / "witting_ray_amplitude_phase.csv"
    table = {}
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            idx = int(row["ray_index"])
            comp = int(row["comp"])
            table.setdefault(idx, []).append(row)
    return table


def main():
    examples_path = DOCS / "witting_pancharatnam_examples.json"
    if not examples_path.exists():
        print("Missing docs/witting_pancharatnam_examples.json")
        return

    examples = json.loads(examples_path.read_text())
    table = load_ray_table()

    md_path = DOCS / "witting_pancharatnam_runsheet.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Pancharatnam Phase Run‑Sheet (π/6, π/2)\n\n")
        f.write("This run‑sheet gives concrete ray triples and state‑prep tables.\n\n")
        f.write("## Measurement loop\n")
        f.write("1. Prepare |a⟩\n2. Measure phase of ⟨a|b⟩\n3. Prepare |b⟩ and measure phase of ⟨b|c⟩\n4. Prepare |c⟩ and measure phase of ⟨c|a⟩\n5. Sum phases → Φ\n\n")

        for label in ["+pi/6", "-pi/6", "+pi/2", "-pi/2"]:
            triple = examples.get(label)
            if not triple:
                continue
            i, j, k, ang = triple
            f.write(f"## Target phase {label}\n")
            f.write(f"Ray triple: ({i}, {j}, {k})\n")
            f.write(f"Expected Φ ≈ {ang:.6f} rad\n\n")
            for idx in (i, j, k):
                f.write(f"### Ray r{idx} amplitude/phase per component\n")
                f.write("comp | amp | phase (deg)\n")
                f.write("--- | --- | ---\n")
                for row in table[idx]:
                    f.write(f"{row['comp']} | {row['amp']} | {row['phase_deg']}\n")
                f.write("\n")

        f.write("## Notes\n")
        f.write("- Phases are modulo 2π.\n")
        f.write("- Use common phase reference across interferometric measurements.\n")

    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
