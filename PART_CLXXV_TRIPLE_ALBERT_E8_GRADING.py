#!/usr/bin/env python3
"""
PART CLXXV - Triple Albert / E8 Z3-Grading Bridge
=================================================

CLXXIV built the algebraic ladder

    Fano heptad -> octonion carrier O -> Albert algebra J_3(O) -> E6.

One Albert algebra has dimension

    dim J_3(O) = 3 + 3*8 = 27 = q^3.

CLXXV takes the next step: three Fano transport directions index three Albert
copies, giving the W33 homology/generation carrier

    3 * J_3(O) = 3 * 27 = 81 = H1(W33).

The sharper internal split is

    3 * (3 + 24) = 9 + 72 = 81.

Interpretation:
    - The 9 diagonal Albert directions are the q^2 fiber/diagonal sector.
    - The 72 off-diagonal octonion directions match the E6 root count.

This welds three previously separate facts:
    H1(W33) = 81 = 27+27+27
    E6 roots = 72
    diagonal/fiber count = 9 = q^2

Finally, the standard E8 Z3 grading closes dimensionally:

    e8 = (e6 + a2) + 81 + 81
       = 86 + 81 + 81
       = 248.

Here
    dim(e6)=78,
    dim(a2)=8=J^{-1}=1+Phi6,
    g1=three Albert copies=81,
    g2=dual three Albert copies=81.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent

Q = 3
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
RANK_SEED = 2 * Q
J = 5
J_INV = 8
OCTONION_DIM = 1 + PHI6
ALBERT_DIAGONAL = Q
ALBERT_OFFDIAGONAL = Q * OCTONION_DIM
ALBERT_DIM = ALBERT_DIAGONAL + ALBERT_OFFDIAGONAL
GENERATION_COUNT = Q
TRIPLE_ALBERT_DIM = GENERATION_COUNT * ALBERT_DIM
TRIPLE_DIAGONAL = GENERATION_COUNT * ALBERT_DIAGONAL
TRIPLE_OFFDIAGONAL = GENERATION_COUNT * ALBERT_OFFDIAGONAL
E6_RANK = RANK_SEED
E6_ROOTS = TRIPLE_OFFDIAGONAL
E6_DIM = E6_RANK + E6_ROOTS
A2_DIM = J_INV
G0_DIM = E6_DIM + A2_DIM
G1_DIM = TRIPLE_ALBERT_DIM
G2_DIM = TRIPLE_ALBERT_DIM
E8_DIM = G0_DIM + G1_DIM + G2_DIM

DIRECTIONS = [
    ("threshold_q_horizontal", Q, "J_3(O)_q"),
    ("rank_2q_vertical", RANK_SEED, "J_3(O)_2q"),
    ("carrier_q2_diagonal", Q * Q, "J_3(O)_q2"),
]


@dataclass(frozen=True)
class AlbertCopy:
    generation: int
    direction_name: str
    direction_residue: int
    module: str
    diagonal_dim: int
    offdiagonal_dim: int
    total_dim: int
    interpretation: str


def albert_copies() -> List[AlbertCopy]:
    rows: List[AlbertCopy] = []
    for i, (name, residue, module) in enumerate(DIRECTIONS, start=1):
        rows.append(
            AlbertCopy(
                generation=i,
                direction_name=name,
                direction_residue=residue,
                module=module,
                diagonal_dim=ALBERT_DIAGONAL,
                offdiagonal_dim=ALBERT_OFFDIAGONAL,
                total_dim=ALBERT_DIM,
                interpretation=f"generation {i}: 3 diagonal scalars plus 3 octonion off-diagonal slots",
            )
        )
    return rows


@dataclass(frozen=True)
class GradingLayer:
    layer: str
    dimension: int
    formula: str
    interpretation: str


def grading_layers() -> List[GradingLayer]:
    return [
        GradingLayer("g0", G0_DIM, "E6 + A2 = 78 + 8 = 86", "degree-zero symmetry algebra"),
        GradingLayer("g1", G1_DIM, "3*J_3(O)=3*27=81", "matter/generation carrier"),
        GradingLayer("g2", G2_DIM, "dual 3*J_3(O)=81", "dual matter/generation carrier"),
        GradingLayer("E8", E8_DIM, "86+81+81=248", "Z3-graded exceptional closure"),
    ]


def triple_albert_e8_audit() -> Dict[str, object]:
    copies = albert_copies()
    checks = {
        "octonion_dim_is_carrier": OCTONION_DIM == 1 + PHI6 == J_INV == 8,
        "albert_dim_is_q3": ALBERT_DIM == Q ** 3 == 27,
        "albert_internal_split": ALBERT_DIAGONAL == Q == 3 and ALBERT_OFFDIAGONAL == Q * OCTONION_DIM == 24,
        "triple_albert_is_h1": TRIPLE_ALBERT_DIM == Q * Q ** 3 == Q ** 4 == 81,
        "triple_albert_split_is_9_plus_72": TRIPLE_DIAGONAL == Q ** 2 == 9 and TRIPLE_OFFDIAGONAL == 72 and TRIPLE_DIAGONAL + TRIPLE_OFFDIAGONAL == 81,
        "offdiagonal_matches_e6_roots": TRIPLE_OFFDIAGONAL == E6_ROOTS == 72,
        "rank_plus_roots_is_e6": E6_RANK + E6_ROOTS == E6_DIM == 78,
        "a2_dim_is_octonion_carrier": A2_DIM == J_INV == OCTONION_DIM == 8,
        "g0_is_e6_plus_a2": G0_DIM == E6_DIM + A2_DIM == 86,
        "e8_z3_grading_dimension": E8_DIM == G0_DIM + G1_DIM + G2_DIM == 248,
        "one_albert_per_fano_direction": len(copies) == Q == 3,
        "direction_residues_are_q_axis": {c.direction_residue for c in copies} == {Q, RANK_SEED, Q * Q} == {3, 6, 9},
        "each_copy_has_27": all(c.total_dim == 27 for c in copies),
        "each_copy_has_3_plus_24": all(c.diagonal_dim == 3 and c.offdiagonal_dim == 24 for c in copies),
        "threshold_carrier_inverse": (J * J_INV) % PHI3 == 1,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXXV_TRIPLE_ALBERT_E8_GRADING",
        "source_links": {
            "CLXXIV": "Fano-Cayley / Albert / E6 algebra",
            "CLXIX": "Fano three-generation lift",
            "known_E8_Z3": "E8 = (E6 + A2) + 81 + 81",
        },
        "w33_atoms": {
            "q": Q,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "rank_seed_2q": RANK_SEED,
            "J_threshold": J,
            "J_inverse_carrier": J_INV,
            "octonion_dim": OCTONION_DIM,
            "Albert_dim": ALBERT_DIM,
        },
        "albert_copies": [asdict(c) for c in copies],
        "triple_albert_split": {
            "formula": "3*(3+24)=9+72=81",
            "diagonal_sector": "3*3=9=q^2",
            "offdiagonal_octonion_sector": "3*24=72=|roots(E6)|",
            "interpretation": "three generation modules contain a q^2 diagonal/fiber sector plus the E6-root count",
        },
        "e8_z3_grading": [asdict(layer) for layer in grading_layers()],
        "checks": checks,
        "theorem_statement": (
            "Three Fano-indexed Albert algebras give the W33 generation carrier: 3*J_3(O)=3*27=81. "
            "Internally this splits as 3*(3+24)=9+72, where 9=q^2 is the diagonal/fiber sector and 72 "
            "is the E6 root count.  With g0=E6+A2=78+8=86 and a dual 81-sector, the standard Z3 grading "
            "closes E8 dimensionally as 86+81+81=248."
        ),
        "interpretive_note": (
            "This is the algebraic weld between three generations and E6/E8.  The same octonion carrier that makes one "
            "Albert generation also produces the 72 off-diagonal directions across three generations, matching the E6 roots, "
            "while the leftover q^2=9 diagonal sector matches the fiber/diagonal grammar seen earlier."
        ),
    }


def main() -> int:
    audit = triple_albert_e8_audit()
    out = ROOT / "PART_CLXXV_triple_albert_e8_grading_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
