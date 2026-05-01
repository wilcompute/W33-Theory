#!/usr/bin/env python3
"""
PART CXLVI — Fibonacci E6 Mixer
===============================

CXLV identified the 78-dimensional Ramanujan shell as a two-adjoint compiler:

    complex multiplicities: 24 + 15 = 39 = 3*Phi3
    real dimensions:        48 + 30 = 78 = 6*Phi3

The deeper invariant is that the split reduces to

    24 : 15 = 48 : 30 = 8 : 5,

and

    8 + 5 = 13 = Phi3(3).

So the Ramanujan/E6 compiler is normalized by the Fibonacci-type weights

    carrier weight   = 8/13
    threshold weight = 5/13

with three-generation lift

    3*(8/13) = 24/13 = k3_bare
    3*(5/13) = 15/13 = negative-sector companion.

This explains why the successful QCD bare embedding is 24/13: it is not merely
multiplicity divided by Phi3; it is the q-generation lift of the positive
Fibonacci mixer weight.

The same mixer also exposes a natural electroweak-looking residual:

    (8 - 5)/13 = 3/13 = q/Phi3.

This is precisely the W(3,3) q/Phi3 angle that has appeared elsewhere in the
repo as an electroweak-scale diagnostic.  In this reading, q/Phi3 is the
imbalance of the two E6/Ramanujan compiler weights.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent

Q = 3
PHI3 = Q * Q + Q + 1
POSITIVE_COMPLEX = 24
NEGATIVE_COMPLEX = 15
POSITIVE_REAL = 2 * POSITIVE_COMPLEX
NEGATIVE_REAL = 2 * NEGATIVE_COMPLEX
COMPLEX_TOTAL = POSITIVE_COMPLEX + NEGATIVE_COMPLEX
REAL_TOTAL = POSITIVE_REAL + NEGATIVE_REAL

# Reduced mixer weights.
CARRIER_NUM = 8
THRESHOLD_NUM = 5
MIXER_DEN = CARRIER_NUM + THRESHOLD_NUM


@dataclass(frozen=True)
class MixerComponent:
    name: str
    raw_complex_dim: int
    raw_real_dim: int
    reduced_weight: str
    normalized_weight: str
    generation_lift: str
    physical_role: str


def components() -> List[MixerComponent]:
    return [
        MixerComponent(
            name="carrier / positive Q(sqrt(-10)) sector",
            raw_complex_dim=POSITIVE_COMPLEX,
            raw_real_dim=POSITIVE_REAL,
            reduced_weight="8",
            normalized_weight="8/13",
            generation_lift="3*(8/13)=24/13",
            physical_role="bare carrier factor k3_bare=24/13",
        ),
        MixerComponent(
            name="threshold / negative Q(sqrt(-7)) sector",
            raw_complex_dim=NEGATIVE_COMPLEX,
            raw_real_dim=NEGATIVE_REAL,
            reduced_weight="5",
            normalized_weight="5/13",
            generation_lift="3*(5/13)=15/13",
            physical_role="negative-sector companion and QCD threshold field",
        ),
    ]


def reduce_ratio(a: int, b: int) -> tuple[int, int]:
    from math import gcd
    g = gcd(a, b)
    return a // g, b // g


def carrier_weight() -> Fraction:
    return Fraction(CARRIER_NUM, MIXER_DEN)


def threshold_weight() -> Fraction:
    return Fraction(THRESHOLD_NUM, MIXER_DEN)


def imbalance_weight() -> Fraction:
    return carrier_weight() - threshold_weight()


def q_generation_lift(weight: Fraction) -> Fraction:
    return Q * weight


def fibonacci_e6_mixer_audit() -> Dict[str, object]:
    complex_ratio = reduce_ratio(POSITIVE_COMPLEX, NEGATIVE_COMPLEX)
    real_ratio = reduce_ratio(POSITIVE_REAL, NEGATIVE_REAL)
    cw = carrier_weight()
    tw = threshold_weight()
    iw = imbalance_weight()
    k3_bare = q_generation_lift(cw)
    negative_companion = q_generation_lift(tw)

    checks = {
        "complex_ratio_reduces_to_8_5": complex_ratio == (8, 5),
        "real_ratio_reduces_to_8_5": real_ratio == (8, 5),
        "mixer_denominator_is_Phi3": MIXER_DEN == PHI3,
        "carrier_plus_threshold_is_one": cw + tw == 1,
        "imbalance_is_q_over_Phi3": iw == Fraction(Q, PHI3),
        "q_lift_carrier_is_24_over_13": k3_bare == Fraction(24, 13),
        "q_lift_threshold_is_15_over_13": negative_companion == Fraction(15, 13),
        "complex_total_is_3Phi3": COMPLEX_TOTAL == Q * PHI3,
        "real_total_is_6Phi3": REAL_TOTAL == 2 * Q * PHI3,
    }
    assert all(checks.values())

    return {
        "module": "PART_CXLVI_FIBONACCI_E6_MIXER",
        "raw_shell": {
            "positive_complex": POSITIVE_COMPLEX,
            "negative_complex": NEGATIVE_COMPLEX,
            "positive_real": POSITIVE_REAL,
            "negative_real": NEGATIVE_REAL,
            "complex_total": COMPLEX_TOTAL,
            "real_total": REAL_TOTAL,
        },
        "reduced_mixer": {
            "ratio": "8:5",
            "denominator": MIXER_DEN,
            "denominator_identification": "Phi3(3)=13",
            "carrier_weight": str(cw),
            "threshold_weight": str(tw),
            "imbalance_weight": str(iw),
        },
        "components": [asdict(c) for c in components()],
        "generation_lifts": {
            "q_times_carrier": str(k3_bare),
            "q_times_threshold": str(negative_companion),
            "q_times_imbalance": str(q_generation_lift(iw)),
        },
        "electroweak_diagnostic": {
            "mixer_imbalance": "8/13 - 5/13 = 3/13 = q/Phi3",
            "interpretation": "q/Phi3 is the imbalance of the two Ramanujan/E6 compiler weights",
        },
        "checks": checks,
        "theorem_statement": (
            "The 24:15 Ramanujan/E6 compiler split reduces to the Fibonacci mixer "
            "8:5 with denominator 13=Phi3.  The successful QCD bare factor "
            "24/13 is the q-generation lift of the carrier weight 8/13, while "
            "the companion threshold sector is the q-generation lift 15/13 of "
            "the threshold weight 5/13.  Their normalized imbalance is 3/13=q/Phi3."
        ),
        "interpretive_note": (
            "This turns the two-sector compiler into a mixing rule.  The shell does "
            "not merely contain dimensions 24 and 15; it normalizes them into the "
            "weights 8/13 and 5/13.  QCD uses the q-lifted carrier weight, while "
            "electroweak-like diagnostics naturally see the carrier-threshold "
            "imbalance q/Phi3."
        ),
    }


def main() -> int:
    audit = fibonacci_e6_mixer_audit()
    out = ROOT / "PART_CXLVI_fibonacci_e6_mixer_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
