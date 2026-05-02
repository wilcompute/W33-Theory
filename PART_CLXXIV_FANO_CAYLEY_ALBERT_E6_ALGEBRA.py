#!/usr/bin/env python3
"""
PART CLXXIV - Fano-Cayley / Albert / E6 Algebra
===============================================

Goal:
    Turn the heptad/Fano/Csaszar/Szilassi structure into an algebra, not just
    a count dictionary.

Construction:
    1. Use the CLXVI Fano plane as the multiplication skeleton for the seven
       imaginary octonion units.

    2. The seven heptad residues become imaginary units:

          {1,5,12,8,3,6,9}

       and an external scalar unit completes the 8-dimensional Cayley algebra:

          O = R * 1_scalar  +  span{e_1,e_5,e_12,e_8,e_3,e_6,e_9}.

    3. The Fano lines define products of imaginary units.  If {a,b,c} is a
       Fano line, then e_a e_b = +/- e_c depending on orientation; in all
       cases e_a^2 = -1 and e_a e_b = - e_b e_a.

    4. The resulting algebra has the standard octonion dimensions:

          dim O = 8 = 1 + Phi6.

    5. The 3x3 Hermitian matrices over O form the Albert algebra:

          dim J_3(O) = 3 + 3*8 = 27 = q^3.

       This is exactly one generation slice from CLXIX.

    6. The exceptional E6 Lie algebra has the standard Albert decomposition:

          dim e6 = dim f4 + dim J_3(O)_0 = 52 + 26 = 78.

       Therefore the heptad algebra supplies a concrete path:

          Fano heptad -> octonion carrier 8 -> Albert generation 27 -> E6 78.

This file does not claim a new classification theorem for E6.  It makes the
algebraic bridge explicit and auditable: the W33 heptad residues already carry
the Fano multiplication table needed to generate the octonion carrier whose
Albert algebra has the required q^3=27 generation dimension.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parent

Q = 3
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
RANK_SEED = 2 * Q
J = 5
J_INV = 8
K = 12
Q2 = Q * Q

# Residue-to-binary index map for PG(2,2) as nonzero vectors in F_2^3.
# This map makes the CLXVI Fano lines into xor triples.
RESIDUE_TO_INDEX: Dict[int, int] = {
    1: 0b001,
    5: 0b101,
    12: 0b011,
    8: 0b111,
    3: 0b100,
    6: 0b010,
    9: 0b110,
}
INDEX_TO_RESIDUE = {v: k for k, v in RESIDUE_TO_INDEX.items()}
HEPTAD_RESIDUES = [1, 5, 12, 8, 3, 6, 9]

# Standard oriented octonion lines in binary-index labels 1..7.
# If (a,b,c) is listed, then e_a e_b = e_c, cyclically.
ORIENTED_INDEX_LINES: List[Tuple[int, int, int]] = [
    (1, 2, 3),
    (1, 4, 5),
    (1, 7, 6),
    (2, 4, 6),
    (2, 5, 7),
    (3, 4, 7),
    (3, 6, 5),
]

FANO_LINES_RESIDUES: List[Tuple[int, int, int]] = [
    (1, 5, 3),
    (12, 8, 3),
    (1, 12, 6),
    (5, 8, 6),
    (1, 8, 9),
    (5, 12, 9),
    (3, 6, 9),
]

# Vector representation: dictionary basis_index -> integer coefficient.
# basis_index 0 is scalar.  basis_index 1..7 are imaginary octonion units.
Vector = Dict[int, int]


def _basis(i: int, coeff: int = 1) -> Vector:
    return {i: coeff}


def _clean(v: Vector) -> Vector:
    return {i: c for i, c in v.items() if c != 0}


def add(x: Vector, y: Vector) -> Vector:
    out: Vector = dict(x)
    for i, c in y.items():
        out[i] = out.get(i, 0) + c
    return _clean(out)


def scale(a: int, x: Vector) -> Vector:
    return _clean({i: a * c for i, c in x.items()})


# Build oriented pair table for imaginary basis indices.
PAIR_PRODUCT: Dict[Tuple[int, int], Tuple[int, int]] = {}
for a, b, c in ORIENTED_INDEX_LINES:
    cyc = [(a, b, c), (b, c, a), (c, a, b)]
    for x, y, z in cyc:
        PAIR_PRODUCT[(x, y)] = (1, z)
        PAIR_PRODUCT[(y, x)] = (-1, z)


def basis_mul(i: int, j: int) -> Vector:
    if i == 0:
        return _basis(j)
    if j == 0:
        return _basis(i)
    if i == j:
        return _basis(0, -1)
    sign, k = PAIR_PRODUCT[(i, j)]
    return _basis(k, sign)


def mul(x: Vector, y: Vector) -> Vector:
    out: Vector = {}
    for i, ci in x.items():
        for j, cj in y.items():
            term = scale(ci * cj, basis_mul(i, j))
            out = add(out, term)
    return _clean(out)


def conjugate(x: Vector) -> Vector:
    return {i: (c if i == 0 else -c) for i, c in x.items()}


def norm_squared(x: Vector) -> int:
    prod = mul(x, conjugate(x))
    # For this Cayley algebra, x*xbar is scalar.
    return prod.get(0, 0)


def associator(x: Vector, y: Vector, z: Vector) -> Vector:
    return add(mul(mul(x, y), z), scale(-1, mul(x, mul(y, z))))


def index_line_to_residue_line(line: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return tuple(INDEX_TO_RESIDUE[i] for i in line)  # type: ignore[return-value]


@dataclass(frozen=True)
class AlgebraLayer:
    name: str
    dimension: int
    formula: str
    interpretation: str


def algebra_layers() -> List[AlgebraLayer]:
    return [
        AlgebraLayer("imaginary_heptad", PHI6, "Phi6=7", "Fano/Csaszar/Szilassi heptad as imaginary units"),
        AlgebraLayer("cayley_octonion_carrier", 1 + PHI6, "1+Phi6=8=J^{-1}", "scalar unit plus heptad"),
        AlgebraLayer("albert_generation", Q ** 3, "3+3*8=27=q^3", "3x3 Hermitian octonion matrices"),
        AlgebraLayer("traceless_albert", Q ** 3 - 1, "27-1=26", "trace-free Albert directions"),
        AlgebraLayer("f4_derivations", 52, "2*(27-1)=52", "derivations of the Albert algebra"),
        AlgebraLayer("e6_albert_decomposition", 78, "52+26=78", "E6 as F4 plus traceless Albert"),
        AlgebraLayer("e6_root_split", 78, "6+72=78", "Cartan rank plus roots"),
    ]


def fano_cayley_albert_audit() -> Dict[str, object]:
    basis_units = [_basis(i) for i in range(8)]
    imag_units = [_basis(i) for i in range(1, 8)]

    # Algebraic checks on basis units.
    imaginary_squares = [basis_mul(i, i) for i in range(1, 8)]
    anti_comm_checks = []
    for i in range(1, 8):
        for j in range(1, 8):
            if i != j:
                anti_comm_checks.append(add(basis_mul(i, j), basis_mul(j, i)) == {})

    # Alternativity checks on all basis units.
    left_alt = []
    right_alt = []
    for x in basis_units:
        for y in basis_units:
            left_alt.append(associator(x, x, y) == {})
            right_alt.append(associator(y, x, x) == {})

    # Norm multiplicativity on a small deterministic sample of integral vectors.
    samples: List[Vector] = [
        _basis(0),
        _basis(1),
        add(_basis(0), _basis(1)),
        add(_basis(2), _basis(3)),
        add(add(_basis(4), _basis(5)), _basis(0)),
        add(add(_basis(6), _basis(7)), _basis(1)),
    ]
    norm_mult_checks = []
    for x in samples:
        for y in samples:
            norm_mult_checks.append(norm_squared(mul(x, y)) == norm_squared(x) * norm_squared(y))

    oriented_residue_lines = [index_line_to_residue_line(line) for line in ORIENTED_INDEX_LINES]
    unordered_oriented = {frozenset(line) for line in oriented_residue_lines}
    unordered_clxvi = {frozenset(line) for line in FANO_LINES_RESIDUES}

    checks = {
        "heptad_has_seven_imaginary_units": len(HEPTAD_RESIDUES) == PHI6 == 7,
        "octonion_carrier_dimension_is_eight": 1 + PHI6 == J_INV == 8,
        "residue_index_map_is_bijection": len(RESIDUE_TO_INDEX) == len(INDEX_TO_RESIDUE) == 7,
        "oriented_lines_match_clxvi_fano_lines_unordered": unordered_oriented == unordered_clxvi,
        "imaginary_units_square_to_minus_one": all(v == {0: -1} for v in imaginary_squares),
        "imaginary_units_anticommute": all(anti_comm_checks),
        "basis_alternativity_left": all(left_alt),
        "basis_alternativity_right": all(right_alt),
        "sample_norm_multiplicativity": all(norm_mult_checks),
        "albert_dimension_is_generation": 3 + 3 * (1 + PHI6) == Q ** 3 == 27,
        "traceless_albert_dimension": Q ** 3 - 1 == 26,
        "f4_plus_traceless_albert_is_e6": 52 + (Q ** 3 - 1) == 78,
        "e6_rank_plus_roots": RANK_SEED + 72 == 78,
        "e6_root_count_from_rank_subtraction": 78 - RANK_SEED == 72,
        "carrier_completion_matches_previous": PHI6 + 1 == J_INV,
        "threshold_carrier_inverse_mod_phi3": (J * J_INV) % PHI3 == 1,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXXIV_FANO_CAYLEY_ALBERT_E6_ALGEBRA",
        "source_links": {
            "CLXVI": "Fano affine completion",
            "CLXXI_CLXXII": "realization heptad and carrier completion",
            "CLXXIII": "Eisenstein torus map Phi6 generator",
        },
        "w33_atoms": {
            "q": Q,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "rank_seed_2q": RANK_SEED,
            "J_threshold": J,
            "J_inverse_carrier": J_INV,
        },
        "residue_to_octonion_index": {str(k): v for k, v in RESIDUE_TO_INDEX.items()},
        "oriented_fano_lines_residue_labels": [list(line) for line in oriented_residue_lines],
        "algebra_layers": [asdict(layer) for layer in algebra_layers()],
        "multiplication_summary": {
            "rule": "on each oriented Fano line (a,b,c), e_a e_b=e_c cyclically and anti-cyclic products are negative",
            "scalar_unit": "external scalar 1 completes the seven imaginary units to an 8D Cayley algebra",
            "imaginary_square": "e_r^2=-1 for every heptad residue r",
            "anticommutative": "e_r e_s=-e_s e_r for distinct imaginary units",
        },
        "checks": checks,
        "theorem_statement": (
            "The CLXVI heptad carries a Cayley/octonion algebra: the seven Fano residues are the imaginary units, "
            "and adjoining the scalar unit gives an 8D carrier 1+Phi6=8=J^{-1}.  The 3x3 Hermitian matrices over this "
            "carrier have dimension 3+3*8=27=q^3, giving one generation slice.  The standard Albert decomposition "
            "52+26=78 then matches E6, while 6+72=78 matches the rank/root split."
        ),
        "interpretive_note": (
            "This is the algebraic object the heptad has been asking for.  Csaszar/Szilassi give the geometric torus heptad, "
            "the Fano plane gives its multiplication table, the scalar/tetra origin completes it to the octonion carrier, "
            "and the Albert algebra gives the q^3=27 generation module connected to E6."
        ),
    }


def main() -> int:
    audit = fano_cayley_albert_audit()
    out = ROOT / "PART_CLXXIV_fano_cayley_albert_e6_algebra_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
