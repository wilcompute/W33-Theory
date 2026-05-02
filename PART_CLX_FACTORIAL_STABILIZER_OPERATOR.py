#!/usr/bin/env python3
"""
PART CLX - Factorial Stabilizer Operator
=======================================

CLIX ended with the identity

    qE = 720 = 6! = (2q)!

where q=3 and E=240 is the W(3,3) edge carrier.

This module turns that into an operator theorem connecting the original seed

    q! = 2q

to the global E6 root stabilizer.

At q=3:

    q!   = 6       = 2q      = E6 Cartan rank
    (2q)! = 720    = qE      = E6 root stabilizer

Thus the same seed has two levels:

    local factorial seed:  q! = 2q
    global factorial lift: (2q)! = qE

Consequences:

    E = (2q)! / q = 240
    directed_edges = 2(2q)! / q = 480 = a0
    E6_roots = (2q)! / Phi4 = 72
    |W(E6)| = (2q)!^2 / Phi4 = 51840

The factorial stabilizer operator therefore closes the chain

    seed rank -> edge carrier -> root orbit -> Weyl group.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent

Q = 3
V = 40
K = 12
LAM = 2
MU = 4
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
E = V * K // 2
DIRECTED_EDGES = 2 * E
A0 = DIRECTED_EDGES
E6_DIM = 78
CARTAN_RANK = 2 * Q
E6_ROOTS = E6_DIM - CARTAN_RANK
ROOT_STABILIZER = Q * E
WEYL_E6_ORDER = E6_ROOTS * ROOT_STABILIZER
LOCAL_SEED = math.factorial(Q)
GLOBAL_LIFT = math.factorial(2 * Q)


@dataclass(frozen=True)
class FactorialClosureRow:
    name: str
    formula: str
    value: int
    interpretation: str


def factorial_closure_rows() -> List[FactorialClosureRow]:
    return [
        FactorialClosureRow(
            name="local_seed",
            formula="q! = 2q",
            value=LOCAL_SEED,
            interpretation="rank/Cartan seed",
        ),
        FactorialClosureRow(
            name="global_factorial_lift",
            formula="(2q)!",
            value=GLOBAL_LIFT,
            interpretation="factorial root-stabilizer scale",
        ),
        FactorialClosureRow(
            name="edge_carrier_from_lift",
            formula="E = (2q)!/q",
            value=GLOBAL_LIFT // Q,
            interpretation="W(3,3) undirected edge carrier",
        ),
        FactorialClosureRow(
            name="directed_edge_carrier_from_lift",
            formula="2(2q)!/q",
            value=2 * GLOBAL_LIFT // Q,
            interpretation="directed edge carrier a0",
        ),
        FactorialClosureRow(
            name="e6_root_orbit_from_lift",
            formula="(2q)!/Phi4",
            value=GLOBAL_LIFT // PHI4,
            interpretation="E6 root orbit size",
        ),
        FactorialClosureRow(
            name="weyl_order_from_lift",
            formula="(2q)!^2/Phi4",
            value=GLOBAL_LIFT * GLOBAL_LIFT // PHI4,
            interpretation="global Weyl closure |W(E6)|",
        ),
    ]


def factorial_stabilizer_audit() -> Dict[str, object]:
    checks = {
        "local_seed_q_factorial_equals_2q": LOCAL_SEED == 2 * Q == CARTAN_RANK == 6,
        "global_lift_is_2q_factorial": GLOBAL_LIFT == math.factorial(CARTAN_RANK) == 720,
        "root_stabilizer_is_global_lift": ROOT_STABILIZER == GLOBAL_LIFT == Q * E,
        "edge_carrier_from_global_lift": E == GLOBAL_LIFT // Q == 240,
        "directed_edges_from_global_lift": DIRECTED_EDGES == 2 * GLOBAL_LIFT // Q == 480,
        "a0_is_directed_edge_carrier": A0 == DIRECTED_EDGES == 480,
        "e6_roots_from_global_lift_over_phi4": E6_ROOTS == GLOBAL_LIFT // PHI4 == 72,
        "weyl_order_from_factorial_lift": WEYL_E6_ORDER == GLOBAL_LIFT * GLOBAL_LIFT // PHI4 == 51840,
        "weyl_order_from_roots_times_stabilizer": WEYL_E6_ORDER == E6_ROOTS * ROOT_STABILIZER,
        "phi4_divides_global_lift": GLOBAL_LIFT % PHI4 == 0,
        "global_lift_over_local_seed_is_5_factorial": GLOBAL_LIFT // LOCAL_SEED == math.factorial(5) == 120,
        "edge_carrier_is_2_times_5_factorial": E == 2 * math.factorial(5) == 240,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLX_FACTORIAL_STABILIZER_OPERATOR",
        "source_links": {
            "CLVIII": "E6 Weyl orbit-stabilizer closure",
            "CLIX": "root-stabilizer spectral action",
        },
        "w33_atoms": {
            "q": Q,
            "v": V,
            "k": K,
            "lambda": LAM,
            "mu": MU,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "edges_E": E,
            "directed_edges": DIRECTED_EDGES,
        },
        "factorial_scales": {
            "local_seed_q_factorial": LOCAL_SEED,
            "cartan_rank_2q": CARTAN_RANK,
            "global_lift_2q_factorial": GLOBAL_LIFT,
            "root_stabilizer_qE": ROOT_STABILIZER,
            "lift_over_seed": GLOBAL_LIFT // LOCAL_SEED,
        },
        "closure_rows": [asdict(r) for r in factorial_closure_rows()],
        "derived_closure": {
            "E": "E=(2q)!/q=240",
            "a0": "a0=2(2q)!/q=480",
            "E6_roots": "roots(E6)=(2q)!/Phi4=72",
            "W_E6": "|W(E6)|=(2q)!^2/Phi4=51840",
        },
        "checks": checks,
        "theorem_statement": (
            "The original seed q!=2q has a global factorial lift: at q=3, q!=2q=6 "
            "is the E6 Cartan rank, while (2q)!=720 equals the q-lifted W(3,3) edge "
            "carrier qE and hence the E6 root stabilizer.  Consequently E=(2q)!/q, "
            "a0=2(2q)!/q, roots(E6)=(2q)!/Phi4, and |W(E6)|=(2q)!^2/Phi4."
        ),
        "interpretive_note": (
            "This closes the seed-to-global loop.  The same factorial identity that "
            "selects q=3 locally expands to the E6 Weyl stabilizer globally.  The edge "
            "carrier, directed-edge spectral coefficient, root orbit, and Weyl order are "
            "all factorial descendants of q!=2q."
        ),
    }


def main() -> int:
    audit = factorial_stabilizer_audit()
    out = ROOT / "PART_CLX_factorial_stabilizer_operator_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
