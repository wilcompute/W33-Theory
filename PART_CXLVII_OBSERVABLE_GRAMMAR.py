#!/usr/bin/env python3
"""
PART CXLVII — Observable Grammar from the Fibonacci E6 Mixer
===========================================================

CXLVI found the normalized Ramanujan/E6 mixer

    carrier   C = 8/13
    threshold T = 5/13
    imbalance D = C - T = 3/13 = q/Phi3.

This module turns that mixer into a small exact observable grammar.

Base tokens:
    C = 8/13             carrier weight, Q(sqrt(-10)) / su(5) sector
    T = 5/13             threshold weight, Q(sqrt(-7)) / so(6) sector
    D = C - T = 3/13     carrier-threshold imbalance

Immediate grammar operations:
    C + T = 1
    1 - D = 10/13 = Phi4/Phi3
    1 + D = 16/13 = (k+mu)/Phi3
    q*C = 24/13         QCD bare factor
    q*T = 15/13         negative-sector companion
    q*D = 9/13          q-lifted imbalance

Interpretation:
    QCD sees the q-lifted carrier plus the Phi6 threshold.
    Electroweak-like diagnostics see the imbalance D = 3/13.
    Phi4-like/Ko-dimensional diagnostics see the complement 1-D = 10/13.
    Heavy-sector diagnostics see 1+D = 16/13, the normalized k+mu branch.

The purpose is not to assert every token is already physical.  The purpose is
to give the theory a finite, testable grammar for classifying observables by
which operation they apply to the same E6/Ramanujan mixer.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent

Q = 3
MU = 4
K = 12
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1

CARRIER = Fraction(8, PHI3)
THRESHOLD = Fraction(5, PHI3)
IMBALANCE = CARRIER - THRESHOLD


@dataclass(frozen=True)
class GrammarToken:
    name: str
    expression: str
    value: str
    decimal: float
    classification: str
    proposed_observable_role: str


def token(name: str, expression: str, value: Fraction, classification: str, role: str) -> GrammarToken:
    return GrammarToken(
        name=name,
        expression=expression,
        value=str(value),
        decimal=float(value),
        classification=classification,
        proposed_observable_role=role,
    )


def grammar_tokens() -> List[GrammarToken]:
    return [
        token(
            "carrier_weight",
            "C = 8/13",
            CARRIER,
            "base mixer token",
            "positive Q(sqrt(-10)) / su(5) carrier weight",
        ),
        token(
            "threshold_weight",
            "T = 5/13",
            THRESHOLD,
            "base mixer token",
            "negative Q(sqrt(-7)) / so(6) threshold weight",
        ),
        token(
            "imbalance",
            "D = C-T = 3/13 = q/Phi3",
            IMBALANCE,
            "difference token",
            "electroweak-like carrier-threshold imbalance",
        ),
        token(
            "phi4_complement",
            "1-D = 10/13 = Phi4/Phi3",
            1 - IMBALANCE,
            "complement token",
            "Phi4/Ko-dimensional complement of the imbalance",
        ),
        token(
            "heavy_plus_branch",
            "1+D = 16/13 = (k+mu)/Phi3",
            1 + IMBALANCE,
            "sum token",
            "heavy-sector normalized k+mu branch",
        ),
        token(
            "q_lift_carrier",
            "q*C = 24/13",
            Q * CARRIER,
            "q-lift token",
            "QCD bare embedding factor k3_bare",
        ),
        token(
            "q_lift_threshold",
            "q*T = 15/13",
            Q * THRESHOLD,
            "q-lift token",
            "negative-sector companion",
        ),
        token(
            "q_lift_imbalance",
            "q*D = 9/13",
            Q * IMBALANCE,
            "q-lift token",
            "q-lifted electroweak/imbalance companion",
        ),
    ]


def grammar_relations() -> Dict[str, str]:
    return {
        "normalization": "C + T = 1",
        "imbalance": "C - T = D = q/Phi3 = 3/13",
        "phi4_complement": "1 - D = Phi4/Phi3 = 10/13",
        "heavy_plus_branch": "1 + D = (k+mu)/Phi3 = 16/13",
        "q_lift_sum": "q*C + q*T = q = 3",
        "qcd_bare_factor": "q*C = 24/13",
        "threshold_companion": "q*T = 15/13",
        "lifted_imbalance": "q*D = 9/13",
        "fibonacci_ratio": "C/T = 8/5",
    }


def exact_checks() -> Dict[str, bool]:
    return {
        "carrier_plus_threshold_is_one": CARRIER + THRESHOLD == 1,
        "imbalance_is_q_over_phi3": IMBALANCE == Fraction(Q, PHI3),
        "phi4_complement_is_phi4_over_phi3": 1 - IMBALANCE == Fraction(PHI4, PHI3),
        "heavy_plus_is_k_plus_mu_over_phi3": 1 + IMBALANCE == Fraction(K + MU, PHI3),
        "q_lift_carrier_is_24_over_13": Q * CARRIER == Fraction(24, 13),
        "q_lift_threshold_is_15_over_13": Q * THRESHOLD == Fraction(15, 13),
        "q_lift_imbalance_is_9_over_13": Q * IMBALANCE == Fraction(9, 13),
        "q_lift_sum_is_q": Q * CARRIER + Q * THRESHOLD == Q,
        "fibonacci_ratio_is_8_over_5": CARRIER / THRESHOLD == Fraction(8, 5),
    }


def observable_grammar_audit() -> Dict[str, object]:
    checks = exact_checks()
    assert all(checks.values())

    return {
        "module": "PART_CXLVII_OBSERVABLE_GRAMMAR",
        "w33_atoms": {
            "q": Q,
            "k": K,
            "mu": MU,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
        },
        "base_mixer": {
            "carrier": str(CARRIER),
            "threshold": str(THRESHOLD),
            "imbalance": str(IMBALANCE),
            "ratio": "8:5",
        },
        "tokens": [asdict(t) for t in grammar_tokens()],
        "relations": grammar_relations(),
        "checks": checks,
        "theorem_statement": (
            "The Fibonacci E6 mixer generates a finite observable grammar from "
            "C=8/13 and T=5/13.  QCD uses the q-lifted carrier qC=24/13; "
            "electroweak-like diagnostics use the imbalance D=C-T=3/13=q/Phi3; "
            "Phi4/Ko diagnostics use the complement 1-D=10/13=Phi4/Phi3; and "
            "heavy-sector diagnostics use 1+D=16/13=(k+mu)/Phi3."
        ),
        "interpretive_note": (
            "This grammar gives the program a non-arbitrary classification system. "
            "Instead of hunting isolated constants, each observable should be tested "
            "as a base token, complement, imbalance, q-lift, or q-lifted imbalance "
            "of the same Ramanujan/E6 carrier-threshold mixer."
        ),
    }


def main() -> int:
    audit = observable_grammar_audit()
    out = ROOT / "PART_CXLVII_observable_grammar_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
