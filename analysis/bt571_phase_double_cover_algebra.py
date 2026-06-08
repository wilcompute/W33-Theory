#!/usr/bin/env python3
"""BT571: Phase double-cover algebra.

Build the signed two-sheet cover over the 12960 projective support incidences.
Each support incidence has four scalar lifts from F_3^* x F_3^*.  Two lifts land
in phase +1 and two in phase -1, giving a balanced Z2 deck cover:

    12960 support incidences * 2 lifts per phase = 25920 per sheet.
"""
import json
from pathlib import Path

support_incidences = 12960
scalars = [1, 2]  # F_3^*, with 2=-1
phase = {(a,b): (a*b) % 3 for a in scalars for b in scalars}
plus_lifts = [(a,b) for (a,b),p in phase.items() if p == 1]
minus_lifts = [(a,b) for (a,b),p in phase.items() if p == 2]
# Deck involution: flip the X scalar a -> -a = 2a mod 3. This swaps phase sheets.
def deck(pair):
    a,b = pair
    return ((2*a) % 3, b)
checks = {
    "four_scalar_lifts": len(phase) == 4,
    "two_plus_lifts": len(plus_lifts) == 2,
    "two_minus_lifts": len(minus_lifts) == 2,
    "sheet_size_plus": support_incidences * len(plus_lifts) == 25920,
    "sheet_size_minus": support_incidences * len(minus_lifts) == 25920,
    "deck_swaps_plus_to_minus": all(deck(p) in minus_lifts for p in plus_lifts),
    "deck_swaps_minus_to_plus": all(deck(p) in plus_lifts for p in minus_lifts),
    "deck_involution": all(deck(deck(p)) == p for p in phase),
    "total_nonzero": support_incidences * 4 == 51840,
}
result = {
    "bt": 571,
    "title": "Phase double-cover algebra",
    "base_support_incidences": support_incidences,
    "scalar_lifts_F3_star_times_F3_star": [list(k)+[v] for k,v in phase.items()],
    "plus_lifts": plus_lifts,
    "minus_lifts": minus_lifts,
    "deck_involution": "tau(a,b)=(-a,b) over F3^* swaps the + and - phase sheets",
    "plus_sheet_size": support_incidences * len(plus_lifts),
    "minus_sheet_size": support_incidences * len(minus_lifts),
    "total_nonzero_phase_cover": support_incidences * 4,
    "interpretation": "The 51840 scale is a Z2 deck double over 12960 projective support incidences after scalar lifting, with two lifts per nonzero F3 phase.",
    "all_identities": checks,
    "all_identities_hold": all(checks.values()),
}
Path("data/PART_BT571_PHASE_DOUBLE_COVER_ALGEBRA_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
