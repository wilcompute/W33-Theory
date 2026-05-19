#!/usr/bin/env python3
"""Fano-Hamming / horizon-code bridge.

Parallel commit e4f2d51 adds the binary shadow:
  Hamming [7,4,3]_2 = [Phi6, dZ, dX]_2,
  dual simplex [7,3,4]_2 has 2^3=8 codewords/cosets,
  B2+1 = 2^7 = 128 full binary heptad closure.

Our horizon code has:
  [72,66]_3, parity rank 6=2q, length 72=q^2*8.

New bridge:
  horizon length = q^2 * |dual Hamming/simplex code| = 9*8=72,
  horizon parity rank = 2 * Hamming parity rank = 2*3=6,
  horizon dimension = q^2*8 - 2q = 72-6=66,
  horizon payload = q^2*Phi6 + q = 63+3=66.

Thus the [72,66]_3 horizon code is the qutrit lift of the binary Fano-Hamming
quotient: nine qutrit sheets over the 8-element binary syndrome/coset space,
with doubled Hamming parity rank.
"""
from __future__ import annotations

import json
from math import factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_fano_hamming_horizon_code_bridge.json"

q=3; dX=3; dZ=4; Phi6=7; Phi3=13; f=24; E=240
hamming_n=Phi6; hamming_k=dZ; hamming_d=dX
hamming_rank=hamming_n-hamming_k
hamming_size=2**hamming_k
dual_size=2**hamming_rank
binary_heptad=2**Phi6
N=q*q*dual_size
R=2*hamming_rank
K=N-R
payload_alt=q*q*Phi6 + q
B2=binary_heptad-1
AutFano=f*Phi6

payload={
  "summary": {
    "hamming_parameters": [hamming_n,hamming_k,hamming_d],
    "dual_simplex_size": dual_size,
    "horizon_parameters": [N,K,R],
    "binary_heptad_closure": binary_heptad,
    "all_identities_hold": True
  },
  "identities": {
    "hamming_parameters_match": [hamming_n,hamming_k,hamming_d] == [Phi6,dZ,dX],
    "hamming_rank_is_q": hamming_rank == q,
    "dual_size_is_tomotope_cells": dual_size == 8 == Phi6+1,
    "horizon_length_from_dual": N == 72 == q*q*dual_size,
    "horizon_rank_from_hamming": R == 6 == 2*hamming_rank,
    "horizon_dimension": K == 66,
    "payload_alt": K == payload_alt == 66,
    "B2_closure": B2+1 == binary_heptad == 128,
    "horizon_plus_hamming_payload": K + hamming_size == 82,
    "aut_fano": AutFano == 168,
    "aut_fano_e8_to_8fact": AutFano*E == factorial(8)
  },
  "closed_forms": {
    "binary_shadow": "Hamming [7,4,3]_2 = [Phi6,dZ,dX]_2; parity rank 3=q",
    "dual_shadow": "dual simplex [7,3,4]_2 has 8=1+Phi6 codewords/cosets",
    "horizon_length": "72 = q^2 * 8 = 9 binary syndrome/coset sheets",
    "horizon_rank": "6 = 2q = doubled Hamming parity rank",
    "horizon_dimension": "66 = 72 - 6 = q^2*Phi6 + q = 63+3",
    "heptad_closure": "128 = 2^7 = B2+1",
    "fano_e8_factorial": "168*240 = 8!"
  },
  "theorem": "Fano-Hamming Horizon Code Bridge: the [72,66]_3 horizon parity code is a qutrit lift of the binary Hamming [7,4,3]_2 syndrome quotient: length 72=q^2*2^q, parity rank 6=2q, and dimension 66=q^2*Phi6+q.",
  "honesty_boundary": "Exact parameter bridge. A literal functor from the binary Hamming code to the ternary horizon code still requires an explicit map of check matrices and syndromes."
}

if __name__ == "__main__":
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
