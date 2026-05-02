#!/usr/bin/env python3
"""
PART CLXXIX - Torus / Firewall Factorization Layer
==================================================

CLXXVIII gave the closure square:

    36 --orient x2--> 72
     |                 |
    +9                +6
     |                 |
    45                78

with H1 lift 72+9=81.

CLXXIX connects that square back to the Eisenstein/toroidal map layer.

Core factorizations:

    36 = k*q       = 12*3
    45 = J*q^2     = 5*9
    72 = 2*k*q     = 2*36
    78 = 2*k*q+2q  = 72+6
    81 = q^4       = 72+9

Toroidal/Eisenstein side:

    Phi6 = N(q-1,1) = 7
    Csaszar/Szilassi shared edge count = 3*Phi6 = 21
    flag orbits = (2q)*Phi6 = 42
    flags = k*Phi6 = 84

Firewall-square side:

    affine triads = k*q = 36
    fiber/firewall triads = q^2 = 9
    cubic triads = J*q^2 = 45
    oriented affine roots = 2*k*q = 72

The key new identity is

    k*q + q^2 = 36 + 9 = 45 = J*q^2.

At q=3, this is equivalent to

    q(k+q) = q^2*J,

because k+q = 12+3=15 = q*J = 3*5.

So the firewall cubic count is the stabilizer-residue closure of the
mod-12 affine-triad skeleton over the q^2 fiber grid.
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
K = Q * (Q + 1)
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
RANK_SEED = 2 * Q
J = 5
J_INV = 8

AFFINE_TRIADS = K * Q
FIREWALL_FIBERS = Q2
CUBIC_TRIADS = AFFINE_TRIADS + FIREWALL_FIBERS
ORIENTED_ROOTS = 2 * AFFINE_TRIADS
E6_DIM = ORIENTED_ROOTS + RANK_SEED
H1_DIM = ORIENTED_ROOTS + FIREWALL_FIBERS

TORUS_EDGES = Q * PHI6
FLAG_ORBITS = RANK_SEED * PHI6
FLAGS = K * PHI6
NEXT_H6_EDGES = K * (K - 1) // 2


def eisenstein_norm(b: int, c: int) -> int:
    return b * b + b * c + c * c


@dataclass(frozen=True)
class FactorizationRow:
    name: str
    value: int
    formula: str
    interpretation: str


def factorization_rows() -> List[FactorizationRow]:
    return [
        FactorizationRow("affine_triads", AFFINE_TRIADS, "k*q=12*3=36", "mod-12 affine-triad skeleton over q"),
        FactorizationRow("firewall_fibers", FIREWALL_FIBERS, "q^2=9", "fiber/diagonal firewall grid"),
        FactorizationRow("cubic_triads", CUBIC_TRIADS, "k*q+q^2=J*q^2=45", "stabilizer-residue closure of affine plus fibers"),
        FactorizationRow("oriented_roots", ORIENTED_ROOTS, "2*k*q=72", "oriented affine triads / E6 roots"),
        FactorizationRow("E6_dimension", E6_DIM, "2*k*q+2q=78", "rank-completed E6 closure"),
        FactorizationRow("H1_dimension", H1_DIM, "2*k*q+q^2=q^4=81", "firewall-completed H1/triple-Albert closure"),
        FactorizationRow("torus_edges", TORUS_EDGES, "q*Phi6=3*7=21", "Csaszar/Szilassi shared edge count"),
        FactorizationRow("flag_orbits", FLAG_ORBITS, "2q*Phi6=42", "toroidal flag orbit count"),
        FactorizationRow("flags", FLAGS, "k*Phi6=84", "toroidal flag count"),
        FactorizationRow("next_h6_edges", NEXT_H6_EDGES, "C(k,2)=66", "next genus h=2q edge invariant"),
    ]


def torus_firewall_factorization_audit() -> Dict[str, object]:
    checks = {
        "k_is_q_qplus1": K == Q * (Q + 1) == 12,
        "phi6_eisenstein_norm": eisenstein_norm(Q - 1, 1) == PHI6 == 7,
        "affine_triads_are_kq": AFFINE_TRIADS == K * Q == 36,
        "firewall_fibers_are_q2": FIREWALL_FIBERS == Q2 == 9,
        "cubic_triads_are_affine_plus_fibers": CUBIC_TRIADS == AFFINE_TRIADS + FIREWALL_FIBERS == 45,
        "cubic_triads_are_J_q2": CUBIC_TRIADS == J * Q2 == 45,
        "closure_equation_k_plus_q_equals_qJ": K + Q == Q * J == 15,
        "oriented_roots_are_2kq": ORIENTED_ROOTS == 2 * K * Q == 72,
        "e6_is_2kq_plus_2q": E6_DIM == ORIENTED_ROOTS + RANK_SEED == 2 * K * Q + 2 * Q == 78,
        "h1_is_2kq_plus_q2": H1_DIM == ORIENTED_ROOTS + Q2 == Q4 == 81,
        "h1_minus_e6_is_q": H1_DIM - E6_DIM == Q == 3,
        "torus_edges_are_q_phi6": TORUS_EDGES == Q * PHI6 == 21,
        "flag_orbits_are_2q_phi6": FLAG_ORBITS == RANK_SEED * PHI6 == 42,
        "flags_are_k_phi6": FLAGS == K * PHI6 == 84,
        "flags_are_four_torus_edges": FLAGS == 4 * TORUS_EDGES,
        "next_h6_edges": NEXT_H6_EDGES == 66,
        "next_h6_edges_phi3J_plus_one": NEXT_H6_EDGES == PHI3 * J + 1 == 66,
        "threshold_carrier_inverse": (J * J_INV) % PHI3 == 1,
        "phi6_carrier_step": PHI6 + 1 == J_INV,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXXIX_TORUS_FIREWALL_FACTORIZATION",
        "source_links": {
            "CLXXIII": "Eisenstein torus map bridge",
            "CLXXVIII": "E6/H1 firewall closure square",
        },
        "w33_atoms": {
            "q": Q,
            "q2": Q2,
            "q3": Q3,
            "q4": Q4,
            "k": K,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "rank_seed_2q": RANK_SEED,
            "J": J,
            "J_inverse": J_INV,
        },
        "factorization_rows": [asdict(row) for row in factorization_rows()],
        "bridge_identities": {
            "eisenstein_generator": "Phi6=N(q-1,1)=7",
            "toroidal_projection": "q*Phi6=21, 2q*Phi6=42, k*Phi6=84",
            "firewall_projection": "k*q=36, q^2=9, J*q^2=45",
            "root_projection": "2*k*q=72, 2*k*q+2q=78, 2*k*q+q^2=81",
            "closure_equation": "k*q+q^2=J*q^2 because k+q=qJ",
        },
        "checks": checks,
        "theorem_statement": (
            "The firewall closure square is the mod-12/toroidal factorization of the same q=3 carrier. "
            "The affine triads are kq=36, the firewall grid is q^2=9, and the cubic total is kq+q^2=45=Jq^2. "
            "Orientation gives 2kq=72 roots; adding rank 2q gives E6=78, while adding firewall q^2 gives H1=q^4=81. "
            "On the torus side Phi6=N(q-1,1)=7 generates edges qPhi6=21, flag orbits 2qPhi6=42, and flags kPhi6=84."
        ),
        "interpretive_note": (
            "This connects the Eisenstein torus quotient directly to the firewall square.  The count 36 is not isolated: it is "
            "k times the q-clock.  The cubic 45 is not isolated either: it is the stabilizer-residue count J=5 over the q^2 fiber grid."
        ),
    }


def main() -> int:
    audit = torus_firewall_factorization_audit()
    out = ROOT / "PART_CLXXIX_torus_firewall_factorization_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
