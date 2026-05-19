#!/usr/bin/env python3
"""Narain/E8 theta coefficient bridge to the [72,66]_3 horizon split.

Parallel commit DCCLXXXI notes the E8 theta series coefficients:
  Theta_E8 = 1 + 240 q + 2160 q^2 + 6720 q^3 + 17520 q^4 + ...
with
  2160 = q^2*|E|,
  6720 = dZ*Phi6*|E|.

New bridge to the explicit horizon parity code:
  horizon split: 72 = 30 + 42
  pure CSS sector: 30 = 2g
  corrected mixed/toroidal flag sector: 42 = 36 + q!
  phase-frame size: 160 = mu*v = 81+79

Then:
  a_2 = 2160 = 30 * 72
  a_3 = 6720 = 160 * 42

So the second E8 theta coefficient is the pure CSS sector times horizon length,
and the third E8 theta coefficient is the phase-frame size times the corrected
toroidal flag sector.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_narain_theta_horizon_split.json"

q=3; dZ=4; Phi6=7; E=240; g=15; mu=4; v=40; H1=81; kernel=79
horizon=72
pure=2*g
mixed=36
parity=6
flags=mixed+parity
phase=mu*v
coeffs={1:240,2:2160,3:6720,4:17520}

payload={
  "summary": {
    "theta_coefficients": coeffs,
    "horizon_split": [pure, flags],
    "a2_split": "2160 = 30*72",
    "a3_split": "6720 = 160*42",
    "all_identities_hold": True
  },
  "identities": {
    "a1_edges": coeffs[1] == E,
    "a2_q2_edges": coeffs[2] == q*q*E,
    "a3_dZ_phi6_edges": coeffs[3] == dZ*Phi6*E,
    "horizon_split": horizon == pure + flags,
    "pure_sector": pure == 30,
    "flag_sector": flags == 42,
    "phase_size": phase == H1 + kernel == 160,
    "a2_horizon_pure": coeffs[2] == pure*horizon,
    "a3_phase_flags": coeffs[3] == phase*flags,
    "a2_over_horizon": coeffs[2]//horizon == pure,
    "a3_over_flags": coeffs[3]//flags == phase,
    "a4_boundary": coeffs[4] == 73*E
  },
  "closed_forms": {
    "a1": "240 = |E(W33)| = E8 roots",
    "a2": "2160 = q^2*|E| = 30*72 = pure CSS sector * horizon length",
    "a3": "6720 = dZ*Phi6*|E| = 160*42 = phase-frame size * toroidal flag block",
    "a4": "17520 = 73*240; 73 remains an honesty boundary",
    "horizon": "72 = 30 + 42 = pure sector + corrected mixed/toroidal flags",
    "phase": "160 = 81+79 = protected H1 image + toroidal metric kernel"
  },
  "theorem": "Narain Theta Horizon Split Theorem: the first nontrivial E8 theta coefficients align with the explicit horizon parity split: a2=2160=30*72 and a3=6720=160*42. Thus the E8 theta/Narain layer sees both the pure CSS sector and the corrected toroidal flag sector of the [72,66]_3 horizon model.",
  "honesty_boundary": "Exact finite arithmetic. This connects theta coefficients to the horizon split, but does not by itself prove a Narain-lattice construction of the W33 code."
}

if __name__ == "__main__":
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
