#!/usr/bin/env python3
"""
PART CLXXVIII - E6 / H1 Firewall Closure Square
==============================================

CLXXVII interpreted the L-infinity firewall repair as homotopy completion of
the deleted q^2=9 diagonal/fiber sector.

CLXXVIII packages the architecture into one closure square.

Start with the 36 affine-line triads in the E6 cubic / Heisenberg model.
There are two basic closures:

    geometric cubic closure:
        36 + 9 = 45

    oriented root closure:
        2 * 36 = 72

The shared 72-sector then has two higher closures:

    E6 Lie closure:
        72 + 6 = 78

    H1 / triple-Albert generation closure:
        72 + 9 = 81

The same 9-sector also appears in the lower cubic closure:

        45 = 36 + 9.

So the square is:

        36  --orient x2-->  72
         |                  |
        +9                 +6     gives E6
         |                  |
        45                  78

and the H1 lift is:

        72 + 9 = 81.

Interpretation:
    - 36 is the unoriented affine-triad skeleton.
    - 72 is the oriented root/off-diagonal sector.
    - 9 is the firewall/fiber/diagonal sector.
    - 45 is the cubic tritangent/triad total.
    - 78 is E6 = rank 6 + roots 72.
    - 81 is H1 / triple-Albert = firewall 9 + roots 72.

This square is the clean finite architecture linking the cubic model, firewall,
E6 roots, H1 carrier, and L-infinity repair.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent

Q = 3
Q2 = Q * Q
Q3 = Q ** 3
Q4 = Q ** 4
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
J = 5
J_INV = 8
RANK_SEED = 2 * Q

AFFINE_TRIADS = 36
FIREWALL_FIBERS = Q2
CUBIC_TRIADS = AFFINE_TRIADS + FIREWALL_FIBERS
ORIENTED_ROOTS = 2 * AFFINE_TRIADS
E6_DIM = ORIENTED_ROOTS + RANK_SEED
H1_DIM = ORIENTED_ROOTS + FIREWALL_FIBERS
A2_DIM = J_INV
G0_DIM = E6_DIM + A2_DIM
E8_DIM = G0_DIM + H1_DIM + H1_DIM


@dataclass(frozen=True)
class ClosureNode:
    name: str
    value: int
    formula: str
    interpretation: str


def closure_nodes() -> List[ClosureNode]:
    return [
        ClosureNode("affine_triad_skeleton", AFFINE_TRIADS, "36", "unoriented affine-line triads"),
        ClosureNode("firewall_fiber_sector", FIREWALL_FIBERS, "q^2=9", "vertical fiber / diagonal completion sector"),
        ClosureNode("cubic_triad_total", CUBIC_TRIADS, "36+9=45", "E6 cubic tritangent/triad total"),
        ClosureNode("oriented_root_sector", ORIENTED_ROOTS, "2*36=72", "oriented affine/root/off-diagonal sector"),
        ClosureNode("rank_seed", RANK_SEED, "2q=6", "E6 Cartan/rank completion"),
        ClosureNode("E6_dimension", E6_DIM, "72+6=78", "E6 Lie closure"),
        ClosureNode("H1_triple_Albert", H1_DIM, "72+9=81", "H1/generation/triple-Albert closure"),
        ClosureNode("E8_Z3", E8_DIM, "(78+8)+81+81=248", "E8 Z3 closure"),
    ]


@dataclass(frozen=True)
class ClosureArrow:
    source: str
    target: str
    operation: str
    meaning: str


def closure_arrows() -> List[ClosureArrow]:
    return [
        ClosureArrow("36", "72", "orient x2", "unoriented affine triads become oriented E6-root directions"),
        ClosureArrow("36", "45", "+9", "add firewall/fiber triads to complete cubic triads"),
        ClosureArrow("72", "78", "+6", "add rank seed to close E6"),
        ClosureArrow("72", "81", "+9", "add firewall/fiber diagonal sector to close H1/triple-Albert"),
        ClosureArrow("78", "248", "+8,+81,+81", "add A2 carrier and dual generation sectors to close E8"),
    ]


def closure_square_audit() -> Dict[str, object]:
    checks = {
        "firewall_sector_is_q2": FIREWALL_FIBERS == Q2 == 9,
        "cubic_closure": CUBIC_TRIADS == AFFINE_TRIADS + FIREWALL_FIBERS == 45,
        "orientation_closure": ORIENTED_ROOTS == 2 * AFFINE_TRIADS == 72,
        "e6_closure": E6_DIM == ORIENTED_ROOTS + RANK_SEED == 78,
        "h1_closure": H1_DIM == ORIENTED_ROOTS + FIREWALL_FIBERS == Q4 == 81,
        "rank_seed_is_2q": RANK_SEED == 2 * Q == 6,
        "h1_minus_e6_is_q": H1_DIM - E6_DIM == Q == 3,
        "h1_minus_roots_is_firewall": H1_DIM - ORIENTED_ROOTS == FIREWALL_FIBERS,
        "e6_minus_roots_is_rank": E6_DIM - ORIENTED_ROOTS == RANK_SEED,
        "cubic_minus_affine_is_firewall": CUBIC_TRIADS - AFFINE_TRIADS == FIREWALL_FIBERS,
        "roots_are_e6_root_count": ORIENTED_ROOTS == 72,
        "e8_z3_closure": E8_DIM == (E6_DIM + A2_DIM) + H1_DIM + H1_DIM == 248,
        "a2_dim_is_carrier": A2_DIM == J_INV == 8,
        "threshold_carrier_inverse": (J * J_INV) % PHI3 == 1,
        "phi6_carrier_step": PHI6 + 1 == J_INV,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXXVIII_E6_H1_FIREWALL_CLOSURE_SQUARE",
        "source_links": {
            "CLXXVI": "firewall diagonal/fiber Albert bridge",
            "CLXXVII": "L-infinity firewall homotopy bridge",
        },
        "w33_atoms": {
            "q": Q,
            "q2": Q2,
            "q3": Q3,
            "q4": Q4,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "J": J,
            "J_inverse": J_INV,
            "rank_seed_2q": RANK_SEED,
        },
        "closure_nodes": [asdict(node) for node in closure_nodes()],
        "closure_arrows": [asdict(arrow) for arrow in closure_arrows()],
        "commuting_square": {
            "top": "36 --orient x2--> 72",
            "left": "36 --+9 firewall--> 45",
            "right_E6": "72 --+6 rank--> 78",
            "right_H1": "72 --+9 firewall--> 81",
            "interpretation": "36 is the affine-triad skeleton; 72 is oriented roots; 45 is cubic triads; 78 is E6; 81 is H1/triple-Albert",
        },
        "checks": checks,
        "theorem_statement": (
            "The E6 cubic, firewall, H1, and L-infinity structures fit into a closure square.  "
            "Starting from 36 affine triads, orientation gives 72 root directions, while adding the 9 firewall fibers gives "
            "45 cubic triads.  The same 72-sector closes to E6 by adding rank 6, and closes to H1/triple-Albert by adding "
            "the 9 firewall diagonal modes.  Thus 36->72, 36->45, 72->78, and 72->81 are four faces of the same finite closure architecture."
        ),
        "interpretive_note": (
            "This square is likely the simplest final explanation of the firewall.  It is the difference between Lie closure "
            "and generation-carrier closure: E6 adds rank 6 to roots 72, while H1 adds firewall/fiber 9 to roots 72.  "
            "The L-infinity repair appears exactly when one filters away the 9-sector but still expects strict closure."
        ),
    }


def main() -> int:
    audit = closure_square_audit()
    out = ROOT / "PART_CLXXVIII_e6_h1_firewall_closure_square_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
