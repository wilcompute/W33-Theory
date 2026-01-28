#!/usr/bin/env python3
"""Estimate noise robustness for the 24-basis KS inequality.

We model depolarizing noise: rho -> v rho + (1-v) I/d.
The KS functional S equals the sum of probabilities of the designated outcomes
(one per basis). In the ideal case, S_q = 24.
Under depolarization, each projector expectation shifts to:
  p_v = v * p_ideal + (1-v)/d.
Since each basis includes exactly one designated outcome, S_v = 24 * (v + (1-v)/d).
We solve for v where S_v equals the noncontextual bound (23).
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)


def main():
    d = 4
    S_q = 24

    # Load exact noncontextual bound if available
    bound_path = ROOT / "artifacts" / "witting_24basis_exact_bound.json"
    if bound_path.exists():
        data = json.loads(bound_path.read_text())
        S_nc = data.get("max_satisfied", 23)
    else:
        S_nc = 23

    # S_v = S_q * (v + (1-v)/d)
    # Solve S_v = S_nc
    # v + (1-v)/d = S_nc / S_q
    target = S_nc / S_q
    v = (target - 1 / d) / (1 - 1 / d)

    # Convert to noise p = 1 - v
    p = 1 - v

    md_path = DOCS / "witting_24basis_noise_threshold.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Witting 24‑Basis KS Noise Threshold\n\n")
        f.write(f"Dimension d = {d}\n\n")
        f.write(f"Noncontextual bound: S_nc = {S_nc}\n")
        f.write(f"Quantum value: S_q = {S_q}\n\n")
        f.write("## Depolarizing noise model\n")
        f.write("S(v) = S_q * (v + (1-v)/d)\n\n")
        f.write("## Threshold\n")
        f.write(f"Solve S(v) = S_nc → v ≥ {v:.6f}\n")
        f.write(f"Equivalent depolarizing noise fraction: p ≤ {p:.6f}\n")

    out_path = DOCS / "witting_24basis_noise_threshold.json"
    out_path.write_text(
        json.dumps(
            {"d": d, "S_q": S_q, "S_nc": S_nc, "v_min": v, "p_max": p},
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Wrote {md_path}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
