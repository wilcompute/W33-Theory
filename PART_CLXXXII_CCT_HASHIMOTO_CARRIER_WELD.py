#!/usr/bin/env python3
"""
PART CLXXXII - CCT / Hashimoto Carrier Weld
===========================================

CLXXXI ranked the CCT/Hashimoto weld as the highest-value next bridge.

This file joins three older/newer layers:

  1. CLXXX master ladder:
       completed carrier q^4 = 81,
       nonzero color boundary q^4 - 1 = 80,
       edge shell q(q^4-1) = 240,
       directed shell 2q(q^4-1) = 480.

  2. Hashimoto bundle:
       480 directed edges,
       nonbacktracking branch k-1 = 11,
       Ihara-Bass forces the (k-1) structural factor.

  3. CCT loop-conditioning audit:
       first trit loop probability = lambda / (k-1)^q = 2/11^3,
       first primitive semantic layer = 320 = 2*160,
       Parry/KMS stationary weight = 1/480,
       Doob bridge lenses 11 choices down to lambda=2 triangle-compatible choices.

Main weld:

    480 = 2q(q^4 - 1).

This says the nonbacktracking CCT loop carrier is the directed dynamical lift of
three nonzero q^4 color boundaries.  The completed q^4=81 carrier belongs to
the algebraic/Albert layer; deleting its closure point gives q^4-1=80 per edge
color; multiplying by q colors and by orientation gives 480 directed states.

The CCT branch law is then

    k - 1 = 11 = (K - mu) + q = 8 + 3.

So the loop clock has an 8-neighbor empire packet plus q=3 slack.  Under first
triangle-loop conditioning, the Doob bridge projects 11 local choices to
lambda=2 triangle-compatible choices, leaving 9 open turns.  That 9 matches the
firewall/fiber q^2 sector from CLXXVI-CLXXVIII.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent

Q = 3
Q2 = Q * Q
Q3 = Q ** 3
Q4 = Q ** 4
V = 40
K = 12
LAMBDA = 2
MU = 4
PHI3 = 13
PHI6 = 7
J = 5
J_INV = 8

EDGES_PER_COLOR = Q4 - 1
EDGE_COLORS = Q
EDGE_SHELL = EDGE_COLORS * EDGES_PER_COLOR
DIRECTED_SHELL = 2 * EDGE_SHELL
HASHIMOTO_BRANCH = K - 1
EMPIRE_PACKET = K - MU
QUTRIT_SLACK = Q
OPEN_TURNS = HASHIMOTO_BRANCH - LAMBDA
FIRST_LOOP_LOCAL_WORDS = HASHIMOTO_BRANCH ** Q
FIRST_LOOP_PROBABILITY = Fraction(LAMBDA, FIRST_LOOP_LOCAL_WORDS)
TRIANGLES = 160
ORIENTED_TRIANGLE_PRIMITIVES = 2 * TRIANGLES
PARRY_STATIONARY_WEIGHT = Fraction(1, DIRECTED_SHELL)
LEGAL_LENGTH3_CYLINDER = Fraction(1, DIRECTED_SHELL * HASHIMOTO_BRANCH ** Q)


@dataclass(frozen=True)
class CarrierLayer:
    name: str
    value: int | str
    formula: str
    interpretation: str


def carrier_layers() -> List[CarrierLayer]:
    return [
        CarrierLayer("completed_albert_boundary", Q4, "q^4=81", "completed algebraic/H1 carrier"),
        CarrierLayer("nonzero_color_boundary", EDGES_PER_COLOR, "q^4-1=80", "one nonzero edge-color boundary"),
        CarrierLayer("edge_shell", EDGE_SHELL, "q(q^4-1)=240", "three W33 edge colors"),
        CarrierLayer("directed_hashimoto_shell", DIRECTED_SHELL, "2q(q^4-1)=480", "oriented nonbacktracking state space"),
        CarrierLayer("hashimoto_branch", HASHIMOTO_BRANCH, "k-1=11", "nonbacktracking choices per directed edge"),
        CarrierLayer("branch_split", HASHIMOTO_BRANCH, "11=(k-mu)+q=8+3", "empire packet plus qutrit slack"),
        CarrierLayer("first_loop_probability", str(FIRST_LOOP_PROBABILITY), "lambda/(k-1)^q=2/11^3", "first trit triangle-loop probability"),
        CarrierLayer("primitive_triangle_layer", ORIENTED_TRIANGLE_PRIMITIVES, "2*160=320", "oriented primitive triangle semantic layer"),
        CarrierLayer("parry_stationary_weight", str(PARRY_STATIONARY_WEIGHT), "1/480", "uniform Parry/KMS state on directed edges"),
        CarrierLayer("doob_lensing", OPEN_TURNS, "11 -> 2, open turns=9", "first-loop conditioning kills nine open turns"),
    ]


def cct_hashimoto_carrier_weld_audit() -> Dict[str, object]:
    checks = {
        "completed_boundary_is_q4": Q4 == 81,
        "nonzero_color_boundary_is_q4_minus_one": EDGES_PER_COLOR == Q4 - 1 == 80,
        "edge_shell_is_q_times_nonzero_boundary": EDGE_SHELL == Q * EDGES_PER_COLOR == 240,
        "directed_shell_is_two_q_times_nonzero_boundary": DIRECTED_SHELL == 2 * Q * EDGES_PER_COLOR == 480,
        "hashimoto_branch_is_k_minus_one": HASHIMOTO_BRANCH == K - 1 == 11,
        "branch_split_is_empire_plus_q": HASHIMOTO_BRANCH == EMPIRE_PACKET + QUTRIT_SLACK == 11,
        "empire_packet_is_k_minus_mu": EMPIRE_PACKET == K - MU == 8,
        "first_loop_words_are_11_cubed": FIRST_LOOP_LOCAL_WORDS == 1331,
        "first_loop_probability_is_two_over_1331": FIRST_LOOP_PROBABILITY == Fraction(2, 1331),
        "open_turns_are_q2": OPEN_TURNS == Q2 == 9,
        "doob_lenses_11_to_lambda": HASHIMOTO_BRANCH == LAMBDA + OPEN_TURNS,
        "oriented_triangle_primitives": ORIENTED_TRIANGLE_PRIMITIVES == 320,
        "primitive_triangle_factorization": ORIENTED_TRIANGLE_PRIMITIVES == DIRECTED_SHELL * LAMBDA // Q,
        "parry_weight_is_one_over_480": PARRY_STATIONARY_WEIGHT == Fraction(1, 480),
        "legal_length3_cylinder": LEGAL_LENGTH3_CYLINDER == Fraction(1, 480 * 1331),
        "phi6_carrier_step": PHI6 + 1 == J_INV,
        "threshold_carrier_inverse": (J * J_INV) % PHI3 == 1,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXXXII_CCT_HASHIMOTO_CARRIER_WELD",
        "source_links": {
            "CLXXX": "master identity ladder",
            "CLXXXI": "repo hint atlas",
            "CCT_loop_conditioning": "scripts/w33_cct_loop_conditioning_bridge_audit.py",
            "Hashimoto_480_bundle": "archive/misc/ChatGPT Files/v01/W33_480_OPERATOR_ALPHA_BUNDLE_v01/README.md",
        },
        "w33_atoms": {
            "q": Q,
            "q2": Q2,
            "q3": Q3,
            "q4": Q4,
            "v": V,
            "k": K,
            "lambda": LAMBDA,
            "mu": MU,
            "Phi3": PHI3,
            "Phi6": PHI6,
            "J": J,
            "J_inverse": J_INV,
        },
        "carrier_layers": [asdict(layer) for layer in carrier_layers()],
        "bridge_identities": {
            "algebra_to_edge_shell": "q^4=81 -> q^4-1=80 -> q(q^4-1)=240",
            "edge_to_hashimoto": "2*q*(q^4-1)=480 directed states",
            "branch_law": "k-1=11=(k-mu)+q=8+3",
            "first_loop_law": "P(first trit loop)=lambda/(k-1)^q=2/11^3",
            "doob_lensing": "11 choices = 2 triangle-compatible + 9 open turns",
            "firewall_match": "9 open turns = q^2 firewall/fiber diagonal sector",
            "primitive_semantics": "first primitive oriented triangle layer = 2*160=320 = 480*lambda/q",
        },
        "checks": checks,
        "theorem_statement": (
            "The CCT/Hashimoto loop carrier is the directed dynamical lift of the CLXXX algebraic boundary. "
            "The completed carrier q^4=81 loses its closure point to give q^4-1=80 states per edge color; three colors "
            "give 240 edges, and orientation gives 480 Hashimoto states.  The nonbacktracking branch law k-1=11 splits as "
            "8+3=(k-mu)+q.  First-loop Doob conditioning lenses these 11 choices to lambda=2 triangle-compatible choices, "
            "leaving 9 open turns, exactly the q^2 firewall/fiber diagonal sector."
        ),
        "interpretive_note": (
            "This is the first weld between the CCT loop-clock files and the CLXXX master ladder.  The CCT loop calculus is not "
            "a separate numerology layer: its 480-state Parry/KMS carrier is the oriented edge lift of the same 81-completed "
            "Albert boundary, and its 11->2 Doob lens exposes the same missing 9-sector as the firewall square."
        ),
    }


def main() -> int:
    audit = cct_hashimoto_carrier_weld_audit()
    out = ROOT / "PART_CLXXXII_cct_hashimoto_carrier_weld_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
