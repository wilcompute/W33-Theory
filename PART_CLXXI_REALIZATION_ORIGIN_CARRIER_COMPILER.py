#!/usr/bin/env python3
"""
PART CLXXI - Realization Origin / Carrier Compiler
==================================================

The fuller toroidal-triad page adds realization data:

    Csaszar realizations:     5
    Szilassi realizations:    2
    Tetrahedron seed:         1

There are two counts hidden in that data:

    toroidal geometric count:     5 + 2 = 7  = Phi6
    full triad geometric count:   1 + 5 + 2 = 8  = J^{-1}

The page also notes a combinatorial-type convention:

    1 tetrahedron + 5 Csaszar + 1 Szilassi = 7 combinatorial types,

because the two Szilassi geometric realizations collapse to one combinatorial
type.

Thus the realization data independently generates the same threshold/carrier
pair found earlier:

    J       = 5      Csaszar realization count / stabilizer residue
    q - 1   = 2      Szilassi mirror/duality count
    Phi6    = 7      toroidal realization closure
    +1      = seed   tetrahedron origin
    J^{-1}  = 8      full geometric triad count

The lone-1 asymmetry is also a Fano-origin decomposition:

    7 = 1 + 2 + 2 + 2.

In the Fano affine completion, choose origin 1.  The remaining six points pair
by direction:

    (5,3), (12,6), (8,9).

Each pair is an affine endpoint together with its point at infinity.  This is
the same 1+2+2+2 structure described for both Csaszar vertices and Szilassi
faces.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent

Q = 3
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
J = 5
J_INV = 8
BINARY_DUALITY = Q - 1
TETRA_SEED = 1
CSASZAR_REALIZATIONS = J
SZILASSI_REALIZATIONS = BINARY_DUALITY
SZILASSI_COMBINATORIAL_TYPES = 1
TOROIDAL_GEOMETRIC_REALIZATIONS = CSASZAR_REALIZATIONS + SZILASSI_REALIZATIONS
FULL_TRIAD_GEOMETRIC_COUNT = TETRA_SEED + TOROIDAL_GEOMETRIC_REALIZATIONS
COMBINATORIAL_TYPE_COUNT = TETRA_SEED + CSASZAR_REALIZATIONS + SZILASSI_COMBINATORIAL_TYPES

FANO_ORIGIN = 1
DIRECTION_PAIRS: List[Tuple[str, Tuple[int, int], str]] = [
    ("threshold_horizontal", (5, 3), "threshold affine endpoint plus q infinity"),
    ("rank_vertical", (12, 6), "k/opposition endpoint plus 2q infinity"),
    ("carrier_diagonal", (8, 9), "carrier endpoint plus q^2 infinity"),
]


@dataclass(frozen=True)
class RealizationCount:
    name: str
    value: int
    formula: str
    interpretation: str


def realization_counts() -> List[RealizationCount]:
    return [
        RealizationCount("Csaszar_realizations", CSASZAR_REALIZATIONS, "J=5", "stabilizer residue / threshold count"),
        RealizationCount("Szilassi_realizations", SZILASSI_REALIZATIONS, "q-1=2", "binary mirror/duality count"),
        RealizationCount("toroidal_geometric_total", TOROIDAL_GEOMETRIC_REALIZATIONS, "J+(q-1)=Phi6=7", "toroidal realization closure"),
        RealizationCount("tetrahedron_seed", TETRA_SEED, "1", "genus-zero origin seed"),
        RealizationCount("full_triad_geometric_total", FULL_TRIAD_GEOMETRIC_COUNT, "1+Phi6=8=J^{-1}", "carrier completion by adding the origin seed"),
        RealizationCount("combinatorial_type_total", COMBINATORIAL_TYPE_COUNT, "1+5+1=7=Phi6", "Szilassi mirror pair collapsed to one combinatorial type"),
    ]


@dataclass(frozen=True)
class FanoOriginPair:
    direction: str
    pair: List[int]
    interpretation: str


def fano_origin_pairs() -> List[FanoOriginPair]:
    return [FanoOriginPair(name, list(pair), interp) for name, pair, interp in DIRECTION_PAIRS]


def realization_origin_carrier_audit() -> Dict[str, object]:
    all_pair_points = [p for _, pair, _ in DIRECTION_PAIRS for p in pair]
    checks = {
        "csaszar_count_is_J": CSASZAR_REALIZATIONS == J == 5,
        "szilassi_count_is_binary_duality": SZILASSI_REALIZATIONS == BINARY_DUALITY == 2,
        "toroidal_realizations_are_phi6": TOROIDAL_GEOMETRIC_REALIZATIONS == PHI6 == 7,
        "full_geometric_total_is_carrier": FULL_TRIAD_GEOMETRIC_COUNT == J_INV == 8,
        "combinatorial_type_total_is_phi6": COMBINATORIAL_TYPE_COUNT == PHI6 == 7,
        "geometric_minus_combinatorial_is_one": FULL_TRIAD_GEOMETRIC_COUNT - COMBINATORIAL_TYPE_COUNT == 1,
        "carrier_is_threshold_plus_q": J_INV == J + Q == 8,
        "carrier_is_toroidal_plus_origin": J_INV == PHI6 + TETRA_SEED == 8,
        "phi6_is_J_plus_q_minus_one": PHI6 == J + (Q - 1) == 7,
        "fano_origin_decomposition_size": 1 + 2 + 2 + 2 == PHI6,
        "fano_pairs_cover_remaining_six": len(set(all_pair_points)) == 6,
        "origin_not_in_pairs": FANO_ORIGIN not in all_pair_points,
        "origin_plus_pairs_gives_seven": len({FANO_ORIGIN, *all_pair_points}) == PHI6 == 7,
        "direction_pairs_expected": {tuple(pair) for _, pair, _ in DIRECTION_PAIRS} == {(5, 3), (12, 6), (8, 9)},
        "threshold_and_carrier_inverse": (J * J_INV) % PHI3 == 1,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXXI_REALIZATION_ORIGIN_CARRIER_COMPILER",
        "source_hint": "full toroidal-triad page realization data: Csaszar 5, Szilassi 2, tetrahedron seed 1, and lone-1 asymmetry 1+2+2+2",
        "w33_atoms": {
            "q": Q,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "J_stabilizer_residue": J,
            "J_inverse_carrier": J_INV,
            "binary_duality_q_minus_1": BINARY_DUALITY,
        },
        "realization_counts": [asdict(r) for r in realization_counts()],
        "fano_origin_decomposition": {
            "origin": FANO_ORIGIN,
            "pairs": [asdict(p) for p in fano_origin_pairs()],
            "formula": "7 = 1 + 2 + 2 + 2",
            "interpretation": "lone origin plus three direction-pairs; same structure read as Csaszar vertices or Szilassi faces",
        },
        "bridge_identities": {
            "toroidal_realizations": "5+2=7=Phi6",
            "full_geometric_triad": "1+5+2=8=J^{-1}",
            "combinatorial_types": "1+5+1=7=Phi6",
            "carrier_transition": "Phi6+1=8 and J+q=8",
        },
        "checks": checks,
        "theorem_statement": (
            "The realization data realizes the same threshold/carrier grammar.  Csaszar's five realizations are J=5, "
            "Szilassi's two geometric realizations are q-1=2, and their toroidal total is Phi6=7.  Adding the tetrahedron "
            "origin gives 1+5+2=8=J^{-1}, the carrier residue.  Collapsing the two Szilassi geometries to one combinatorial "
            "type gives 1+5+1=7=Phi6."
        ),
        "interpretive_note": (
            "This uses the realizations rather than only the polyhedron counts.  The page's lone-1 asymmetry is the Fano-origin "
            "decomposition: one origin plus three affine/infinity direction-pairs.  The realization layer moves from threshold "
            "closure Phi6=7 to carrier completion J^{-1}=8 by adjoining the tetrahedron origin."
        ),
    }


def main() -> int:
    audit = realization_origin_carrier_audit()
    out = ROOT / "PART_CLXXI_realization_origin_carrier_compiler_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
