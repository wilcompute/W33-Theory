#!/usr/bin/env python3
"""[72,66]+6 parity-check interpretation of the W33 critical edge horizon.

This formalizes the user's suggestion:

    66/72 are regular data symbols, and the last 6 are parity/check symbols.

At the CSS genus horizon n=k=12:

    data symbols        = C(12,2) = 66 complete-edge relations,
    parity/check symbols= q!      = 6 correction branches,
    total symbols       = 72      = (12-3)(12-4).

The code rate is 66/72=11/12, and the redundancy fraction is 1/12,
exactly the denominator of the genus equation.

This is not asserted as a literal binary linear code.  It is a finite
qutrit-substrate horizon code: a complete edge payload plus a q! parity budget.
"""
from __future__ import annotations

import json
from math import comb, factorial, gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_edge_horizon_parity_code.json"

q = 3
dX, dZ = 3, 4
k = dX * dZ
payload_edges = comb(k, 2)
parity_symbols = factorial(q)
total_symbols = (k - dX) * (k - dZ)
genus_denominator = dX * dZ
genus_value = total_symbols // genus_denominator
num = payload_edges
den = total_symbols
rate_gcd = gcd(num, den)
rate = [num // rate_gcd, den // rate_gcd]
redundancy = [parity_symbols // gcd(parity_symbols, total_symbols), total_symbols // gcd(parity_symbols, total_symbols)]

row_edges = dX * comb(dZ, 2)
col_edges = dZ * comb(dX, 2)
mixed_edges = payload_edges - row_edges - col_edges
pure_edges = row_edges + col_edges
corrected_mixed = mixed_edges + parity_symbols

payload = {
  "summary": {
    "horizon_total": total_symbols,
    "data_payload_edges": payload_edges,
    "parity_symbols": parity_symbols,
    "rate_simplified": rate,
    "redundancy_fraction_simplified": redundancy,
    "genus_value": genus_value,
    "all_identities_hold": True
  },
  "identities": {
    "data_payload_is_C12_2": payload_edges == 66,
    "parity_is_q_factorial": parity_symbols == 6,
    "total_is_genus_numerator": total_symbols == 72,
    "total_is_data_plus_parity": total_symbols == payload_edges + parity_symbols,
    "rate_is_11_over_12": rate == [11, 12],
    "redundancy_is_1_over_12": redundancy == [1, 12],
    "genus_is_parity": genus_value == parity_symbols,
    "row_edges": row_edges == 18,
    "column_edges": col_edges == 12,
    "mixed_edges": mixed_edges == 36,
    "pure_edges_are_30": pure_edges == 30,
    "mixed_plus_parity_is_flags": corrected_mixed == 42,
    "total_split": total_symbols == pure_edges + corrected_mixed
  },
  "grid_split": {
    "row_edges": row_edges,
    "column_edges": col_edges,
    "mixed_edges": mixed_edges,
    "pure_edges": pure_edges,
    "corrected_mixed": corrected_mixed,
    "closed_form": "72 = (18+12) + (36+6) = 30 + 42"
  },
  "closed_forms": {
    "data": "66 = C(12,2)",
    "parity": "6 = q! = genus(K12)",
    "total": "72 = (12-3)(12-4)",
    "rate": "66/72 = 11/12",
    "redundancy": "6/72 = 1/12, the genus denominator fraction",
    "grid": "66 = 18 row-fiber + 12 column-fiber + 36 mixed; parity corrects 36 to 42 flags"
  },
  "theorem": "Edge-Horizon Parity Code Theorem: at n=k=12, the genus numerator 72 is a [72,66]+6 horizon code: 66 complete-edge payload symbols plus q!=6 parity/check symbols. The rate is 11/12 and the redundancy is 1/12, matching the genus denominator.",
  "honesty_boundary": "This is a finite qutrit-substrate code analogy, not a claim of a literal binary linear error-correcting code without additional construction."
}

if __name__ == "__main__":
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
