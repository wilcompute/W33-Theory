#!/usr/bin/env python3
"""Construct KS inequality for the 24-basis Witting subset.

We use the exact noncontextual bound: max satisfied bases = 23.
Quantum prediction: 24 (state-independent), since each basis sum of projectors = I.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)


def main():
    # Load exact bound
    exact_path = ROOT / "artifacts" / "witting_24basis_exact_bound.json"
    if not exact_path.exists():
        print("Missing exact bound artifact")
        return
    exact = json.loads(exact_path.read_text())
    max_sat = exact.get("max_satisfied")

    # Inequality summary
    num_bases = 24
    quantum_value = 24

    md_path = DOCS / "witting_24basis_inequality.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Witting 24‑Basis KS Inequality\n\n")
        f.write("We define the KS functional as the number of bases satisfied by a\n")
        f.write("noncontextual 0/1 assignment (exactly one 1 per basis).\n\n")
        f.write("## Noncontextual bound (exact)\n")
        f.write(f"- Max satisfiable bases: **{max_sat} / {num_bases}**\n\n")
        f.write("## Quantum prediction (state‑independent)\n")
        f.write(f"- Quantum value: **{quantum_value} / {num_bases}**\n\n")
        f.write("**Reason:** For any quantum state, each orthonormal basis sums to identity,\n")
        f.write("so the expected ‘one‑outcome’ per basis is exactly 1.\n\n")
        f.write("## Inequality\n")
        f.write(f"For any noncontextual model:  S ≤ {max_sat}.\n")
        f.write(f"Quantum mechanics gives:       S = {quantum_value}.\n\n")
        f.write("This yields a state‑independent violation by 1 basis.\n")

    out_path = DOCS / "witting_24basis_inequality.json"
    out_path.write_text(
        json.dumps(
            {
                "noncontextual_bound": int(max_sat),
                "quantum_value": int(quantum_value),
                "bases": num_bases,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Wrote {md_path}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
