#!/usr/bin/env python3
"""
PART CLXIII - Decimal Reptend Compiler
=====================================

User hint:
    1/7 = 0.142857142857...
    The reptend 142857 contains the one-digit terminating-denominator set
    {1,2,4,5,8}, with 7 itself as the cyclic denominator.  The missing
    one-digit denominators are {3,6,9}.  In mod 12, 3,6,9 cut the wheel into
    quarters, with 6 as the middle/rank transition and 7 as the next cyclic
    number after the middle.

This module formalizes that hint in W(3,3) atoms.

The key identity is not base-ten numerology.  In the W33 compiler,

    Phi4 = q^2 + 1 = 10      (the bridge/base)
    Phi6 = q^2 - q + 1 = 7   (the threshold/cyclic denominator)
    2q   = 6                 (the rank seed)

The repeating decimal of 1/7 is the base-Phi4 expansion of 1/Phi6.
Its period is the multiplicative order

    ord_{Phi6}(Phi4) = ord_7(10) = 6 = 2q.

Therefore

    1/Phi6 in base Phi4 has reptend length 2q,

and the reptend is

    R = (Phi4^(2q)-1)/Phi6 = (10^6-1)/7 = 142857.

The cyclic fraction 1/7 is thus the decimal shadow of the same structure
seen in CLX-CLXII:

    base = Phi4 = 10,
    denominator = Phi6 = 7,
    period = 2q = 6,
    reptend = 142857.

The missing decimal denominators {3,6,9} are exactly {q,2q,q^2}.  They are
not absent randomly: they are the q-clock/rank-square axis.  The middle value
6=2q is also the Cartan rank seed and the value q! from q!=2q.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Set

ROOT = Path(__file__).resolve().parent

Q = 3
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
RANK_SEED = 2 * Q
Q_SQUARE = Q * Q
BASE = PHI4
DEN = PHI6


def multiplicative_order(a: int, n: int) -> int:
    if math.gcd(a, n) != 1:
        raise ValueError("multiplicative order requires gcd(a,n)=1")
    x = a % n
    k = 1
    while x != 1:
        x = (x * a) % n
        k += 1
    return k


def reptend(numer: int, denom: int, base: int = BASE) -> str:
    """Return the repeating block for numer/denom in the given base.

    Assumes gcd(base, denom)=1 and pure periodicity for the denominator.
    For 1/7 in base 10 this returns '142857'.
    """
    rem = numer % denom
    seen = {}
    digits: List[int] = []
    while rem not in seen:
        seen[rem] = len(digits)
        rem *= base
        digits.append(rem // denom)
        rem %= denom
    start = seen[rem]
    block = digits[start:]
    return "".join(str(d) for d in block)


def decimal_kind(denom: int, base: int = BASE) -> str:
    """Classify 1/denom in base 10-like base as terminating/mixed/pure-periodic."""
    d = denom
    g = math.gcd(d, base)
    while g > 1:
        while d % g == 0:
            d //= g
        g = math.gcd(d, base)
    if d == 1:
        return "terminating"
    if math.gcd(denom, base) > 1:
        return "mixed preperiodic"
    return "pure periodic"


def terminating_denominators_1_to_9() -> List[int]:
    return [n for n in range(1, 10) if decimal_kind(n) == "terminating"]


def q_axis_denominators_1_to_9() -> List[int]:
    return [Q, RANK_SEED, Q_SQUARE]


def rotations_of_reptend(block: str) -> List[str]:
    return [block[i:] + block[:i] for i in range(len(block))]


@dataclass(frozen=True)
class ReptendMultiple:
    numerator: int
    fraction: str
    block: str
    is_rotation: bool


def reptend_multiples() -> List[ReptendMultiple]:
    base_block = reptend(1, DEN)
    rots = set(rotations_of_reptend(base_block))
    rows = []
    for m in range(1, DEN):
        b = reptend(m, DEN)
        rows.append(ReptendMultiple(m, f"{m}/{DEN}", b, b in rots))
    return rows


@dataclass(frozen=True)
class DecimalDenominatorRow:
    denominator: int
    fraction: str
    kind: str
    w33_role: str


def decimal_denominator_rows() -> List[DecimalDenominatorRow]:
    roles = {
        1: "unit",
        2: "binary/base factor",
        3: "q-clock fixed repetend axis",
        4: "mu/base-square terminating factor",
        5: "stabilizer residue / threshold numerator",
        6: "2q rank transition: mixed base factor and q-clock",
        7: "Phi6 cyclic threshold denominator",
        8: "inverse residue / carrier numerator",
        9: "q^2 fixed repetend square axis",
    }
    return [DecimalDenominatorRow(n, f"1/{n}", decimal_kind(n), roles[n]) for n in range(1, 10)]


def decimal_reptend_compiler_audit() -> Dict[str, object]:
    block = reptend(1, DEN)
    period = multiplicative_order(BASE, DEN)
    digits = {int(ch) for ch in block}
    terminating = set(terminating_denominators_1_to_9())
    q_axis = set(q_axis_denominators_1_to_9())
    multiples = reptend_multiples()

    checks = {
        "base_is_phi4": BASE == PHI4 == 10,
        "denominator_is_phi6": DEN == PHI6 == 7,
        "period_is_2q": period == RANK_SEED == 6,
        "reptend_is_142857": block == "142857",
        "reptend_formula": int(block) == (BASE ** RANK_SEED - 1) // DEN == 142857,
        "seven_times_reptend_is_all_nines": DEN * int(block) == BASE ** RANK_SEED - 1 == 999999,
        "terminating_denominators_are_subset_of_reptend_digits": terminating.issubset(digits),
        "terminating_denominators_expected": terminating == {1, 2, 4, 5, 8},
        "q_axis_missing_denominators": q_axis == {3, 6, 9},
        "q_axis_disjoint_from_terminating": terminating.isdisjoint(q_axis),
        "q_axis_plus_terminating_plus_cyclic_is_1_to_9": terminating | q_axis | {DEN} == set(range(1, 10)),
        "six_is_rank_middle_transition": RANK_SEED == 6 == math.factorial(Q),
        "seven_follows_rank_seed": DEN == RANK_SEED + 1 == 7,
        "multiples_are_rotations": all(m.is_rotation for m in multiples),
        "mod12_quarter_markers": {Q, RANK_SEED, Q_SQUARE, 12} == {3, 6, 9, 12},
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXIII_DECIMAL_REPTEND_COMPILER",
        "source_hint": "user decimal-cycle observation: 1/7 reptend 142857, missing 3/6/9, mod-12 quarters, 6 middle and 7 first cyclic after middle",
        "w33_atoms": {
            "q": Q,
            "Phi3": PHI3,
            "Phi4_base": PHI4,
            "Phi6_denominator": PHI6,
            "rank_seed_2q": RANK_SEED,
            "q_square": Q_SQUARE,
        },
        "reptend_core": {
            "base": BASE,
            "denominator": DEN,
            "period_ord_den_base": period,
            "reptend": block,
            "formula": "R=(Phi4^(2q)-1)/Phi6",
            "formula_value": str((BASE ** RANK_SEED - 1) // DEN),
            "all_nines_identity": "7*142857=999999=10^6-1",
        },
        "digit_partition_1_to_9": {
            "terminating_denominators": sorted(terminating),
            "cyclic_denominator": DEN,
            "q_axis_missing_denominators": sorted(q_axis),
            "interpretation": "1..9 partitions into terminating digits {1,2,4,5,8}, cyclic Phi6 denominator {7}, and q-axis {3,6,9}.",
        },
        "decimal_denominator_rows": [asdict(r) for r in decimal_denominator_rows()],
        "reptend_multiples": [asdict(m) for m in multiples],
        "mod12_quarter_axis": {
            "markers": [Q, RANK_SEED, Q_SQUARE, 12],
            "quarters": ["1-2-3", "4-5-6", "7-8-9", "10-11-12"],
            "middle_transition": "6=2q=q! is the rank seed; 7=Phi6 is the cyclic threshold immediately after it.",
        },
        "checks": checks,
        "theorem_statement": (
            "The decimal cycle 1/7=0.overline{142857} is the base-Phi4 expansion of "
            "1/Phi6, and its period is ord_{Phi6}(Phi4)=2q=6.  The reptend is "
            "R=(Phi4^(2q)-1)/Phi6=142857.  Among denominators 1..9, the terminating "
            "set {1,2,4,5,8} appears inside the reptend, while the missing set {3,6,9} "
            "is exactly {q,2q,q^2}, the q-clock/rank-square axis."
        ),
        "interpretive_note": (
            "This connects the user decimal hint to the W33 compiler: base ten is Phi4, "
            "the cyclic denominator seven is Phi6, and the six-digit period is the Cartan "
            "rank seed 2q.  The point after the middle, 7, is cyclic because Phi4 has full "
            "order 2q modulo Phi6."
        ),
    }


def main() -> int:
    audit = decimal_reptend_compiler_audit()
    out = ROOT / "PART_CLXIII_decimal_reptend_compiler_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
