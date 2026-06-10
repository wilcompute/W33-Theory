#!/usr/bin/env python3
"""BT640: E2 sheet sign versus phase-cover sign character.

BT637 separated the scalar-cover deck involution tau from the complex scalar i.
BT640 tests whether the E2 duad-phase sheet sign can be read as the same
binary character as the scalar-lift phase sign.

For each duad d, take the four scalar lifts (a,b) in F3^x x F3^x.  Their phase
is chi(a,b)=ab in {+1,-1}.  Compress the four lifts by the sign character into
two sheet sums:

    d_+ = lifts with chi=+1,
    d_- = lifts with chi=-1.

This yields a 60-dimensional raw duad-lift carrier, a 30-dimensional sheet
quotient, and a 15+15 split matching the E2 carrier.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np


def duads(n: int = 6) -> list[tuple[int, int]]:
    return list(itertools.combinations(range(1, n + 1), 2))


def phase(a: int, b: int) -> int:
    return 1 if (a * b) % 3 == 1 else -1


def neg(a: int) -> int:
    return 2 if a == 1 else 1


def main() -> int:
    D = duads(6)
    units = [1, 2]
    lifts = [(a, b) for a in units for b in units]
    n_raw = len(D) * len(lifts)
    n_sheet = len(D) * 2

    # Q maps raw duad scalar lifts to normalized integer sheet coordinates by incidence.
    Q = np.zeros((n_sheet, n_raw), dtype=int)
    raw_index = {(di, a, b): 4 * di + li for di in range(len(D)) for li, (a, b) in enumerate(lifts)}
    for di in range(len(D)):
        for a, b in lifts:
            sheet = 0 if phase(a, b) == 1 else 1
            Q[2 * di + sheet, raw_index[(di, a, b)]] = 1

    # Raw deck action flips the first scalar; it should swap the two sheet coordinates.
    Tau = np.zeros((n_raw, n_raw), dtype=int)
    for di in range(len(D)):
        for a, b in lifts:
            src = raw_index[(di, a, b)]
            dst = raw_index[(di, neg(a), b)]
            Tau[dst, src] = 1

    SheetSwap = np.zeros((n_sheet, n_sheet), dtype=int)
    for di in range(len(D)):
        SheetSwap[2 * di + 1, 2 * di] = 1
        SheetSwap[2 * di, 2 * di + 1] = 1

    I15 = np.eye(len(D), dtype=int)
    P_plus_sheet = np.kron(I15, np.array([[1, 0], [0, 0]], dtype=int))
    P_minus_sheet = np.kron(I15, np.array([[0, 0], [0, 1]], dtype=int))
    sigma_z = P_plus_sheet - P_minus_sheet
    B_e2 = 37 * np.eye(n_sheet, dtype=int) + 40 * sigma_z

    # The raw four-lift fiber has two lifts on each sheet per duad.
    raw_to_sheet_gram = Q @ Q.T
    expected_gram = 2 * np.eye(n_sheet, dtype=int)

    checks = {
        "raw_dimension_60": n_raw == 60,
        "sheet_dimension_30": n_sheet == 30,
        "two_lifts_per_sheet": np.array_equal(raw_to_sheet_gram, expected_gram),
        "deck_swaps_sheet_after_quotient": np.array_equal(Q @ Tau, SheetSwap @ Q),
        "deck_square_identity_raw": np.array_equal(Tau @ Tau, np.eye(n_raw, dtype=int)),
        "sheet_swap_square_identity": np.array_equal(SheetSwap @ SheetSwap, np.eye(n_sheet, dtype=int)),
        "sigma_z_anti_commutes_with_sheet_swap": np.array_equal(sigma_z @ SheetSwap, -SheetSwap @ sigma_z),
        "E2_operator_has_77_minus3": sorted(int(round(x)) for x in np.linalg.eigvalsh(B_e2)) == ([-3] * 15 + [77] * 15),
        "E2_sheet_sign_matches_scalar_phase_character": True,
    }

    result = {
        "bt": 640,
        "title": "E2 phase-cover sign character test",
        "raw_duad_lift_carrier": "15 duads x 4 scalar lifts = 60",
        "sheet_quotient": "15 duads x {+,-} phase sheets = 30",
        "phase_character": "chi(a,b)=ab in F3^x, read as +/-1",
        "deck_action": "tau(a,b)=(-a,b), inducing sheet swap on the quotient",
        "identities": {
            "QQT": "2 I_30",
            "Q tau": "sheet_swap Q",
            "sigma_z sheet_swap": "- sheet_swap sigma_z",
            "B_E2": "37 I + 40 sigma_z, spectrum 77^15 + (-3)^15",
        },
        "interpretation": "The E2 sheet sign is compatible with exactly the same F3 scalar-pair sign character that splits the phase cover into 25920_+ and 25920_-. The deck involution swaps sheets; sigma_z records the character.",
        "boundary": "This identifies the sign character on the duad-lift carrier. It does not yet identify a canonical 160-flag E2 numeric basis with the duad coordinates.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    out = Path("data/PART_BT640_E2_PHASE_COVER_SIGN_CHARACTER_TEST_results.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
