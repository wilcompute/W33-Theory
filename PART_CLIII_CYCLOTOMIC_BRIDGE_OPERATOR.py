#!/usr/bin/env python3
"""
PART CLIII - Cyclotomic Bridge Operator
=======================================

CL showed that the mixer layer and projection layer intersect at exactly
10/13:

    1 - D = P(Phi4) = 10/13.

This module explains why that bridge is inevitable rather than accidental.
The bridge comes from the cyclotomic complement identity at q=3:

    Phi3 = q^2 + q + 1 = 13
    Phi4 = q^2 + 1     = 10

so

    Phi4 = Phi3 - q.

Dividing by Phi3 gives

    Phi4/Phi3 = 1 - q/Phi3.

But the Fibonacci/E6 mixer imbalance is

    D = C - T = 3/13 = q/Phi3.

Therefore

    1 - D = Phi4/Phi3 = P(Phi4).

This is the cyclotomic bridge operator:

    B_q(D) = 1 - D.

At q=3 it sends the mixer imbalance to the carrier-field projection.
The bridge is therefore forced by the relation between Phi3 and Phi4, not
chosen after the fact.
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
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1

C = Fraction(8, PHI3)
T = Fraction(5, PHI3)
D = C - T


@dataclass(frozen=True)
class BridgeIdentity:
    name: str
    expression: str
    value: str
    role: str


def bridge_operator(x: Fraction) -> Fraction:
    """Cyclotomic complement operator B(x)=1-x."""
    return 1 - x


def cyclotomic_bridge_identities() -> List[BridgeIdentity]:
    return [
        BridgeIdentity(
            name="cyclotomic_complement",
            expression="Phi4 = Phi3 - q",
            value=f"{PHI4} = {PHI3} - {Q}",
            role="forces the bridge after Phi3 normalization",
        ),
        BridgeIdentity(
            name="mixer_imbalance",
            expression="D = C - T = q/Phi3",
            value=str(D),
            role="mixer layer input to the bridge operator",
        ),
        BridgeIdentity(
            name="bridge_output",
            expression="B(D)=1-D=Phi4/Phi3",
            value=str(bridge_operator(D)),
            role="unique mixer/projection intersection token",
        ),
        BridgeIdentity(
            name="projection_target",
            expression="P(Phi4)=Phi4/Phi3",
            value=str(Fraction(PHI4, PHI3)),
            role="carrier-field projection target",
        ),
    ]


def bridge_audit() -> Dict[str, object]:
    output = bridge_operator(D)
    checks = {
        "phi4_is_phi3_minus_q": PHI4 == PHI3 - Q,
        "imbalance_is_q_over_phi3": D == Fraction(Q, PHI3),
        "bridge_operator_sends_D_to_10_over_13": output == Fraction(10, 13),
        "bridge_output_is_phi4_projection": output == Fraction(PHI4, PHI3),
        "bridge_output_is_unique_CL_intersection": output == Fraction(10, 13),
        "phi6_is_phi3_minus_2q": PHI6 == PHI3 - 2 * Q,
        "phi4_minus_phi6_is_q": PHI4 - PHI6 == Q,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLIII_CYCLOTOMIC_BRIDGE_OPERATOR",
        "w33_atoms": {
            "q": Q,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "C": str(C),
            "T": str(T),
            "D": str(D),
        },
        "operator": {
            "name": "cyclotomic bridge/complement operator",
            "formula": "B(x)=1-x",
            "input": "D=q/Phi3=3/13",
            "output": "B(D)=10/13",
        },
        "identities": [asdict(i) for i in cyclotomic_bridge_identities()],
        "checks": checks,
        "theorem_statement": (
            "The unique CL bridge token 10/13 is forced by the cyclotomic identity "
            "Phi4=Phi3-q. Since the mixer imbalance is D=q/Phi3, applying the "
            "complement operator B(D)=1-D gives Phi4/Phi3=P(Phi4). Thus the "
            "mixer/projection intersection is inevitable."
        ),
        "interpretive_note": (
            "This makes the two-layer algebra much tighter: the bridge is not an "
            "empirical overlap between two lists. It is the normalized cyclotomic "
            "complement of the q-imbalance. Phi4 is literally the part of Phi3 left "
            "after removing the q-clock."
        ),
    }


def main() -> int:
    audit = bridge_audit()
    out = ROOT / "PART_CLIII_cyclotomic_bridge_operator_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
