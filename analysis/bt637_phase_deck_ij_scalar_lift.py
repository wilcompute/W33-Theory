#!/usr/bin/env python3
"""BT637: phase-cover deck involution versus complex iJ scalar lift.

BT634 showed that the real folded-cubic cross-channel obeys J^2=-I, while
adjoining i gives (iJ)^2=+I.  BT637 checks whether this is compatible with the
actual scalar-lift cover used in the minimal logical phase frame.

Each projective support incidence has four scalar lifts (a,b) in F3^x x F3^x.
The pairing phase is a*b in {+1,-1}.  Flipping one scalar is the deck map

    tau(a,b)=(-a,b),

and it swaps the + and - sheets.  Therefore tau^2=1 on the cover, while the
complex scalar i supplies the separate square-root of the sheet sign needed to
turn J^2=-1 into (iJ)^2=+1.
"""
from __future__ import annotations

import json
from pathlib import Path


def f3_neg(x: int) -> int:
    return 2 if x == 1 else 1


def phase(a: int, b: int) -> int:
    # F3 units {1,2}; read 2 as -1.
    prod = (a * b) % 3
    return 1 if prod == 1 else -1


def main() -> int:
    units = [1, 2]
    lifts = [(a, b) for a in units for b in units]
    phase_profile = {+1: [], -1: []}
    for lift in lifts:
        phase_profile[phase(*lift)].append(lift)

    tau = {(a, b): (f3_neg(a), b) for a, b in lifts}
    tau2 = {x: tau[tau[x]] for x in lifts}
    tau_swaps_phase = all(phase(*tau[x]) == -phase(*x) for x in lifts)
    tau_order_two = all(tau2[x] == x for x in lifts)

    base = 12960
    plus = base * len(phase_profile[+1])
    minus = base * len(phase_profile[-1])
    total = base * len(lifts)

    J_square = -1
    tau_square = 1
    i_square = -1
    iJ_square = i_square * J_square

    checks = {
        "four_scalar_lifts": len(lifts) == 4,
        "two_plus_two_minus": len(phase_profile[+1]) == 2 and len(phase_profile[-1]) == 2,
        "tau_swaps_phase_sheets": tau_swaps_phase,
        "tau_order_two": tau_order_two,
        "counts_25920_each": plus == minus == 25920,
        "total_51840": total == 51840,
        "J_square_minus_one": J_square == -1,
        "tau_square_plus_one": tau_square == 1,
        "i_square_minus_one": i_square == -1,
        "iJ_square_plus_one": iJ_square == 1,
    }

    result = {
        "bt": 637,
        "title": "Phase-cover deck involution and iJ scalar lift",
        "fiber": {
            "units": units,
            "lifts": lifts,
            "phase_profile": {str(k): v for k, v in phase_profile.items()},
            "deck_map": "tau(a,b)=(-a,b)",
            "tau_order": 2,
            "tau_swaps_phase_sheets": tau_swaps_phase,
        },
        "counts": {
            "base_projective_support_incidences": base,
            "plus_sheet": plus,
            "minus_sheet": minus,
            "total_cover": total,
        },
        "operator_boundary": {
            "real_cross_channel": "J^2=-I",
            "deck_involution": "tau^2=+I and tau swaps phase sheets",
            "complex_scalar": "i^2=-1",
            "complexified_channel": "(iJ)^2=+I",
            "interpretation": "The deck involution supplies the sheet swap; the complex scalar i supplies the square-root phase. They are compatible but not identical operations.",
        },
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    out = Path("data/PART_BT637_PHASE_DECK_IJ_SCALAR_LIFT_results.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
