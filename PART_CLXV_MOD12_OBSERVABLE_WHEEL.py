#!/usr/bin/env python3
"""
PART CLXV - Mod-12 Observable Wheel
==================================

CLXIII connected the decimal reptend 1/7 = 0.overline(142857) to

    base Phi4 = 10,
    denominator Phi6 = 7,
    period 2q = 6,
    missing decimal denominators {3,6,9} = {q,2q,q^2}.

CLXIV connected the toroidal genus equations to the residue gate

    H(n)=((n-3)(n-4))/12,

whose accepted residues are

    {3,4,7,12} = {q, q+1, Phi6, k}.

CLXV fuses these into a single mod-12 observable wheel.

The wheel has four simultaneous structures:

1. q-axis boundaries:
       {3,6,9,12} = {q,2q,q^2,k}

2. toroidal hole-gate residues:
       {3,4,7,12} = {q,q+1,Phi6,k}

3. decimal partition:
       terminating digits {1,2,4,5,8}, cyclic denominator {7}, q-axis {3,6,9}

4. stabilizer quarter-turn residues from J=5 in F_13:
       1 -> 5 -> 12 -> 8 -> 1

Together they assign the full 1..12 wheel:

    1  unit / decimal terminator / J-cycle identity
    2  binary duality q-1 / decimal terminator
    3  q boundary / genus zero root / missing decimal axis
    4  q+1 tetra seed / genus zero root / decimal terminator
    5  stabilizer residue J / threshold numerator / decimal terminator
    6  2q rank middle / q! seed / missing decimal axis
    7  Phi6 / genus-one torus / cyclic denominator
    8  carrier numerator J^{-1} / decimal terminator
    9  q^2 / missing decimal square axis
    10 Phi4 bridge/base
    11 Hashimoto norm k-1
    12 k / mod-12 closure / J^2=-1 / h=2q closure

The mod-12 wheel is therefore the common finite interface between decimal
cycles, toroidal genus, stabilizer residue dynamics, and W(3,3) graph atoms.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Set

ROOT = Path(__file__).resolve().parent

Q = 3
Q2 = Q * Q
RANK_SEED = 2 * Q
K = 12
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
J = 5
J_INV = 8
BINARY_DUALITY = Q - 1
HASHIMOTO_NORM = K - 1

Q_AXIS = {Q, RANK_SEED, Q2, K}
HOLE_GATE = {Q, Q + 1, PHI6, K}
DECIMAL_TERMINATING = {1, 2, 4, 5, 8}
DECIMAL_CYCLIC = {PHI6}
DECIMAL_MISSING_Q_AXIS = {Q, RANK_SEED, Q2}
J_CYCLE = [1, J, K, J_INV]
BRIDGE_ATOMS = {PHI4, PHI6, HASHIMOTO_NORM, K}


@dataclass(frozen=True)
class WheelResidue:
    residue: int
    quarter: int
    labels: List[str]
    primary_role: str


def quarter_of(n: int) -> int:
    return (n - 1) // Q + 1


def labels_for(n: int) -> List[str]:
    labels: List[str] = []
    if n in Q_AXIS:
        labels.append("q-axis boundary")
    if n in HOLE_GATE:
        labels.append("toroidal hole-gate residue")
    if n in DECIMAL_TERMINATING:
        labels.append("decimal terminating digit")
    if n in DECIMAL_CYCLIC:
        labels.append("decimal cyclic denominator")
    if n in DECIMAL_MISSING_Q_AXIS:
        labels.append("missing decimal q-axis")
    if n in J_CYCLE:
        labels.append("stabilizer J-cycle")
    if n == Q:
        labels.append("q")
    if n == Q + 1:
        labels.append("q+1 tetra seed")
    if n == J:
        labels.append("J stabilizer residue / threshold numerator")
    if n == RANK_SEED:
        labels.append("2q=q! rank middle")
    if n == PHI6:
        labels.append("Phi6 torus/cyclic threshold")
    if n == J_INV:
        labels.append("J inverse / carrier numerator")
    if n == Q2:
        labels.append("q^2 square axis")
    if n == PHI4:
        labels.append("Phi4 decimal base / bridge")
    if n == HASHIMOTO_NORM:
        labels.append("Hashimoto norm k-1")
    if n == K:
        labels.append("k=12 closure / J^2=-1")
    return labels


def primary_role(n: int) -> str:
    roles = {
        1: "unit / J-cycle identity",
        2: "binary duality q-1",
        3: "q boundary and genus zero root",
        4: "tetrahedral q+1 root",
        5: "stabilizer residue threshold numerator",
        6: "rank middle 2q=q!",
        7: "Phi6 torus and decimal cyclic denominator",
        8: "carrier numerator J inverse",
        9: "q^2 square axis",
        10: "Phi4 bridge/base",
        11: "Hashimoto norm",
        12: "k closure and -1 quarter-turn state",
    }
    return roles[n]


def wheel_rows() -> List[WheelResidue]:
    return [WheelResidue(n, quarter_of(n), labels_for(n), primary_role(n)) for n in range(1, K + 1)]


def quarter_table() -> List[Dict[str, object]]:
    rows = []
    for qtr in range(1, 5):
        residues = [n for n in range(1, K + 1) if quarter_of(n) == qtr]
        rows.append(
            {
                "quarter": qtr,
                "residues": residues,
                "boundary": residues[-1],
                "contains_hole_residue": sorted(set(residues) & HOLE_GATE),
                "contains_decimal_terminators": sorted(set(residues) & DECIMAL_TERMINATING),
                "contains_J_cycle": sorted(set(residues) & set(J_CYCLE)),
            }
        )
    return rows


def orbit_threads() -> Dict[str, object]:
    return {
        "q_axis_boundaries": sorted(Q_AXIS),
        "hole_gate_residues": sorted(HOLE_GATE),
        "decimal_terminating": sorted(DECIMAL_TERMINATING),
        "decimal_cyclic": sorted(DECIMAL_CYCLIC),
        "decimal_missing_q_axis": sorted(DECIMAL_MISSING_Q_AXIS),
        "stabilizer_J_cycle": J_CYCLE,
        "bridge_atoms": sorted(BRIDGE_ATOMS),
    }


def mod12_observable_wheel_audit() -> Dict[str, object]:
    all_residues = set(range(1, K + 1))
    tagged = {r.residue for r in wheel_rows() if r.labels}
    checks = {
        "q_axis_is_quarter_boundaries": Q_AXIS == {3, 6, 9, 12},
        "hole_gate_is_q_qp1_phi6_k": HOLE_GATE == {3, 4, 7, 12},
        "decimal_partition_1_to_9": DECIMAL_TERMINATING | DECIMAL_CYCLIC | DECIMAL_MISSING_Q_AXIS == set(range(1, 10)),
        "decimal_parts_disjoint": DECIMAL_TERMINATING.isdisjoint(DECIMAL_CYCLIC) and DECIMAL_TERMINATING.isdisjoint(DECIMAL_MISSING_Q_AXIS) and DECIMAL_CYCLIC.isdisjoint(DECIMAL_MISSING_Q_AXIS),
        "j_cycle_is_quarter_turn_thread": J_CYCLE == [1, 5, 12, 8],
        "j_square_is_k_mod_phi3": (J * J) % PHI3 == K,
        "j_inverse_is_carrier": J_INV == pow(J, -1, PHI3) == 8,
        "phi6_is_j_plus_binary_duality": J + BINARY_DUALITY == PHI6,
        "phi4_is_2j": 2 * J == PHI4,
        "hashimoto_norm_is_k_minus_one": HASHIMOTO_NORM == K - 1 == 11,
        "all_12_residues_tagged": tagged == all_residues,
        "hole_gate_hits_one_residue_per_quarter_or_boundary": [sorted(set(row["residues"]) & HOLE_GATE) for row in quarter_table()] == [[3], [4], [7], [12]],
        "q_axis_boundaries_match_quarter_boundaries": [row["boundary"] for row in quarter_table()] == [3, 6, 9, 12],
        "cyclic_phi6_is_first_after_rank_middle": PHI6 == RANK_SEED + 1 == 7,
        "base_phi4_sits_after_qsquare": PHI4 == Q2 + 1 == 10,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXV_MOD12_OBSERVABLE_WHEEL",
        "source_links": {
            "CLXII": "stabilizer field dynamics",
            "CLXIII": "decimal reptend compiler",
            "CLXIV": "toroidal genus/reptend bridge",
        },
        "w33_atoms": {
            "q": Q,
            "q_square": Q2,
            "rank_seed_2q": RANK_SEED,
            "k": K,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "J": J,
            "J_inverse": J_INV,
            "binary_duality_q_minus_1": BINARY_DUALITY,
            "Hashimoto_norm": HASHIMOTO_NORM,
        },
        "orbit_threads": orbit_threads(),
        "quarter_table": quarter_table(),
        "wheel_rows": [asdict(r) for r in wheel_rows()],
        "checks": checks,
        "theorem_statement": (
            "The mod-12 wheel is the common finite interface of the decimal reptend, "
            "toroidal genus gate, stabilizer quarter-turn, and W(3,3) atoms.  Its "
            "quarter boundaries are {3,6,9,12}={q,2q,q^2,k}; its toroidal residues "
            "are {3,4,7,12}={q,q+1,Phi6,k}; its decimal partition is "
            "{1,2,4,5,8} plus {7} plus {3,6,9}; and its stabilizer cycle is "
            "1->5->12->8->1."
        ),
        "interpretive_note": (
            "This makes the mod-12 wheel explicit.  The value 7=Phi6 is not just the "
            "decimal cyclic denominator or the torus solution: it is the first residue "
            "after the rank middle 6, the CRT recombination in the hole equation, and "
            "the realization closure J+(q-1)."
        ),
    }


def main() -> int:
    audit = mod12_observable_wheel_audit()
    out = ROOT / "PART_CLXV_mod12_observable_wheel_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
