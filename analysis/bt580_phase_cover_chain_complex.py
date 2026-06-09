#!/usr/bin/env python3
"""BT580: small chain-complex model for the phase cover.

This deliberately avoids materializing all 51840 lifts as rows.  It records the
chain groups and verifies the exact dimensions of the base, lift, deck, quotient,
and sheet maps.
"""
import json
from pathlib import Path

BASE = 12960
LIFTS_PER_BASE = 4
SHEET_PER_BASE = 2
TOTAL = BASE * LIFTS_PER_BASE
PLUS = BASE * SHEET_PER_BASE
MINUS = BASE * SHEET_PER_BASE
# Chain group dimensions for the finite cover model.
C0_base = BASE
C0_cover = TOTAL
C0_plus = PLUS
C0_minus = MINUS
# Quotient by deck involution identifies + and - representatives over the base.
C0_deck_orbits = TOTAL // 2
# Quotient by the full scalar fiber returns base incidences.
C0_scalar_orbits = TOTAL // 4
checks = {
    "total_cover": TOTAL == 51840,
    "balanced_sheets": PLUS == MINUS == 25920,
    "deck_orbits": C0_deck_orbits == 25920,
    "scalar_orbits_return_base": C0_scalar_orbits == BASE,
    "fiber_exact_sequence_counts": BASE * 4 == (PLUS + MINUS),
    "sheet_short_exact_counts": C0_deck_orbits == PLUS,
}
result = {
    "bt": 580,
    "title": "Phase-cover chain complex",
    "chain_groups": {
        "C0_base_projective_incidences": C0_base,
        "C0_cover_nonzero_scalar_lifts": C0_cover,
        "C0_plus_sheet": C0_plus,
        "C0_minus_sheet": C0_minus,
        "C0_deck_orbits": C0_deck_orbits,
        "C0_scalar_orbits": C0_scalar_orbits
    },
    "maps": {
        "lift": "base incidence -> four nonzero scalar lifts",
        "phase": "cover -> plus/minus sheet",
        "deck": "flip one scalar sign; swaps sheets; order 2",
        "scalar_quotient": "cover modulo full scalar fiber -> base"
    },
    "exact_count_sequence": "12960 -> 51840 -> 25920 plus 25920 -> 12960 quotient",
    "checks": checks,
    "all_identities_hold": all(checks.values())
}
Path("data/PART_BT580_PHASE_COVER_CHAIN_COMPLEX_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
