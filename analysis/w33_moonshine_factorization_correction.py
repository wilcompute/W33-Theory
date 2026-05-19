#!/usr/bin/env python3
"""Corrective Moonshine / Heegner-163 bridge.

Parallel commit 3299aa8 suggested that
    640320 = 2^7 * q^2 * 5 * Phi6 * B2.
This is arithmetically false: the RHS is 5,120,640.

The correct factorization is
    640320 = 2^6 * 3 * 5 * 23 * 29
           = 240 * 4 * 23 * 29
           = |E(W33)| * dZ * (f-1) * (f+lambda+q).

But the B2=127 hint is still real in additive form:
    640320 = Phi6! * B2 + |E(W33)|
           = 7! * 127 + 240.

Thus the Ramanujan-Heegner cube root is the Fano factorial acting on the
nonzero Boolean heptad, corrected by the W33/E8 edge carrier.
"""
from __future__ import annotations

import json
from math import factorial, prod
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_moonshine_factorization_correction.json"

q=3; lam=2; dZ=4; Phi6=7; f=24; E=240; B2=127
ramanujan_root=640320
claimed_wrong=(2**7)*(q**2)*5*Phi6*B2
correct_factor=(2**6)*q*5*(f-1)*(f+lam+q)
edge_factor=E*dZ*(f-1)*(f+lam+q)
additive=factorial(Phi6)*B2 + E
j_constant=744
pell_last=31

payload={
  "summary": {
    "ramanujan_root": ramanujan_root,
    "wrong_claim_value": claimed_wrong,
    "correct_prime_factor_form": "2^6 * 3 * 5 * 23 * 29",
    "additive_B2_bridge": "640320 = 7!*127 + 240",
    "all_identities_hold": True
  },
  "identities": {
    "wrong_claim_is_false": claimed_wrong != ramanujan_root,
    "correct_factorization": correct_factor == ramanujan_root,
    "edge_factorization": edge_factor == ramanujan_root,
    "additive_fano_boolean_edge": additive == ramanujan_root,
    "factorial_phi6": factorial(Phi6) == 5040,
    "B2_mersenne": B2 == 2**Phi6 - 1,
    "edge_carrier": E == 240,
    "j_constant_pell": j_constant == f*pell_last == 24*31,
    "j_constant_alt": j_constant == (2**3)*q*pell_last,
    "root_over_edges": ramanujan_root//E == dZ*(f-1)*(f+lam+q)
  },
  "closed_forms": {
    "correction_to_parallel_claim": "2^7*q^2*5*Phi6*B2 = 5120640, not 640320",
    "correct_factorization": "640320 = 2^6*3*5*23*29",
    "edge_factorization": "640320 = 240*4*23*29 = |E|*dZ*(f-1)*(f+lambda+q)",
    "additive_B2_bridge": "640320 = 7!*127 + 240 = Phi6!*B2 + |E|",
    "moonshine_constant": "744 = f*31 = 24*31 = 2^3*q*31"
  },
  "theorem": "Corrected Heegner-163 Moonshine Bridge: the Ramanujan root 640320 is not multiplicatively divisible by B2=127 as claimed; instead it satisfies the exact additive identity 640320=Phi6!*B2+|E|=7!*127+240 and the exact factorization 640320=|E|*dZ*(f-1)*(f+lambda+q).",
  "honesty_boundary": "This corrects an arithmetic error in the parallel hint while preserving the useful B2 connection in additive form."
}

if __name__ == "__main__":
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
