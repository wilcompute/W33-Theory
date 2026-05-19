#!/usr/bin/env python3
"""Ramanujan/Heegner-163 horizon expansion.

Builds on the corrected Moonshine factorization:
    640320 = 7!*127 + 240.

New observation:
    7! = 5040 = 7 * 10 * 72 = Phi6 * Phi4 * lambda_gauge.

Therefore
    640320 = Phi6 * Phi4 * lambda_gauge * B2 + |E|.

The Ramanujan correction term also has a horizon reading:
    744 = 10*72 + 24 = Phi4*lambda_gauge + f.

Hence the famous near integer is organized by the W33 horizon eigenvalue:
    exp(pi sqrt(163)) ~= (Phi6*Phi4*lambda_gauge*B2 + |E|)^3
                         + (Phi4*lambda_gauge + f).
"""
from __future__ import annotations

import json
from math import factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_ramanujan_horizon_expansion.json"

q=3
Phi6=7
Phi4=10
lambda_gauge=72
B2=127
E=240
f=24
root=640320
correction=744

payload={
  "summary": {
    "root": root,
    "correction": correction,
    "factorial_bridge": "7! = Phi6*Phi4*lambda_gauge",
    "root_bridge": "640320 = Phi6*Phi4*lambda_gauge*B2 + |E|",
    "correction_bridge": "744 = Phi4*lambda_gauge + f",
    "all_identities_hold": True
  },
  "identities": {
    "factorial_bridge": factorial(Phi6) == Phi6*Phi4*lambda_gauge == 5040,
    "B2_mersenne": B2 == 2**Phi6 - 1,
    "root_horizon_expansion": root == Phi6*Phi4*lambda_gauge*B2 + E,
    "root_fano_factorial_expansion": root == factorial(Phi6)*B2 + E,
    "correction_horizon_expansion": correction == Phi4*lambda_gauge + f,
    "correction_pell_expansion": correction == f*31,
    "root_mod_horizon": root % lambda_gauge == f,
    "root_minus_edge_divides_horizon_fano_superstring": (root-E) == Phi6*Phi4*lambda_gauge*B2,
    "root_over_edges": root//E == 2668
  },
  "closed_forms": {
    "7_factorial": "7! = 5040 = 7*10*72 = Phi6*Phi4*lambda_gauge",
    "640320": "640320 = 7!*127 + 240 = Phi6*Phi4*lambda_gauge*B2 + |E|",
    "744": "744 = 10*72 + 24 = Phi4*lambda_gauge + f = f*31",
    "near_integer": "e^(pi sqrt(163)) approx (Phi6*Phi4*lambda_gauge*B2 + |E|)^3 + (Phi4*lambda_gauge + f)",
    "mod72": "640320 = 72*8893 + 24, so the root leaves tetrahedron flags modulo the horizon length"
  },
  "theorem": "Ramanujan Horizon Expansion Theorem: the Heegner-163 cube root 640320 and correction 744 are organized by the W33 horizon eigenvalue 72: 640320=Phi6*Phi4*72*B2+|E| and 744=Phi4*72+f.",
  "honesty_boundary": "Exact arithmetic identity. It organizes the Ramanujan near-integer by W33 primitives but does not by itself prove a moonshine module action."
}

if __name__ == "__main__":
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
